"""General utility class and functions for internal EmaCalc use.

Defines class
EmaParamBase --- container for common properties used by all model classes
    specifying the indexing of separate types of parameters.

NOTE: To make the model identifiable,
although both latent-variable locations and response thresholds are freely variable,
and the zero point on the attribute scale is arbitrary,
some restriction is necessary.

This behavior is user-controlled by initialization arguments
restrict_attribute and restrict_threshold.

The model must also be slightly restricted by a weakly informative prior,
for numerical stability in case of extreme response patterns,
e.g., ALL ratings in the highest ordinal category.


*** Version history:
* Version 0.9.2:
2022-06-12, response-threshold mapping functions
    mapped_width(), d_mapped_width_d_eta(), and mapped_width_inv()
    slightly modified to be safe against numerical underflow.
    Global PRIOR_PSEUDO_RESPONDENT slightly modified, with no apparent effect on result.

* Version 0.9:
2022-03-17, use Pandas CategoricalDtype instances in EmaFrame scenarios and attributes
2022-03-18, use Pandas DataFrame for EMA data in EmaDataSet, to allow many input file formats

* Version 0.8.1
2022-02-28, changed class name -> EmaParamBase
2022-02-23, GMM comp moved to ema_model.EmaGroupModel, separate GMM for each group

* Version 0.7.1
2022-01-11, _make_prior with log normalized uniform scenario prob

* Version 0.7
2022-01-02, minor cleanup _make_prior: ONLY scalar precision shape for GMM components

* Version 0.6
2021-12-03, user-definable prior inter-individual variance for reference parameters
2021-12-05, testing ways to set hyper-prior
2021-12-06, boolean properties restrict_attribute, restrict_threshold of EmaParamBase
            for user-specified model restriction
2021-12-08, minor checks against numerical overflow

* Version 0.5.1
2021-11-26, allow ZERO Attributes, i.e., empty emf.attribute_grades
2021-12-01, cleanup some doc comments
2021-12-02, Attribute sensory location fixed == 0. for first Scenario category
            regardless of regression_effect specification.

* Version 0.5
2021-11-24, first published beta version
"""
import numpy as np
from scipy.special import logit, expit
import logging

from EmaCalc.gauss_gamma import GaussianRV

# ------------------------------------------------------
__version__ = "2022-06-12"

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # *** TEST

PRIOR_PSEUDO_RESPONDENT = 0.5  # seems to work OK, previous version = 0.1
# = hyperprior total pseudo-count re ONE real respondent
# = prior GaussianRV.mean.learned_weight for all GMM components.
# This value is NOT critical for Occam's Razor behavior.

PRIOR_PARAM_SCALE = 1.
# = main hyperprior scale of most Gaussian model parameters,
# defined in Thurstone d-prime units for attribute parameters,
# rescaled if the Bradley (logistic) model is used for latent variables.
# This prior may have effect on the Occam's Razor function:
# small values may allow several active GMM components with small variance,
# but experiments suggest the prior value is not critical.

PRIOR_PREC_A = PRIOR_PSEUDO_RESPONDENT / 2
# = GaussianRV precision shape for ALL parameters

PRIOR_PREC_B = PRIOR_PARAM_SCALE**2 / 2
# = GaussianRV precision inv_scale for MOST EmaModel parameters
# -> allows very small precision <=> large inter-individual variance
# -> mode of prior component-element variance = PRIOR_PREC_B /(PRIOR_PREC_A + 1) approx= PRIOR_PREC_B

ETA_W_EPSILON = np.finfo(float).eps
# = additive constant to prevent too small mapped_width(eta)


# ------------------------------------------------------------------
class EmaParamBase:
    """Container for common properties of ema_model.EmaModel and its sub-models.

    Each individual parameter distribution is represented by
    a large set of samples, stored as property EmaSubjectModel.xi, with
    xi[s, :] = s-th sample of the parameter vector for ONE subject.

    All model classes share mapping properties defined here,
    for extracting parameter subsets
    from the array of parameter vectors.
    """
    # *** Future: define threshold_slices separate from attribute_slices,
    # *** to allow identical thresholds tied for several attributes.
    def __init__(self, emf, effects, rv_class,
                 theta_map,
                 scenario_slices,
                 attribute_slices,
                 comp_prior,
                 restrict_attribute=False,
                 restrict_threshold=False):
        """
        :param emf: single ema_data.EmaFrame instance,
        :param effects: iterable with regression-effect terms for attribute regression
            effects[i] = single key in emf.scenarios.keys() or tuple of such keys
        :param rv_class: latent sensory variable class,
            defining its distribution as either logistic or normal.
        :param theta_map: fixed 2D array to extract latent-variable location samples from xi array
        :param scenario_slices: list of slice objects, such that
            xi[:, scenario_slices[t]] = alpha = log-prob for scenarios in t-th test phase
        :param attribute_slices: list of slice objects, such that
            xi[:, attribute_slices[i]] = all (beta, eta) parameters for i-th Attribute
            where
            beta = xi[:, attribute_slices[i]][:, :n_beta] = regression-effect parameters
            eta = xi[:, attribute_slices[i]][:, n_beta:] = threshold parameters
            where
            n_beta = n of regression-effect parameters, same for each attribute question.
        :param comp_prior: single GaussianRV instance, prior for ALL GMM components,
        :param restrict_attribute: (optional) boolean switch
            to force restriction on attribute sensory-variable locations
        :param restrict_threshold: (optional) boolean switch
            to force restriction on response-threshold locations
        """
        self.emf = emf
        self.effects = effects
        self.rv_class = rv_class
        self.theta_map = theta_map
        self.scenario_slices = scenario_slices
        self.attribute_slices = attribute_slices
        self.comp_prior = comp_prior
        self.restrict_attribute = restrict_attribute
        self.restrict_threshold = restrict_threshold

    @classmethod
    def initialize(cls, emf, effects, rv_class,
                   restrict_attribute=False,
                   restrict_threshold=False):
        """Assign all parameter-extraction properties, and
        GaussianRV mixture components with correct size.
        :param emf: single ema_data.EmaFrame instance,
            defining the experiment structure.
        :param effects: iterable with regression-effect terms for attribute regression
            effects[i] = single key in emf.scenarios.keys() or tuple of such keys
        :param rv_class: latent sensory variable class,
            defining its distribution as either logistic or normal.
        :param restrict_attribute: (optional) boolean switch
            to force restriction on attribute sensory-variable locations
        :param restrict_threshold: (optional) boolean switch
            to force restriction on response-threshold locations
        :return: None

        Result: all properties initialized
        """
        _check_effects(emf, effects)
        effects = [e_i if type(e_i) is tuple else (e_i,)
                   for e_i in effects]
        # = list of requested regression effects of scenario categories
        # to be estimated for their influence on ATTRIBUTE responses.
        # Each element MUST be a tuple with one or more scenario key(s).

        # Define mapping indices from rows of xi array to its parts:
        n_phases = emf.scenario_shape[0]
        n_scenarios = np.prod(emf.scenario_shape[1:], dtype=int)  # except phases
        scenario_slices = _make_slices(n_phases * [n_scenarios])
        # = list of slice objects, such that
        # xi[:, cls.scenario_slices[t]] = alpha = log-prob for scenarios in t-th test phase
        # i.e., n_phases slices with equal lengths, for all test phases.

        theta_map = _theta_map(emf, effects)
        # = fixed 2D array to extract latent-variable location samples from xi array
        # by method attribute_theta(...)

        n_beta = theta_map.shape[0]
        # = number of regression-effect parameters, same for every Attribute
        n_attr_param = [n_beta + len(grade.categories)
                        for grade in emf.attribute_grades.values()]
        # n_attr_param[i] = total number of model params for i-th Attribute
        # NOTE: May be EMPTY if no Attributes are defined
        attribute_slices = _make_slices(n_attr_param,
                                        start=scenario_slices[-1].stop)
        # xi[:, cls.attribute_slices[i]] = all (beta, eta) parameters for i-th Attribute
        # where
        # beta = xi[:, cls.attribute_slices[i]][:, :n_beta] = regression-effect parameters
        # eta = xi[:, cls.attribute_slices[i]][:, n_beta:] = threshold parameters
        # where
        # n_beta = n of regression-effect parameters, same for each attribute question.
        if len(attribute_slices) > 0:
            n_parameters = attribute_slices[-1].stop
        else:
            n_parameters = scenario_slices[-1].stop

        # define mixture components:
        comp_prior = _make_prior(n_parameters, n_beta,
                                 scenario_slices,
                                 attribute_slices, rv_class)
        # = single GaussianRV instance, prior for ALL GMM components,
        # fixed throughout the VI learning procedure.
        logger.debug(f'PRIOR_PSEUDO_RESPONDENT = {PRIOR_PSEUDO_RESPONDENT:.3f}; ' +
                     f'PRIOR_PARAM_SCALE = {PRIOR_PARAM_SCALE:.3f}; ' +
                     f'PRIOR_PREC_A = {PRIOR_PREC_A:.3f}; ' +
                     f'PRIOR_PREC_B = {PRIOR_PREC_B:.3f}')
        logger.debug(f'comp_prior.prec.a = {comp_prior.prec.a:.3f}')
        logger.debug('comp_prior.prec.b = '
                     + np.array_str(comp_prior.prec.b,
                                    precision=5))
        logger.debug('mode{1 / comp_prior.prec}= '
                     + np.array_str(comp_prior.prec.mode_inv(),
                                    precision=5))
        return cls(emf, effects, rv_class,
                   theta_map,
                   scenario_slices,
                   attribute_slices,
                   comp_prior,
                   restrict_attribute,
                   restrict_threshold)

    @property
    def n_parameters(self):
        if len(self.attribute_slices) > 0:
            return self.attribute_slices[-1].stop
        else:
            return self.scenario_slices[-1].stop

    @property
    def n_beta(self):
        """Total number of regression-effect parameters, same for each Attribute
        """
        return self.theta_map.shape[0]

    @property
    def attribute_slice_dict(self):
        """
        :return: dict with elements (attribute_key, attribute_slice)
        """
        return dict((a, a_slice)
                    for (a, a_slice) in zip(self.emf.attribute_grades.keys(),
                                            self.attribute_slices))

    def beta_0_size(self):
        """number of effect parameters for FIRST effect term
        :return: n_beta = scalar

        NOTE: matches sizes defined in _theta_map()
        """
        return np.prod([len(self.emf.scenarios[sc_i].categories) for sc_i in self.effects[0]],
                       dtype=int)

    def scenario_prob(self, xi):
        """Extract probability-mass for scenarios, given parameters,
        used mainly by ema_display
        :param xi: 2D array with parameter samples
        :return: u = mD array with scenario probability-mass within each phase,
            u[s, k0, k1, k2, ...] = s-th sample of P[(k1, k2,...)-th scenario | phase k0]
            sum u[s, k0] == 1., for all s and k0

        2022-02-15, check for underflow
        """
        n_sc = self.scenario_slices[-1].stop
        alpha = xi[:, :n_sc].reshape((xi.shape[0], self.emf.n_phases, -1))
        alpha -= np.amax(alpha, axis=-1, keepdims=True)
        too_small = np.all(alpha < np.log(np.finfo(float).tiny), axis=-1)
        n_underflow = np.sum(too_small)
        if n_underflow > 0:
            logger.warning(f'scenario_prob: {n_underflow} alpha samples too small. '
                           + 'Should not happen. Maybe too few responses?')
            logger.debug(f'alpha[too_small, :] = {alpha[too_small]}')
        u = np.exp(alpha)
        # avoid nan after normalization, should not be needed !
        u /= np.sum(u, axis=-1, keepdims=True)
        return u.reshape((-1, *self.emf.scenario_shape))

    def attribute_theta(self, xi, a):
        """Extract location of latent sensory variable, for given attribute
        :param xi: 2D array with parameter sample vectors
            xi[s, :] = s-th parameter sample vector
        :param a: attribute key = one of self.emf.attribute_grades.keys()
        :return: theta = mD array, with
            theta[s, k0, k1, ...] = s-th sample of
                attribute location, given the (k0, k1, ...)-th scenario.
        """
        a_slice = self.attribute_slice_dict[a]
        beta = xi[..., a_slice][..., :self.n_beta]
        return np.dot(beta, self.theta_map).reshape((-1, *self.emf.scenario_shape))

    def attribute_tau(self, xi, a):
        """Extract response thresholds for given attribute
        :param xi: 2D array with parameter sample vectors
            xi[s, :] = s-th parameter sample vector
        :param a: attribute key = one of self.emf.attribute_grades.keys()
        :return: tau = mD array, with
            tau[s, l] = s-th sample of UPPER limit of l-th response interval,
                EXCEPT the last at +inf
                tau.shape[-1] == len(self.emf.attribute_grades[a]) - 1
        """
        a_slice = self.attribute_slice_dict[a]
        eta = xi[..., a_slice][..., self.n_beta:]
        return response_thresholds(eta)[..., 1:-1]


# ---------------------------------------- General module functions:

def response_thresholds(eta):
    """Transform given log-category-width parameters to response thresholds.
    :param eta: = 1D or 2D array with
        eta[..., m] = ...-th sample of parameter defining
            non-normalized width of m-th interval in mapped domain [0, 1].
        eta.shape[-1] == M == number of response-scale intervals.
    :return: tau = 1D or 2D array, with all elements in [-inf, +inf]
        (tau[..., m], tau[..., m+1] = (LOWER, UPPER) limits for m-th ordinal response interval
        tau[..., 0] ==  - np.inf
        tau[..., -1] == + np.inf
        tau.ndim == eta.ndim; tau.shape[-1] == eta.shape[-1] + 1

    Method:
        Normalized widths and interval limits are defined in transformed domain [0, 1.],
        using a logistic mapping function of actual thresholds tau:
        y = expit(tau), where y in [0, 1],
            y[..., 0] = 0.
            y[..., m+1] =  (w_0 +...+ w_m) / (w_0 + ... + w_{M-1};  0 <= m <= M-1
        Thus, thresholds are calculated with the inverse transform
        tau = logit(y)
        w_m = _w(eta[..., m]) is a monotonic function of eta, always > 0
    """
    # w = _w(eta) = non-normalized width of transformed intervals, always > 0
    cum_w = np.cumsum(mapped_width(eta), axis=-1)
    z_shape = (*cum_w.shape[:-1], 1)
    cum_w = np.concatenate((np.zeros(z_shape), cum_w),
                           axis=-1)
    # sum_w = cum_w[..., -1:]
    # *** check for too small intervals in [0,1] domain here ? ******
    return logit(cum_w / cum_w[..., -1:])
    # min_tau = np.amin(tau[..., 1:-1])
    # max_tau = np.amax(tau[..., 1:-1])
    # if min_tau < -37. or max_tau > 30.:
    #     print(f'response_threshold: min, max tau = {min_tau:.3f}, {max_tau:.3f}')
    # return tau


def d_response_thresholds(eta):
    """Jacobian of cat_limits with respect to eta
    :param eta: 1D or 2D array (called eta in Leijon doc), with
        eta[..., m] = ...-th sample of log non-normalized width of m-th interval,
        eta.shape[-1] = M = number of response intervals
    :return: 2D or 3D array d_tau, with
        d_tau[..., m, i] = d tau[..., m] / d eta[..., i]; m = 0,..., M-2; i = 0, ..., M-1
            where (tau[s, m], tau[s, m+1] = (LOWER, UPPER) limits of m-th response interval
        d_tau[..., 0, :] = d_tau[..., -1, :] = 0.; for extreme limits at +-inf
        d_tau.shape == (N, M+1, M); (N, M) = eta.shape

    2022-06-07, tested OK
    """
    w = mapped_width(eta)
    # (n_samples, nw) = w.shape
    nw = w.shape[-1]
    cum_w = np.cumsum(w, axis=-1)
    cw = cum_w[..., :-1, np.newaxis]  # only inner limits
    sw = cum_w[..., -1:, np.newaxis]
    # tau[..., m+1] = ln cw[..., m]  - ln (sw[..., 0] - cw[..., m])
    # dcw_dw[..., m, i] = dcw[..., m] / dw[..., i]  = 1. if i <= m else 0.
    dcw_dw = np.tril(np.ones((nw - 1, nw), dtype=int))
    dtau_dw = dcw_dw / cw - (1 - dcw_dw) / (sw - cw)
    dtau_d_eta = dtau_dw * d_mapped_width_d_eta(w)[..., np.newaxis, :]
    # dtau_d_eta.shape = (n_samples, nw + 1, nw)  OR (nw + 1, nw)
    z_shape = list(dtau_d_eta.shape)
    z_shape[-2] = 1
    return np.concatenate((np.zeros(z_shape),  # *** use np.pad ???
                           dtau_d_eta,
                           np.zeros(z_shape)), axis=-2)


def tau_inv(tau):
    """Inverse of response_thresholds(eta)
    :param tau: 1D or 2D array with response thresholds, EXCEPT extremes at +-inf,
        i.e., all tau elements in (-inf, +inf),
        tau[..., m] = UPPER limit for m-th interval,
            = LOWER limit for the (m+1)-th interval
        tau.shape[-1] == M - 1 == number of response intervals - 1
    :return: eta: 1D or 2D array with
        eta[..., m] = ...-th sample of log non-normalized width of m-th interval.
        eta.shape[-1] == M == number of response intervals.

    Method:
        Normalized widths and interval limits are defined in transformed domain (0, 1.),
        using a logistic mapping function,
        y = expit(tau), where y in (0, 1]
            y[..., m] =  (w_0 +...+ w_m) / (w_0 + ... + w_{M-1};  0 <= m <= M-1
            w_m = _w(eta[..., m])
    """
    y = expit(tau)
    cat_shape = (*y.shape[:-1], 1)
    # include extreme limits at 0 and 1:
    y = np.concatenate((np.zeros(cat_shape),
                        y,
                        np.ones(cat_shape)), axis=-1)
    w = np.diff(y, axis=-1)
    return mapped_width_inv(w)


# ----------- Original up to version 0.9.1 -> numeric overflow in some extreme cases
# _w = np.exp  # _w(eta) -> non-normalized interval widths in (0, 1) domain
# _w_inv = np.log  # _w_inv(w) -> eta, such that _w(eta) == w
#
#
# def _dw_d_eta(w):
#     """Derivative of _w, , as a function of w, NOT eta
#     :param w: = _w(eta) = 1D or 2D array
#     :return: array dw, with
#         dw[..., m] = d _w(eta)[..., m] / d eta[..., m]
#     """
#     return w

# ---------- *** exponential variant 2022-06-12
# works OK as long as eta values <-> sum(_w(eta)) == 1.

def mapped_width(eta):  # ***** renamed from _w(eta)
    """Mapping function from model eta param to
    non-normalized interval widths in (0, 1) range
    :param eta: = 1D or 2D array with
        eta[..., m] = ...-th sample of parameter defining
            non-normalized width of m-th interval in mapped domain [0, 1].
        eta.shape[-1] == M == number of response-scale intervals.
    :return: w = array with mapped widths
        w.shape == eta.shape
    """
    return np.exp(eta) + ETA_W_EPSILON


def d_mapped_width_d_eta(w):
    """Derivative of _w, , as a function of w, NOT eta.
    Must be consistent with _w().
    :param w: = _w(eta) = 1D or 2D array
    :return: array dw, with
        dw[..., m] = d _w(eta)[..., m] / d eta[..., m]
    """
    return w - ETA_W_EPSILON


def mapped_width_inv(w):
    """Inverse of mapped_width(eta),
    used only after each VI iteration,
    so it is OK to be slightly inconsistent with mapped_width()
    :param w: = 1D or 2D array with
        w[..., m] = ...-th sample of
            non-normalized width of m-th interval in mapped domain [0, 1].
        sum_m w[..., m] approx == 1.
        w.shape[-1] == M == number of response-scale intervals.
    :return: eta = array with mapped widths mapped back to eta parameter
        eta.shape == w.shape
    """
    return np.log(w + np.finfo(float).tiny)
    # adjust eta -> roughly symmetric around zero -> higher prior log-pdf ? NO, keep sum(w) == 1.
    # return eta  # - np.median(eta, axis=-1, keepdims=True)


# ---------- *** piecewise (exp, linear ) variant, tested no good
# def _w(eta):
#     """Mapping function from model eta param to
#     non-normalized interval widths in (0, 1) range
#     :param eta: = 1D or 2D array with
#         eta[..., m] = ...-th sample of parameter defining
#             non-normalized width of m-th interval in mapped domain [0, 1].
#         eta.shape[-1] == M == number of response-scale intervals.
#     :return: w = array with mapped widths
#         w.shape == eta.shape
#
#     Method: Trying continous exp and linear function
#     """
#     w = 1. + eta
#     neg = eta < 0.
#     w[neg] = np.exp(eta[neg])
#     return w

# def _w_inv(w):
#     """Inverse of _w(eta)
#     :param w: = 1D or 2D array with
#         w[..., m] = ...-th sample of
#             non-normalized width of m-th interval in mapped domain [0, 1].
#         w.shape[-1] == M == number of response-scale intervals.
#     :return: eta = array with mapped widths mapped back to eta parameter
#         eta.shape == w.shape
#     """
#     eta = w - 1.  # only for non-negative eta
#     neg = eta < 0.
#     eta[neg] = np.log(w[neg])
#     return eta

# def _dw_d_eta(w):
#     """Derivative of _w, , as a function of w, NOT eta
#     :param w: = _w(eta) = 1D or 2D array
#     :return: array dw, with
#         dw[..., m] = d _w(eta)[..., m] / d eta[..., m]
#     """
#     dw = np.ones_like(w)  # = 1, for w ge 1, eta ge 0.
#     neg = w < 1.
#     dw[neg] = w[neg]
#     return dw


# ------------- piecewise (inverted linear, linear ) variant, tested no good
# def _w(eta):
#     """Mapping function from model eta param to
#     non-normalized interval widths in (0, 1) range
#     :param eta: = 1D or 2D array with
#         eta[..., m] = ...-th sample of parameter defining
#             non-normalized width of m-th interval in mapped domain [0, 1].
#         eta.shape[-1] == M == number of response-scale intervals.
#     :return: w = array with mapped widths
#         w.shape == eta.shape
#     """
#     w = 1. + eta
#     neg = eta < 0.
#     w[neg] = 1. / (1. - eta[neg])
#     return w
#
#
# def _w_inv(w):
#     """Inverse of _w(eta)
#     :param w: = 1D or 2D array with
#         w[..., m] = ...-th sample of
#             non-normalized width of m-th interval in mapped domain [0, 1].
#         w.shape[-1] == M == number of response-scale intervals.
#     :return: eta = array with mapped widths mapped back to eta parameter
#         eta.shape == w.shape
#     """
#     # *** scale w to get eta more symmetric around 0
#     s = np.median(w, axis=-1, keepdims=True)
#     # *** or s = median w ?
#     w = w / s
#     eta = w - 1.  # only for non-negative eta
#     neg = eta < 0.
#     eta[neg] = 1. - 1. / w[neg]
#     return eta
#
#
# def _dw_d_eta(w):
#     """Derivative of _w, , as a function of w, NOT eta
#     :param w: = _w(eta) = 1D or 2D array
#     :return: array dw, with
#         dw[..., m] = d _w(eta)[..., m] / d eta[..., m]
#     """
#     dw = np.ones_like(w)  # = 1, for w ge 1, eta ge 0.
#     neg = w < 1.
#     dw[neg] = w[neg]**2
#     return dw


def _make_prior(n_parameters, n_beta,
                scenario_slices,
                attribute_slices, rv_class):
    """Create hyperprior for parameter distribution in the total population
    :param n_parameters: total number of parameters
    :param scenario_slices: list with index slice for each Scenario phase
    :param attribute_slices: list with index slice for each attribute
    :param n_beta: number of regression-effect parameters for each attribute
    :return: single GaussianRV instance
    """
    prec_a = PRIOR_PREC_A  # ***** scalar, same for all elements
    prec_b = PRIOR_PREC_B * np.ones(n_parameters)
    for a_slice in attribute_slices:
        prec_b[a_slice][:n_beta] *= rv_class.scale**2
    loc = np.zeros(n_parameters)
    for sc_slice in scenario_slices:
        loc[sc_slice] = - np.log(sc_slice.stop - sc_slice.start)
    return GaussianRV.initialize(loc=loc,
                                 learned_weight=PRIOR_PSEUDO_RESPONDENT,
                                 prec_a=prec_a,
                                 prec_b=prec_b)


def _check_effects(emf, effects):
    """Check that all effects refer to unique scenario keys
    :param emf: ema_data.EmaFrame instance
    :param effects: iterable with regression-effect specifications
        effects[i] = single key in emf.scenarios.keys(), OR tuple of such keys
    :return: None
    Result: raise RuntimeError if incorrect effects
    """
    effect_keys = sum((list(e_i) if type(e_i) is tuple else [e_i]
                      for e_i in effects), start=[])
    if len(set(effect_keys)) != len(effect_keys):
        raise RuntimeError('scenario keys can occur only ONCE in regression effects')
    # *** Check no effect of scenario dimension with only ONE category
    for sc in emf.scenarios.keys():
        if len(emf.scenarios[sc].categories) > 1 and sc not in effect_keys:
            logger.warning(f'Scenario dim {repr(sc)} to be disregarded in regression?')
    for e_i in effect_keys:
        if e_i not in emf.scenarios.keys():
            raise RuntimeError(f'regression effect key {e_i} is not a scenario key')


def _make_slices(lengths, start=0):
    """Create a sequence of consecutive index slices, with given lengths
    :param lengths: sequence with desired slice sizes
    :param start: (optional) start index of first slice
    :return: slice_list; len(slice_list) == len(l)
    """
    slice_list = []
    for l_i in lengths:
        slice_list.append(slice(start, start + l_i))
        start += l_i
    return slice_list


def _theta_map(emf, effects):
    """Create 2D array for extraction of attribute locations
    from parameter vector samples
    :param emf: ema_data.EmaFrame instance,
        defining the analysis model structure.
    :param effects: iterable with regression-effect specifications
        effects[i] = tuple with one or more key(s) from emf.scenarios.keys()
    :return: th = 2D binary array, with
        th[j, k] = 1, IFF parameter
        beta[:, j] = xi[:, attr_slice][:, j]
        is the regression effect of k-th <=> (k0, k1, ...)-th scenario on attribute location theta,
        and xi is a 2D array of row parameter-vector samples.
    """
    def theta_one(effect):
        """Make theta_map part for ONE effect term
        :param effect: tuple of one or more scenario keys
        :return: mD array th, with
            th[j, k0, k1, ...] = j-th effect given (k0, k1, ...)-th scenario
            th[j, 0, 0, ...] = 0, in 0-th reference scenario.
            th.shape == (size_effect, *emf.scenario_shape), where
            size_effect = size of category array defined by effect.
        """
        beta_shape = tuple(len(emf.scenarios[sc_i].categories) for sc_i in effect)
        # = scenario_shape, for this effect term
        beta_ndim = len(beta_shape)
        beta_size = int(np.prod(beta_shape))
        t = np.eye(beta_size).reshape((beta_size, *beta_shape))
        if effect != effects[0]:  # **** version 0.6 ???
            t = t[1:]
            # fixed effect beta[0] for all additional effect terms, EXCEPT FIRST
            # -> ONE overall theta intercept parameter across all effect terms
        # expand t.ndim to emf.scenario.ndim:
        t = t.reshape(t.shape + tuple(np.ones(len(emf.scenarios) - beta_ndim,
                                              dtype=int)
                                      ))
        ax_0 = range(1, 1 + len(beta_shape))
        ax_new = tuple(list(emf.scenarios).index(e_i) + 1
                       for e_i in effect)
        t = np.moveaxis(t, ax_0, ax_new)
        return t + np.zeros(emf.scenario_shape)
    # ---------------------------------------------------------------
    th = np.concatenate([theta_one(e_tuple)
                         for e_tuple in effects],
                        axis=0)
    return th.reshape((th.shape[0], -1))  # keep as 2D for simplicity


# ------------------------------------------------- TEST:
if __name__ == '__main__':
    from scipy.optimize import approx_fprime, check_grad

    from ema_data import EmaFrame
    from ema_latent import Bradley

    print('*** Testing some ema_base module functions ')
    emf = EmaFrame(scenarios={'CoSS': [f'{i}.' for i in range(1, 8)],
                              'Viktigt': ('Lite',
                                          'Ganska',
                                          'Mycket'),
                              # 'Test': (None, None),
                              'HA': ('A', 'B')
                              },  # nominal variables
                   # phase_key='Phase',
                   attribute_grades={'Speech': ('Svårt',
                                                'Normalt',
                                                'Lätt'),
                                     'Quality': ('Bad', 'Good')
                                     },  # ordinal variables
                   )

    # print('emf=\n', emf)

    main_theta = {'Phase': [0.],
                  'CoSS': 0.1 * np.arange(len(emf.scenarios['CoSS'].categories)),
                  'Viktigt': np.array([-1., 0., 1.]),
                  'HA': np.array([0., 1.])
                  }
    # = only main effects, additive
    regr_effects = ['HA', ('CoSS', 'Viktigt')]

    # effect_HA = np.array([-1., 1.])
    # effect_CoSS = 0.1 * np.arange(len(emf.scenarios['CoSS']))
    # effect_Vikt = np.array([-1., 0., 1.])
    true_theta = main_theta['CoSS'][:, None] + main_theta['Viktigt']
    true_theta = true_theta[..., None] + main_theta['HA']
    true_theta = true_theta[None, ...]  # only one phase
    # stored like emf.scenarios

    beta_HA = main_theta['HA'][1:] - main_theta['HA'][0]
    # beta_CoSS = effect_CoSS[1:] - effect_CoSS[0]
    # beta_Vikt = effect_Vikt[1:] - effect_Vikt[0]
    beta_CoSS_Vikt = main_theta['CoSS'][:, None] + main_theta['Viktigt']
    beta_all = np.concatenate((beta_HA, beta_CoSS_Vikt.reshape((-1)), ))

    eta = [np.zeros(len(r_cat.categories))
           for r_cat in emf.attribute_grades.values()]

    lp_scenarios = np.zeros(emf.scenario_shape).reshape((-1))
    beta_eta = [np.concatenate((beta_all, eta_r))
                for eta_r in eta]
    print(f'len(beta_eta): ', [len(be_i) for be_i in beta_eta])

    xi = np.concatenate((lp_scenarios, *beta_eta))
    xi = xi[None, :]

    # p_base = EmaParamBase()
    p_base = EmaParamBase.initialize(emf, regr_effects, rv_class=Bradley)
    print('p_base= ', p_base)
    print(f'p_base.emf=\n{p_base.emf}')
    print(f'p_base.effects= {p_base.effects}')
    print('p_base.scenario_slices', p_base.scenario_slices)
    print('p_base.attribute_slices', p_base.attribute_slices)
    print('p_base.n_parameters= ', p_base.n_parameters)
    print('p_base.n_beta= ', p_base.n_beta)
    print('p_base.theta_map.shape= ', p_base.theta_map.shape)
    print('p_base.comp_prior= ', p_base.comp_prior)

    print('\n*** Testing param extraction methods ***')

    for (phase, alpha_slice) in zip(emf.scenarios[emf.phase_key].categories,
                                    p_base.scenario_slices):
        print(f'{emf.phase_key}= {phase}: xi[:, alpha_slice].shape= ', xi[:, alpha_slice].shape)
    # for (phase, alpha) in zip(emf.scenarios[emf.phase_key], p_base.scenario_logprob(xi)):
    #     print(f'{emf.phase_key}= {phase}: prob-mass=\n', np.exp(alpha))
    print(f'\nemf.scenario_shape= {emf.scenario_shape}')
    for (a, a_slice) in zip(emf.attribute_grades.keys(), p_base.attribute_slices):
        print(f'\nAttribute {a}.slice: {a_slice}')
        print(f'\nAttribute {a}: xi[:, a_slice]={xi[:, a_slice]}')

    for a in emf.attribute_grades.keys():
        theta = p_base.attribute_theta(xi, a)
        print(f'\nAttribute {a}: theta.shape={theta.shape}.')
        sc_dim_0 = 'Phase'
        sc_dim_1 = 'CoSS'
        theta = theta.reshape((-1, *emf.scenario_shape))  # *** just for testing
        for (sc_0, theta_0, true_theta_0) in zip(emf.scenarios[sc_dim_0].categories,
                                                 theta[0], true_theta):
            print(f'\t{sc_dim_0}= {sc_0}:')
            for (sc_1, theta_1, true_theta_1) in zip(emf.scenarios[sc_dim_1].categories,
                                                     theta_0, true_theta_0):
                print(f'\t\t{sc_dim_1}= {sc_1}: theta=\n', theta_1)
                print(f'\t\t{sc_dim_1}= {sc_1}: true_theta=\n', true_theta_1)

    for a in emf.attribute_grades.keys():
        tau = p_base.attribute_tau(xi, a)
        print(f'\nAttribute {a}: tau.shape={tau.shape}. tau=\n', tau)

    print('\n*** Testing response_thresholds() and tau_inv() ***')

    eta = np.arange(4) - 50.
    eta = np.array([0., 0., -1., -50., -50.])
    tau = response_thresholds(eta)
    print(f'eta = ', eta)
    print(f'_w(eta) = ', mapped_width(eta))
    print(f'tau({eta}) = ', tau)
    print(f'tau_inv(tau[1:-1] = ', tau_inv(tau[1:-1]))
    print(f'tau(tau_inv(tau[1:-1]) = ', response_thresholds(tau_inv(tau[1:-1])))

    # ----- **** check extreme tau, that might occur in restrict_xi ************
    tau = np.array([-np.inf, -100., 0., 0., 100., np.inf])
    print(f'tau = ', tau)
    print(f'tau_inv(tau[1:-1] = ', tau_inv(tau[1:-1]))
    print(f'tau(tau_inv(tau[1:-1]) = ', response_thresholds(tau_inv(tau[1:-1])))

    print('\n*** Testing d_response_thresholds gradient functions ***')

    eta = np.arange(4) - 50.
    eta = np.array([0., 0., -1., -50., -50.])
    limit = 1

    def fun(eta):
        return response_thresholds(eta.reshape((1, -1)))[0, limit]

    def jac(eta):
        return d_response_thresholds(eta.reshape((1, -1)))[0, limit]

    print(f'tau(eta) = {response_thresholds(eta.reshape((1, -1)))}')
    # print(f'tau(eta+d) = {response_thresholds(eta.reshape((1, -1)) + .1)} Should remain the same')

    print('approx gradient = ', approx_fprime(eta, fun, epsilon=1e-6))
    print('exact  gradient = ', jac(eta))
    err = check_grad(fun, jac, eta, epsilon=1e-6)
    print('check_grad err = ', err)

