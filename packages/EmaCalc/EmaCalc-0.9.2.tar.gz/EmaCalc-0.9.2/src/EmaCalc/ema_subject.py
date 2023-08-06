"""This module defines a class for individual subject parameter model
to be part of an ema_group.EmaGroupModel instance,
which is part the main Bayesian probabilistic model of EMA data.

Individual parameter distributions are approximated by sampling.
The population mixture model is common prior for all individuals in
the group recruited from the same population.

*** Class Defined here:

EmaSubjectModel: Distribution of individual parameter vector
    assumed to determine the observed EMA data for ONE subject,
    including, in each EMA record,
    (1) a nominal (possibly multi-dimensional) Scenario category, and
    (2) ordinal Ratings for zero, one, or more perceptual Attributes.
    The parameter distribution is represented by an array xi with many samples.

*** Version History:
* Version 0.9.2:
2022-06-15, EmaSubjectModel methods mean_attribute_grades, nap_diff deleted.
            Replaced by ema_data.EmaDataSet.(mean_attribute_table, nap_table).

2022-06-15, new _initialize_rating_eta(y); changed _initialize_rating_theta(y, eta)
            tested initial response thresholds crudely based on response counts

2022-05-21, EmaSubject.cdf_arg: check for too small response interval,
            that might cause numerical underflow in case of many missing data

* Version 0.8.3:
2022-03-08, minor cleanup logging to work in multi-processing

* Version 0.8.2: prepared for multi-processing subject adapt() in parallel processes
2022-03-03, EmaSubjectModel methods mean_zeta, mean_zeta_mom no longer needed

* Version 0.8.1: minor cleanup of comments and logger output

* Version 0.8
2022-02-12, Changed VI factorization for better approximation,
    with individual indicators conditional on parameter samples,
    defining variational q(zeta_n, xi_n) = q(zeta_n | xi_n) q(xi_n)
"""
import multiprocessing
import logging
# import warnings

import numpy as np
from scipy.optimize import minimize
from scipy.special import logit, logsumexp, softmax
from scipy.special import expit  # only for numerical test in EmaSubject.cdf_args

from samppy import hamiltonian_sampler as ham
from samppy.sample_entropy import entropy_nn_approx as entropy

from EmaCalc.dirichlet_point import JEFFREYS_CONC
# = Jeffreys prior concentration for Dirichlet distribution

from EmaCalc.ema_base import PRIOR_PARAM_SCALE
from EmaCalc.ema_base import response_thresholds, d_response_thresholds
from EmaCalc.ema_base import tau_inv  # , mapped_width_inv
# from EmaCalc.ema_nap import nap_count


# -------------------------------------------------------------------
__ModelVersion__ = "2022-06-15"

DITHER_PARAM_SCALE = 0.1 * PRIOR_PARAM_SCALE
# -> initial dithering of point-estimated individual parameters

N_SAMPLES = 1000
# = number of parameter vector samples in each EmaSubjectModel instance

logger = logging.getLogger(__name__)
# logger does NOT inherit parent handlers, when this module is running as child process
if multiprocessing.current_process().name != "MainProcess":
    # restore a formatter like ema_logging, only for console output
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('{asctime} {name}: {message}',
                                           style='{',
                                           datefmt='%H:%M:%S'))
    logger.addHandler(console)
# Might instead send the parent logger as argument to adapt() ? ***
# logger.setLevel(logging.DEBUG)  # *** TEST
# ham.logger.setLevel(logging.DEBUG)  # *** TEST sampler


# -------------------------------------------------------------------
class EmaSubjectModel:
    """Container for EMA response data for ONE respondent,
    and a sampled approximation of the individual parameter distribution,
    and corresponding mixture weights for the parameters.

    Individual parameter distributions are approximated by a large set of samples
    stored as property xi, with
    self.xi[s, :] = s-th sample vector of parameters,
    with subsets of parameter types (alpha, beta, eta) as defined in self.base.
    """
    # *** subject.name as property of EmaSubjectModel ? ********
    def __init__(self, base, scenario_count, rating_count, xi, rng, prior=None, id=''):
        """
        :param id: key to identify self, instead of group.dict key
        :param base: single common EmaParamBase object, used by all model parts
        :param scenario_count: 2D array with response counts
            scenario_count[k0, k] = number of responses
            in k-th <=> (k1, k2, ...)-th scenario category at k0-th test stage,
            using flattened index for scenario dimensions 1,2,....
            NOTE: ema_data.EmaFrame always stores test stage as first scenario dimension.
        :param rating_count: list of 2D arrays with response counts
            rating_count[i][l, k] = number of responses for i-th ATTRIBUTE,
            at l-th ordinal level, given the k-th <=> (k0, k1, k2, ...)-th scenario
        :param xi: 2D array with parameter sample vector(s)
            xi[s, j] = s-th sample of j-th individual parameter,
                concatenating parameter sub-types as defined in superclass.
        :param rng: random Generator object for sampler
        :param prior: ref to owner EmaGroupModel  *** -> arg for self.adapt() ???
        """
        self.id = id
        self.base = base
        self.scenario_count = scenario_count
        self.rating_count = rating_count
        self.xi = xi
        self._sampler = ham.HamiltonianSampler(x=self.xi,
                                               fun=self._neg_ll,
                                               jac=self._grad_neg_ll,
                                               epsilon=0.2,
                                               n_leapfrog_steps=10,     # = default
                                               min_accept_rate=0.8,     # = default
                                               max_accept_rate=0.95,    # = default
                                               rng=rng
                                               )
        # keeping sampler properties across learning iterations
        self.prior = prior
        self.ll = None  # space for log-likelihood result from self.adapt()

    def __repr__(self):
        return (self.__class__.__name__ + '('
                + '\n\tscenario_count=' + f'{self.scenario_count},'
                + '\n\trating_count=' + f'{self.rating_count},'
                + f'\n\txi= parameter array with shape {self.xi.shape}; id={id(self.xi)},'
                + f'\n\tid(prior)= {id(self.prior)},'
                + f'\n\tll= {self.ll})')

    @classmethod
    def initialize(cls, base, ema_data, rng, id=''):  # *** rng -> seed_seq ?
        """Create model from recorded data
        :param base: single common EmaParamBase object
        :param ema_data: list of ema tuples, as stored im ema_data.EmaDataSet instance
        :param rng np.random.Generator for sampler use
        :param id: key to identify self
        :return: a cls instance
        """
        z = base.emf.count_scenarios(ema_data).reshape((base.emf.n_phases, -1))
        # z[t, k] = number of EMA assessments at t-th test stage
        # in k-th <=> (k1, k2, ...)-th scenario, EXCL. k0= test stage
        y = [base.emf.count_grades(a, ema_data)
             for a in base.emf.attribute_grades.keys()]
        # y[i][l, k] = number of attribute_grades at l-th ordinal level for i-th ATTRIBUTE question
        # given k-th <=> (k0, k1, k2, ...)-th scenario (INCL. k0= test stage)
        alpha = _initialize_scenario_param(z)
        xi = list(np.ravel(alpha))
        for y_i in y:
            eta = _initialize_rating_eta(y_i)
            theta = _initialize_rating_theta(y_i, eta)
            a = base.theta_map  # .reshape((base.theta_map.shape[0], -1))  # **** needed ?
            beta = np.linalg.lstsq(a.T, theta, rcond=None)[0]
            xi.extend(np.concatenate((beta, eta)))
        xi = np.array(xi)
        # dither to N_SAMPLES:
        xi = xi + DITHER_PARAM_SCALE * rng.standard_normal(size=(N_SAMPLES, len(xi)))
        return cls(base, z, y, xi, rng, id=id)

    def _kl_div_zeta(self, prior):
        """KLdiv for indicator variables zeta re prior
        = KLdiv{q(zeta | self.xi) || p(zeta | prior.mix_weight)}
        using current variational q(xi, zeta) = q(zeta | xi) q(xi)
        :param prior: ref to EmaGroupModel instance containing self
        :return: kl = scalar E{ ln q(zeta | self.xi) - ln p(zeta | prior.mix_weight)}

        Method: Leijon doc eq:VIlowerBoundCalc
        """
        w = prior.mean_conditional_zeta(self.xi)
        # w[c, s] = E{zeta_c | self.xi[s, :]} Leijon doc eq:ProbZetaGivenXi
        return np.sum(np.mean(w * (np.log(w + np.finfo('float').tiny)  # avoid log(0.) = nan
                                   - prior.mix_weight.mean_log[:, None]),
                              axis=1))

    def adapt(self, s_name):
        """Adapt parameter distribution self.xi
        to stored EMA count data, given the current self.w
        and the current estimate of population GMM components self.base.comp.
        :param s_name: subject id, for logger output
        :return: self, to send result via map() or Pool.imap()

        Result: Updated self.xi,
            self.ll = E{ ln p(self.scenario_count, self.rating_count | self.xi) }_q(xi)
             - E{ ln q(xi) / prior_p(xi) }_q(xi)
             - KLdiv( q(zeta | xi) || p(zeta || prior.mix_weight)
        """
        # find MAP point first:  ****** -> initialize ? NO just leave it here!
        # lp_0 = - np.mean(self._neg_ll(self.xi), axis=0)  # ****** ref for test
        xi_0 = np.mean(self.xi, axis=0)
        res = minimize(fun=self._neg_ll,
                       jac=self._grad_neg_ll,
                       x0=xi_0)
        if res.success:
            xi_map = res.x.reshape((1, -1))
        else:
            raise RuntimeError(f'{s_name}: MAP search did not converge: '
                               + 'res= ' + repr(res))
        if len(self.xi) != N_SAMPLES:
            # run sampler starting from x_map
            self._sampler.x = xi_map
        else:
            # we have sampled before, start from those samples
            self._sampler.x = self.xi + xi_map - xi_0
        # **** ------------------------------------- test effect of MAP
        # lp_1 = - np.mean(self._neg_ll(self._sampler.x), axis=0)  # ***** test after MAP adjustment
        # print(f'adapt: Subj {s_name}: MAP adjustment: d_lp = {lp_1 - lp_0:.3f}')
        # -----------------------------------------------------
        self._sampler.safe_sample(n_samples=N_SAMPLES, min_steps=2)
        logger.debug(f'{self.id}: sampler.epsilon= {self._sampler.epsilon:.3f}. '
                     + f'accept_rate= {self._sampler.accept_rate:.1%}. '
                     + f'n_steps= {self._sampler.n_steps}')
        self.xi = self._sampler.x
        self.restrict_xi()

        self._sampler.U = self._sampler.potential(self._sampler.x)
        self._sampler.args = ()  # just in case a pickled prior copy was there
        lp_xi = - np.mean(self._sampler.U)  # after restrict_xi
        # lp_xi = E_xi{ ln p(data | xi) + self.prior.logpdf(xi) }
        h_xi = entropy(self.xi)
        # approx = - E{ ln q(xi) }
        kl_zeta = self._kl_div_zeta(self.prior)
        self.ll = lp_xi + h_xi - kl_zeta
        logger.debug(f'{s_name}: adapt: ll={self.ll:.3f}; '
                     + f'(lp_xi={lp_xi:.3f}; '
                     + f'h_xi= {h_xi:.3f}. '
                     + f'-kl_zeta= {-kl_zeta:.3f})')
        self.ll = lp_xi + h_xi - kl_zeta
        return self

    def restrict_xi(self):
        """Force mean(theta) -> 0, OR mean(tau) -> 0, after sampling
        for all attributes.
        :return: None
        Result: self.xi = self._sampler.x modified in place
            theta and tau samples modified by same amount
        """
        # lp_0 = np.mean(self.logprob(self.xi), axis=0)  # *** to test effect of restrict_xi
        # lp_0_prior = np.mean(self.prior.logpdf(self.xi), axis=0)  # *** to test effect of restrict_xi
        # eta_minmax = dict()  # only for TEST
        # tau_minmax = dict()  # only for TEST
        # *** restrict log scenario prob -> normalized prob:
        for sc_slice in self.base.scenario_slices:
            d = logsumexp(self.xi[:, sc_slice], axis=-1, keepdims=True)
            # logger.debug(f'xi scenario restrict d: mean={np.mean(d):.3}; std={np.std(d):.3}; '
            #              + f'max={np.amax(d):.3}; min={np.amin(d):.3}')
            self.xi[:, sc_slice] -= d
        for (a, a_slice) in self.base.attribute_slice_dict.items():
            theta = self.base.attribute_theta(self.xi, a)
            tau = self.base.attribute_tau(self.xi, a)
            if self.base.restrict_attribute:
                n_samples = self.xi.shape[0]
                d = np.mean(theta.reshape((n_samples, -1)),
                            axis=-1, keepdims=True)
            elif self.base.restrict_threshold:
                d = np.median(tau, axis=-1, keepdims=True)
            else:
                d = 0.
            # d = random offset to be zero-ed out
            n_beta_0 = self.base.beta_0_size()
            # number of beta parameters = first part of a_slice
            beta_slice = slice(a_slice.start,
                               a_slice.start + n_beta_0)
            # = beta slice for FIRST regression effect term
            self.xi[:, beta_slice] -= d
            # adjust tau
            eta = tau_inv(tau - d)
            eta_slice = slice(a_slice.start + self.base.n_beta, a_slice.stop)
            # **** method self.base.eta_slice ???
            self.xi[:, eta_slice] = eta
            # eta_minmax[a] = (np.amin(eta), np.amax(eta))  # only for TEST
            # tau_minmax[a] = (np.amin(tau-d), np.amax(tau-d))  # only for TEST
        # ------------------------ *** checking effects of restrict_xi
        # lp_1 = np.mean(self.logprob(self.xi), axis=0)
        # lp_1_prior = np.mean(self.prior.logpdf(self.xi), axis=0)
        # print(f'restrict_xi: Subj {self.id}: d_lp = {lp_1 - lp_0:.3f}. '
        #       + f'd_lp_prior = {lp_1_prior - lp_0_prior:.3f}.'
        #       + '\n eta: ' + '; '.join(f'{a}: ({eta_min:.1f}, {eta_max:.1f})'
        #                                for (a, (eta_min, eta_max)) in eta_minmax.items())  # ****
        #       + '\n tau: ' + '; '.join(f'{a}: ({tau_min:.1f}, {tau_max:.1f})'
        #                                for (a, (tau_min, tau_max)) in tau_minmax.items()))  # ****

    def _neg_ll(self, xi):
        """Objective function for self.adapt_xi
        :param xi: 1D or 2D array of candidate parameter vectors
        :return: neg_ll = scalar or 1D array
            neg_ll[...] = - ln P{ self.scenario_count, self.rating_count | xi[..., :]}
                    - ln p(xi[..., :] | prior)
            neg_ll.shape == xi.shape[:-1]
        """
        return - self.prior.logpdf(xi) - self.logprob(xi)

    def _grad_neg_ll(self, xi):
        """Gradient of self._neg_ll w.r.t. xi
        :param xi: 1D or 2D array of candidate parameter vectors
        :return: dll = scalar or 1D array
            dll[..., j] = d _neg_ll(xi[..., :]) / d xi[..., j]
            dll.shape == xi.shape
        """
        return - self.prior.d_logpdf(xi) - self.d_logprob(xi)

    def logprob(self, xi):
        """log likelihood of EMA count data, given parameters xi
        :param xi: 1D or 2D array of candidate parameter vectors
        :return: ll = scalar or 1D array
            ll[...] = ln P{ self.scenario_count, self.rating_count | xi[..., :]}
            ll.shape == xi.shape[:-1]
        """
        def scenario_logprob(sc_xi):
            """Log probability mass for scenario categories in ONE test stage
            :param sc_xi: 1D or 2D array with model parameters for ONE test stage
                = alpha = log P{scenarios}, NOT necessarily normalized
            :return: lp = 1D or 2D array with
                lp[..., k] = log P{ k-th scenario | sc_xi[..., :] }
                properly normalized, with sum_k exp(lp[:, k]) == 1.
                lp.shape == sc_xi.shape
            """
            # **** consider using log-Dirichlet here ???
            # NO, this would cause an extra layer in the hierarchy for scenarios,
            # with a log-normal distribution of concentration parameters
            # while these only indirectly determine the probabilities.
            # In the present model, the alpha params directly determine the probabilities.
            return sc_xi - logsumexp(sc_xi, axis=-1, keepdims=True)

        def rating_logprob(y_i, a_xi):
            """Log probability mass for rating categories for ONE attribute.
            :param y_i: 2D array with grade counts for this attribute
            :param a_xi: 1D or 2D array with model parameters for this attribute
            :return: lp = scalar or 1D array with
                lp[...] = log P{ all ratings for this attribute | a_xi }
            """
            # *** calc log_cdf_diff only for y_i > 0 ??? ********
            return np.einsum('lk, ...lk -> ...',  # ********* use np.tensordot ???
                             y_i, self.base.rv_class.log_cdf_diff(*self.cdf_args(a_xi))
                             )
        # def rating_logprob(y_i, a_xi):
        #     """Log probability mass for rating categories for ONE attribute.
        #     :param y_i: 2D array with grade counts for this attribute
        #     :param a_xi: 1D or 2D array with model parameters for this attribute
        #     :return: lp = scalar or 1D array with
        #                 lp[...] = log P{ all ratings for this attribute | a_xi }
        #     2022-05-24: test log_cdf_diff only for y_i > 0; NO speed improvement!
        #     """
        #     (a, b) = self.cdf_args(a_xi)
        #     use_ind = y_i > 0
        #     return np.dot(self.base.rv_class.log_cdf_diff(a[..., use_ind],
        #                                                   b[..., use_ind]),
        #                   y_i[use_ind])
        # ---------------------------------------------------------------

        ll_z = sum(np.dot(scenario_logprob(xi[..., sc_t]), z_t)
                   for (z_t, sc_t) in zip(self.scenario_count,
                                          self.base.scenario_slices))
        # z_t[k] = k-th scenario count for t-th test stage
        # sc_t = parameter slice for t-th test stage
        # *** calc rating_logprob only where y_i >0 ? *** save time ? ***
        ll_y = sum(rating_logprob(y_i, xi[..., a_i])
                   for (y_i, a_i) in zip(self.rating_count,
                                         self.base.attribute_slices))
        # ----------- any rating_logprob = -inf -> ll_y == NaN
        if np.any(np.isnan(ll_y)):
            logger.warning('EmaSubject.logprob: Some ll_y == NaN. Should never happen!')
        # y_i[l, k] = (l, k)-th count for i-th attribute rating
        # a_i = param slice for i-th attribute rating
        return ll_z + ll_y

    def d_logprob(self, xi):
        """Jacobian of self.logprob(xi)
        :param xi: 1D or 2D array with candidate parameter vectors
        :return: d_ll = 2D array
            d_ll[..., j] = d ln P{ self.scenario_count, self.attribute_grades | xi[..., :]} / d xi[..., j]
        """
        def d_scenario_logprob(sc_xi):  # ******** use count input, save RAM ?
            """Gradient of scenario_logprob for ONE test stage
            :param sc_xi: 1D or 2D array with model parameters for ONE test stage
                = alpha = log P{scenarios}, NOT necessarily normalized
            :return: dlp = 2D or 3D array with
                dlp[..., k, j]
                = d log P{ scenario_logprob()[..., k] | sc_xi[..., :] } / d sc_xi[..., j]
            """
            # lp[s, k] = sc_xi[s, k] - ln sum_i(exp(sc_xi[s, i]))
            # dlp[s, k, j] = 1(k==j) - softmax(sc_xi[s, :], axis=-1)[s, j]
            return np.eye(sc_xi.shape[-1]) - softmax(sc_xi[..., None, :], axis=-1)

        # -----------------------------------------------------------------------

        d_ll = [np.einsum('k, ...kj -> ...j',  # ******* use dot or matmul?
                          z_t, d_scenario_logprob(xi[..., sc_t]))
                for (z_t, sc_t) in zip(self.scenario_count,
                                       self.base.scenario_slices)]
        # z_t[k] = k-th count for t-th test stage
        # sc_t = parameter slice for t-th test stage
        for (y_i, a_i) in zip(self.rating_count, self.base.attribute_slices):
            # a_xi = xi[:, a_i]
            a_xi = xi[..., a_i]
            (dlp_low, dlp_high) = self.base.rv_class.d_log_cdf_diff(*self.cdf_args(a_xi))
            # append dlp_d_beta[s, j] = d rating_logprob()[s] / d xi[:, a_i][:, j]
            d_ll.append(np.einsum('...lk, lk, jk -> ...j',
                                  dlp_low + dlp_high, y_i, - self.base.theta_map))  # tensordot 2 steps?
            d_tau_d_eta = d_response_thresholds(a_xi[..., self.base.n_beta:])
            # append dlp_d_eta[..., j] = d rating_logprob()[s] / d xi[:, a_i][:, self.n_beta + j]
            d_ll.append(np.einsum('...lk, lk, ...lj -> ...j',  # *** use dot , matmul ?
                                  dlp_low, y_i, d_tau_d_eta[..., :-1, :]) +
                        np.einsum('...lk, lk, ...lj -> ...j',
                                  dlp_high, y_i, d_tau_d_eta[..., 1:, :]))
            # all d_ll[i][..., :] elements have matching shapes
        return np.concatenate(d_ll, axis=-1)

    def cdf_args(self, a_xi):
        """Extract arguments for rv_class logprob calculation
        :param a_xi: 1D or 2D array with rating-model sample for given attribute a
            a_xi[..., j] = ...-th sample of j-th rating-model parameter
        :return: tuple (arg_low, arg_high) with 2D or 3D array args for probabilistic model,
            such that
            P[ l-th response | ...-th parameter sample, k-th scenario ] =
            = rv_class.cdf(arg_high[..., l, k]) - rv_class.cdf(arg_low[..., l, k])
        """
        theta = np.dot(a_xi[..., :self.base.n_beta], self.base.theta_map)
        # theta[..., k] = ...-th sample of latent variable, given k-th scenario
        # tau_old = self.base.tau(a_xi[..., self.base.n_beta:])
        tau = response_thresholds(a_xi[..., self.base.n_beta:])
        a = tau[..., :-1, None] - theta[..., None, :]  # lower interval limits
        b = tau[..., 1:, None] - theta[..., None, :]  # upper interval limits
        # check for tiny difference b - a: *** not needed: checked in ema_latent
        # if np.any(expit(b) - expit(a) < np.finfo(float).tiny):
        #     logger.warning(f'{self.id}: a=\n' + np.array_str(a[..., 0]))
        #     logger.warning(f'{self.id}: b=\n' + np.array_str(b[..., 0]))
        return a, b

    def rvs(self, size=N_SAMPLES):
        # re-sample if size != len(self.xi) ???
        return self.xi

    # def mean_attribute_grade(self, sc=None):  # *** only for backward compat.
    #     """Average raw attribute grades
    #     :param sc: scenario key, or tuple of scenario keys for result
    #         grade counts summed across scenario dimensions NOT included in sc
    #     :return: dict with elements (a, theta), where
    #         a = attribute key, from self.emf.attribute_grades
    #         th = mD array with
    #         th[i0, i1, ...] = mean grade, given scenario
    #         (self.scenarios[sc[0]][i0], self.scenarios[sc[1]][i1], ...)
    #         aggregated across other scenario dimensions
    #
    #     NOTE: this can be calculated already by ema_data.EmaDataSet.mean_attribute_table(...)
    #     """
    #     # *** call this only for ONE given attribute at a time, like nap_diff ??? *****
    #     def mean_grade(a_count, count_axes):
    #         """Average grade for ONE attribute
    #         :param a_count: mD array with
    #             a_count[l, k0, k1, ...] = count of l-th grade, given (k0, k1, ...)-th scenario
    #         :param count_axes: tuple with a_count axes to keep in result
    #         :return: g = array with mean grades
    #             g[i0, i1, ...] = mean grade, given (i0, i1, ...)-th category
    #                 in self.attribute_rating count_axes, aggregated across other scenario axes
    #             g.shape == self.base.emf.scenario_shape
    #         """
    #         a_count = np.moveaxis(a_count, count_axes,
    #                               tuple(range(1, 1 + len(count_axes))))
    #         sum_axis = tuple(range(1 + len(count_axes), len(a_count.shape)))
    #         a_count = np.sum(a_count, axis=sum_axis)  # across all other axes
    #         grades = [1 + i for i in range(a_count.shape[0])]
    #         g = np.tensordot(grades, a_count,
    #                          axes=1)
    #         n_count = np.sum(a_count, axis=0)
    #         if np.any(n_count == 0):
    #             logger.warning('NO ratings -> undefined mean in some case(s)')
    #         with warnings.catch_warnings():
    #             warnings.simplefilter('ignore')  # suppress standard warning for div by zero
    #             return g / n_count
    #     # ----------------------------------------------------------------
    #     sc_keys = list(self.base.emf.scenarios.keys())
    #     if sc is None:
    #         sc = tuple(sc_keys)  # include all scenario dimensions
    #     if type(sc) is not tuple:
    #         sc = (sc,)  # must be a tuple
    #     sc = tuple(sc_i for sc_i in sc if sc_i in sc_keys)
    #     a_count_axes = tuple(1 + sc_keys.index(sc_i)
    #                          for sc_i in sc)
    #     return {a: mean_grade(a_count.reshape((-1, *self.base.emf.scenario_shape)),
    #                           a_count_axes)
    #             for (a, a_count) in zip(self.base.emf.attribute_grades.keys(),
    #                                     self.rating_count)}
    #
    # def nap_diff(self, attr_key, sc=None, p=0.95):  # *** only for backward compat.
    #     """NAP difference measure for grades of ONE attribute in
    #         ONE scenario dimension with EXACTLY TWO categories
    #     NOTE: This does NOT use the Bayesian model of self.
    #     Can be calculated already by method ema_data.EmaDataSet.nap_table(...)
    #     :param attr_key: single attribute key for selected result
    #     :param sc: scenario key, or tuple of scenario keys for result
    #         grade counts are summed across scenario dimensions NOT included in sc
    #         sc[0] must be scenario dimension with exactly two categories
    #     :param p: (optional) scalar confidence level
    #     :return: dict with elements (a, nap), where
    #         a = attribute key, from self.emf.attribute_grades
    #         nap = array with
    #             nap[1, ...] = point estimate(s) and
    #             nap[[0, 2], ...] = confidence interval, stored as
    #         nap[:, i1, ...] = NAP difference for scenario dimension sc[0],
    #             given (i1, ...)-th category in scenario dimension(s) sc[1, ...]
    #     """
    #     # *** return a dict for ALL attributes, like mean_attribute_grade ??? *****
    #     def nap(a_count, count_axes):
    #         """Non-overlapping Pairs (NAP) difference measure of ONE attribute
    #         in ONE scenario dimension with exactly two categories
    #         :param a_count: mD array with
    #             a_count[l, k0, k1, ...] = count of l-th grade, given (k0, k1, ...)-th scenario
    #         :param count_axes: tuple with a_count axes to keep in result
    #         :return: nap = array with mean grades
    #             nap[i1, ...] = NAP difference, given (i1, ...)-th category
    #                 in self.attribute_rating count_axes, aggregated across other scenario axes
    #             g.shape == self.base.emf.scenario_shape
    #         """
    #         a_count = np.moveaxis(a_count, count_axes,
    #                               tuple(range(1, 1 + len(count_axes))))
    #         sum_axis = tuple(range(1 + len(count_axes), len(a_count.shape)))
    #         a_count = np.sum(a_count, axis=sum_axis)  # across all other axes
    #         nap_u = nap_count(a_count[:, 1, ...], a_count[:, 0, ...], p=p)
    #         # *** calc CI for NAP result ? *********
    #         return nap_u
    #     # ----------------------------------------------------------------
    #
    #     try:
    #         attr_ind = list(self.base.emf.attribute_grades.keys()).index(attr_key)
    #         a_count = self.rating_count[attr_ind]
    #     except ValueError:
    #         logger.warning(f'Attribute {repr(attr_key)} unknown')
    #         return None
    #     sc_keys = list(self.base.emf.scenarios.keys())
    #     sc_shape = self.base.emf.scenario_shape
    #     if sc is None:
    #         try:
    #             sc = (sc_keys[sc_shape.index(2)],)
    #         except ValueError:
    #             sc = (sc_keys[0],)
    #     if type(sc) is not tuple:
    #         sc = (sc,)  # must be a tuple, not a single key
    #     sc = tuple(sc_i for sc_i in sc if sc_i in sc_keys)
    #     if len(self.base.emf.scenarios[sc[0]].categories) != 2:
    #         logger.warning('Can calculate NAP difference only between TWO Scenario categories')
    #         return dict()
    #     a_sc_ind = tuple(1 + sc_keys.index(sc_i)
    #                      for sc_i in sc)
    #     return nap(a_count.reshape((-1, *sc_shape)),
    #                a_sc_ind)


# --------------------------------------------- module help functions:
def _initialize_scenario_param(z):
    """Crude initial estimate of scenario logprob parameters
    :param z: array with scenario counts
    :return: alpha = 2D array
        alpha[t, k] = log prob of k-th scenario at t-th test stage
        alpha.shape == (z.shape[0], z[0].size)
    """
    p = z.reshape((z.shape[0], -1)) + JEFFREYS_CONC  # PRIOR_PSEUDO_RESPONDENT
    p /= np.sum(p, axis=-1, keepdims=True)
    return np.log(p)


def _initialize_rating_eta(y):
    """Crude initial estimate of threshold-defining parameters for ONE attribute question
    :param y: 2D rating_count array,
        y[l, k] = number of responses at l-th ordinal level,
        given the k-th <-> (k0, k1, ...)-th scenario category
    :return: eta = 1D array of eta parameters, defining thresholds as
        tau = ema_base.response_thresholds(eta)
        eta.shape == y.shape[:1]

    Method: set eta parameters to match observed relative freq of all rating grades
        as if theta = 0.
    OR just set all eta == 0.
    """
    # p = np.sum(y, axis=-1) + JEFFREYS_CONC
    # p /= np.sum(p)
    # return mapped_width_inv(p)
    # *** This method seems to improve the first LL,
    # but sometimes give worse or same long-term result
    return np.zeros(len(y))  # original simple method


def _initialize_rating_theta(y, eta):
    """Crude initial estimate of latent sensory variable for ONE attribute question
    :param y: 2D rating_count array,
        y[l, k] = number of responses at l-th ordinal level,
        given the k-th <-> (k0, k1, ...)-th scenario category
    :param eta: 1D array with threshold-defining parameters
    :return: theta = array of sensory-variable locations
        theta[k] = estimated location of latent variable,
        given the k-th <-> (k0, k1, ...)-th scenario category
        theta.shape == y.shape[1:]
    """
    expit_tau = expit(response_thresholds(eta))
    typical_theta = logit((expit_tau[:-1] + expit_tau[1:]) / 2)
    # = back-transformed midpoints in each response interval
    p = y + JEFFREYS_CONC  # PRIOR_PSEUDO_RESPONDENT
    p /= np.sum(p, axis=0, keepdims=True)
    theta = np.dot(typical_theta, p)
    # = typical (midpoint) locations, given y
    return theta


# ------------------------------------------------- TEST:
# if __name__ == '__main__':
#     print('*** Testing _nap_statistic ***')
#     x_count = np.array([1, 2, 3, 4, 5])
#     y_count = np.array([0, 1, 2, 3, 4])
#     print(f'NAP result = {nap_statistic(x_count, y_count)}')
#
