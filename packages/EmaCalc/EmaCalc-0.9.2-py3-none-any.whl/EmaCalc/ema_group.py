"""This module defines classes for a Bayesian probabilistic model of EMA data,
for ONE group of respondents representing ONE population.

*** Class Overview:

EmaGroupModel: Container for individual response-probability models,
    as implemented by an ema_subject.EmaSubjectModel instance for each subject
    in ONE group of test subjects, assumed recruited from the SAME population.
    Also contains a PopulationModel instance representing the population
    from which the subjects were recruited.

PopulationModel: Defines a Gaussian Mixture Model (GMM)
    for the parameter distribution in ONE population,
    from which subjects in ONE group were recruited.
    Part of EmaGroupModel, used as prior for all subjects in this group.

PredictivePopulationModel: marginal distribution of parameters
    in ONE population represented by ONE EmaGroupModel.
    Specifies a mixture of Student-t distributions,
    used for result displays.

*** Version History:
* Version 0.8.3:
2022-03-07, changed class name GroupModel -> EmaGroupModel
2022-03-07, changed class name ProfileMixtureModel -> PredictivePopulationModel
2022-03-07, separate class for GMM: EmaGroupModel.pop_gmm = a PopulationModel instance

* Version 0.8.2:
2022-03-03, allow multi-processing Pool in EmaGroupModel.adapt, parallel across subjects
# ****** Pool sub-processing seems to work! But need change in IndividalModel.prior ref ******
2022-03-02, test prepare to allow multiprocesing Pool.imap
            allow multi-processing Pool in EmaGroupModel.adapt, parallel across subjects

* Version 0.8.1
2022-02-26, complete separate GMM for each group, GMM components -> EmaGroupModel property comp
"""
# *** test multiprocessing start method fork? Does not work in windows ! *********
# *** try using shared_memory or Ray to reduce multiprocessing overhead?
import copy
import logging
import os
from multiprocessing.pool import Pool

import numpy as np
from scipy.special import logsumexp, softmax

from EmaCalc.dirichlet_point import DirichletVector
from EmaCalc.dirichlet_point import JEFFREYS_CONC
from EmaCalc.ema_subject import EmaSubjectModel

MixtureWeight = DirichletVector

# -------------------------------------------------------------------
__ModelVersion__ = "2022-03-08"

PRIOR_MIXTURE_CONC = JEFFREYS_CONC
# = prior conc for sub-population mixture weights.

N_SAMPLES = 1000
# = number of parameter vector samples in each EmaSubjectModel instance

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # *** TEST

usePool = True
# usePool = False # for TEST
# multi-processing speeds up the learning, but the Pool causes some overhead,
# so the time reduction is only about a factor 2 with 4 CPU cores.


# -------------------------------------------------------------------
class EmaGroupModel:
    """Container for EmaSubjectModel instances for all test subjects
    in ONE group of respondents,
    and a PopulationModel instance defining
    a Gaussian Mixture Model (GMM) for the parameter distribution in
    the population from which subjects were recruited.
    The GMM is prior for the parameter distribution in all EmaSubjectModel instances.
    """
    # *** use subject = list; subject_id as property of EmaSubjectModel ? ********
    def __init__(self, base, subjects, pop_gmm):
        """
        :param base: single common EmaParamBase object, used by all model parts
        :param subjects: dict with (subject_id, EmaSubjectModel) elements
        :param pop_gmm: a PopulationModel instance representing a Gaussian Mixture Model (GMM)
            for the parameter distribution in the population from which subjects were recruited.
        """
        self.base = base
        self.subjects = subjects
        self.pop_gmm = pop_gmm
        for s in self.subjects.values():
            s.prior = self.pop_gmm

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                f'\n\tsubjects= {len(self.subjects)} individuals,' +
                f'\n\tpop_gmm={repr(self.pop_gmm)})'
                )

    @classmethod
    def initialize(cls, max_n_comp, base, group_data, seed_seq, rng):
        """Crude initial group model given group EMA data
        :param max_n_comp: integer number of GMM components
        :param base: single common EmaParamBase object, used by all model parts
        :param group_data: a dict with elements (s_id, s_ema), where
            s_id = a subject key,
            s_ema = Pandas.DataFrame with EMA records from an ema_data.EmaDataSet object.
        :param seed_seq: SeedSequence object to spawn children for subjects of this group
        :param rng: random Generator for this group, used by self.pop_gmm
        :return: a cls instance crudely initialized
        """
        subject_rng_list = [np.random.default_rng(s)
                            for s in seed_seq.spawn(len(group_data))]  # -> gen.expr ?
        s_models = {s_id: EmaSubjectModel.initialize(base, s_ema, s_rng, id=s_id)
                    for ((s_id, s_ema), s_rng) in zip(group_data.items(),
                                                      subject_rng_list)}
        n_subjects = len(s_models)
        if max_n_comp is None:
            max_n_comp = n_subjects // 2
        else:
            max_n_comp = min(n_subjects // 2, max_n_comp)
        pop_gmm = PopulationModel.initialize(max_n_comp, s_models, base, rng)
        return cls(base, s_models, pop_gmm)  # , rng)

    def adapt(self, g_name):
        """One VI adaptation step for all model parameters
        :param g_name: group id label for logger output
        :return: ll = scalar VI lower bound to data log-likelihood,
            incl. negative contributions for parameter KLdiv re priors

        NOTE: All contributions to VI log-likelihood
        are calculated AFTER all updates of factorized parameter distributions
        because all must use the SAME parameter distribution
        """
        ll_pop_gmm = self.pop_gmm.adapt(g_name, self.subjects)
        # = -KLdiv{ q(mix_weight) || prior.mix_weight}
        #   sum_m -KLdiv(current q(mu_m, Lambda_m) || prior(mu_m, Lambda_m))

        # *** allow multiprocessing across subjects in parallel
        if usePool:
            n_pool = _pool_size(len(self.subjects))
            ch_size = len(self.subjects) // n_pool
            # ****** check time ! ********************
            if n_pool * ch_size < len(self.subjects):
                ch_size += 1
            logger.debug(f'adapt Pool: n_pool= {n_pool}, ch_size= {ch_size}')
            # ***** Find other way to access subject.xi from sub-process._sampler ??? *******
            with Pool(n_pool) as p:
                self.subjects = dict(p.imap(_adapt_subject, self.subjects.items(),
                                            chunksize=ch_size))
                # ******* send self.pop_gmm as argument to _adapt_subject ??? ******
                # if so, MUST delete the copy in sub-process! Maybe pickling takes longer time? ***
                for s in self.subjects.values():
                    s.prior = self.pop_gmm  # MUST restore link in sub-processed object
        else:
            self.subjects = dict(map(_adapt_subject, self.subjects.items()))
        ll_subjects = sum(s_model.ll for s_model in self.subjects.values())
        # = sum <ln p(data | xi)> + <ln prior p(xi | comp)> - <ln q(xi)>
        #           - KLdiv(q(zeta | xi) || p(zeta | self.mix_weight)
        #  All ll contributions now calculated using the current updated q() distributions
        logger.debug(f'Group {repr(g_name)}: '
                     + f'\n\tll_pop_gmm = {ll_pop_gmm:.3f}'
                     + f'\n\tsubject sum ll_xi= {ll_subjects:.3f}')
        return ll_pop_gmm + ll_subjects

    def prune(self, g_name, min_weight=JEFFREYS_CONC):
        """Prune model to keep only active mixture components
        :param g_name: group label for logger output
        :param min_weight: scalar, smallest accepted value for sum individual weight
        :return: None
        Result: all model components pruned consistently
        """
        w_sum = np.sum([np.mean(self.pop_gmm.mean_conditional_zeta(s.xi), axis=-1)
                        for s in self.subjects.values()],
                       axis=0, keepdims=False)
        # = sum of mean individual mixture weights, given xi
        logger.debug(f'{repr(g_name)}: Before pruning: w_sum = '
                     + np.array2string(w_sum, precision=2, suppress_small=True))
        if np.any(np.logical_and(min_weight < w_sum, w_sum <= 1.5)):
            logger.warning(f'{repr(g_name)}: *** Some component(s) with only ONE member.')
        keep = min_weight < w_sum
        self.pop_gmm.prune(keep)
        logger.info(f'{repr(g_name)}: Model pruned to {np.sum(keep)} active mixture component(s) '
                    + f'out of initially {len(keep)}')
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'{repr(g_name)}.pop_gmm.mean_zeta=\n\t'
                         + '\n\t'.join((s_name + ': '
                                        + np.array_str(np.mean(self.pop_gmm.mean_conditional_zeta(s_model.xi),
                                                               axis=-1),
                                                       precision=2,
                                                       suppress_small=True)
                                        for (s_name, s_model) in self.subjects.items())))

    # ---------------------------- make final results for display:
    def predictive_population_ind(self):
        """Predictive probability-distribution for
        sub-population represented by self
        :return: a PredictivePopulationModel object

        Method: report eq:PredictiveSubPopulation
        """
        return self.pop_gmm.predictive_population_ind()

    def predictive_population_mean(self):
        """Predictive probability-distribution for MEAN parameter vector
        in sub-population represented by self
        :return: a PredictivePopulationModel object

        Method: report eq:PredictiveSubPopulation
        """
        return self.pop_gmm.predictive_population_mean()


# -------------------------------------------------------------------
class PopulationModel:
    """A Gaussian Mixture Model (GMM) representing the parameter distribution in
    a population of subjects from which subjects in ONE group are recruited,
    and their EMA data included in a EmaGroupModel instance.
    The GMM is Bayesian, implemented by random-variable properties
    mix_weight = a MixWeight object = Dirichlet-distributed mixture weights,
    comp = a list of gauss_gamma.GaussianRV objects.
    """
    def __init__(self, base, mix_weight, comp, rng):
        """
        :param base: single common EmaParamBase object, used by all model parts
        :param mix_weight: a single MixtureWeight(DirichletVector) instance,
            with one element for each element of base.comp
        :param comp: list of GaussianRV instances,
            each representing ONE mixture component
            for parameter vector xi, in the (sub-)population represented by self
        :param rng: random Generator instance
        """
        self.base = base
        self.mix_weight = mix_weight
        self.comp = comp
        self.rng = rng

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                f'\n\tmix_weight={repr(self.mix_weight)},'
                f'\n\tcomp= {len(self.comp)} mixture components)'
                )

    @classmethod
    def initialize(cls, max_n_comp, subjects, base, rng):
        """Crude initial group model given group EMA data
        :param max_n_comp: integer number of GMM components
        :param subjects: list with EmaSubjectModel instances for group subjects,
            only crudely initialized
        :param base: single common EmaParamBase object, used by all model parts
        :param rng: random Generator for this group
        :return: a cls instance crudely initialized
        """
        mix_weight = MixtureWeight(alpha=np.ones(max_n_comp) * PRIOR_MIXTURE_CONC,
                                   rng=rng)
        comp = [copy.deepcopy(base.comp_prior)
                for _ in range(max_n_comp)]
        self = cls(base, mix_weight, comp, rng)
        self._init_comp(subjects)
        return self

    def _init_comp(self, subjects):  # **** static, or sub-function of initialize ? *******
        """Initialize Gaussian mixture components to make them distinctly separated,
        using only initialized values for all subject.xi.
        This is a necessary starting point for VI learning.
        :param subjects: dict with (subject_id, EmaSubjectModel) elements
            only crudely initialized
        :return: None

        Method: pull self.comp elements apart by random method like k-means++
        that tends to maximize separation between components.
        Mixture weights will be adapted later in the general VI procedure.
        """
        def distance(x, c):
            """Square-distance from given samples to ONE mixture component,
            as estimated by component logpdf.
            :param x: 2D array of sample row vectors that might be drawn from c
            :param c: ONE mixture component in self.base.comp
            :return: d = 1D array with non-negative distance measures
                d[n] = distance from x[n] to c >= 0.
                len(d) == x.shape[0]
            """
            d = - c.mean_logpdf(x)
            return d - np.amin(d)

        def weight_by_dist(d):
            """Crude weight vector estimated from given distance measures
            :param d: 1D array with non-negative distances
            :return: w = 1D array with weights,
                with ONE large element randomly chosen with probability prop.to d2,
                and all other elements small and equal.
                w.shape == d.shape
            """
            w = np.full_like(d, 1. / len(d))
            # ALL samples jointly contribute with weight equiv to ONE sample
            i = self.rng.choice(len(d), p=d / sum(d))
            w[i] = len(d) / len(self.comp)
            # total weight of all samples divided uniformly across components
            # placed on the single selected i-th sample point
            return w

        # --------------------------------------------------------
        xi = np.array([np.mean(s_model.xi, axis=0)
                       for s_model in subjects.values()])
        xi2 = np.array([np.mean(s_model.xi**2, axis=0)
                        for s_model in subjects.values()])
        xi_d = np.full(len(xi), np.finfo(float).max / len(xi) / 2)
        # = very large numbers that can still be normalized to sum == 1.
        for c_i in self.comp:
            c_i.adapt(xi, xi2, w=weight_by_dist(xi_d), prior=self.base.comp_prior)
            xi_d = np.minimum(xi_d, distance(xi, c_i))
            # xi_d[n] = MIN distance from xi[n] to ALL already initialized components

    def adapt(self, g_name, subjects):
        """One VI adaptation step for all model parameters
        :param g_name: group id label for logger output
        :param subjects: dict with current (subject_id, EmaSubjectModel) elements
        :return: ll = scalar VI lower bound to data log-likelihood,
            incl. negative contributions for parameter KLdiv re priors

        NOTE: All contributions to VI log-likelihood
        are calculated AFTER all updates of factorized parameter distributions
        because all must use the SAME parameter distribution
        """
        ll_weights = self._adapt_mix_weight(subjects)
        # = -KLdiv{ q(self.mix_weight) || prior.mix_weight}
        ll_comp = self._adapt_comp(g_name, subjects)
        # ll_comp = list_m -KLdiv(current q(mu_m, Lambda_m) || prior(mu_m, Lambda_m)), for
        # q = new adapted comp, p = prior_comp model, for m-th mixture component
        # Leijon doc eq:CalcLL
        sum_ll_comp = sum(ll_comp)
        logger.debug(f'{repr(g_name)}.pop_gmm: '
                     + f'\n\tll_weights= {ll_weights:.4f} '
                     + f'\n\tmix_weight.alpha= '
                     + np.array2string(self.mix_weight.alpha,
                                       precision=2,
                                       suppress_small=True)
                     + f'\n\tcomp: -KLdiv= {sum_ll_comp: .3f} = sum'
                     + np.array_str(np.array(ll_comp),
                                    precision=2,
                                    suppress_small=True))
        return ll_weights + sum_ll_comp

    def _adapt_comp(self, g_name, subjects):
        """One VI update for all GMM components in self.comp
        :param g_name: group id label for logger output
        :param subjects: dict with current (subject_id, EmaSubjectModel) elements
        :return: ll = sum_m (-KLdiv re prior) across self.base.comp[m]
        """
        (m_zeta, m_zeta_xi, m_zeta_xi2) = ([], [], [])
        # = accumulators for <zeta>, <zeta * xi>, <zeta * xi**2>
        # for g in self.groups.values():
        for s in subjects.values():
            zeta = self.mean_conditional_zeta(s.xi)
            n_xi = s.xi.shape[0]
            # zeta[c, s] = E{zeta_c | xi[s]}
            m_zeta.append(np.mean(zeta, axis=-1))
            m_zeta_xi.append(np.dot(zeta, s.xi) / n_xi)
            m_zeta_xi2.append(np.dot(zeta, s.xi**2) / n_xi)
        # m_zeta[s][c] = < zeta_cs >_s.xi
        # m_zeta_xi[s][c, :] = < zeta_cs * s.xi >_s.xi
        # m_zeta_xi2[s][c, :] = < zeta_cs * s.xi**2 >_s.xi
        ll = [c.adapt(xi_c, xi2_c, w_c, prior=self.base.comp_prior)
              for (c, xi_c, xi2_c, w_c) in zip(self.comp,
                                               np.array(m_zeta_xi).transpose((1, 0, 2)),
                                               np.array(m_zeta_xi2).transpose((1, 0, 2)),
                                               np.array(m_zeta).T)]
        # = list of -KLdiv(comp[c] || comp_prior)
        return ll

    def _adapt_mix_weight(self, subjects):
        """One update step of properties self.mix_weight,
        :return: ll = - KLdiv(self.mix_weight || prior.mix_weight), after updated mix_weight
        """
        self.mix_weight.alpha = (np.sum([np.mean(self.mean_conditional_zeta(s.xi),
                                                 axis=1)
                                         for s in subjects.values()],
                                        axis=0)
                                 + PRIOR_MIXTURE_CONC)
        # = Leijon doc eq:PosteriorV
        prior_alpha = PRIOR_MIXTURE_CONC * np.ones(len(self.comp))
        return - self.mix_weight.relative_entropy(DirichletVector(alpha=prior_alpha))

    def prune(self, keep):
        """Prune model to keep only active mixture components
        :param keep: boolean array indicating mixture components to keep
        :return: None
        Result: all model components pruned consistently
        """
        self.mix_weight.alpha = self.mix_weight.alpha[keep]
        del_index = list(np.arange(len(keep), dtype=int)[np.logical_not(keep)])
        del_index.reverse()
        # Must delete in reverse index order to avoid IndexError
        for i in del_index:
            del self.comp[i]

    # ----------------- methods used as prior for EmaSubjectModel instances:
    def logpdf(self, xi):
        """Mean log pdf of any candidate subject parameter array,
        given current GMM defined by self.mix_weight and self.comp
        averaged across self.comp parameters and self.mix_weight
        :param xi: array with parameter sample vector(s)
            xi[..., j] = ...-th sample of j-th individual parameter,
        :return: lp = array with
            lp[...] = E_self{ln p(xi[..., :] | self)}
            lp.shape == xi.shape[:-1]

        Method: Leijon doc eq:LogProbXi, prior part
        """
        return logsumexp(self.log_responsibility(xi), axis=0)

    def d_logpdf(self, xi):
        """gradient of self.logpdf(xi) w.r.t. xi
        :param xi: 2D array with parameter sample vector(s)
            xi[..., j] = ...-th sample of j-th individual parameter,
        :return: dlp = array with
            dlp[..., j] = d log p(xi[..., :] | self) / d xi[..., j]
            lp.shape == xi.shape
        """
        return np.sum(softmax(self.log_responsibility(xi)[..., None],
                              axis=0) * self.d_log_responsibility(xi),
                      axis=0)

    def mean_conditional_zeta(self, xi):
        """Expected value of mixture-component indicator zeta,
         given any candidate subject parameter vector(s)
        :param xi: 1D or 2D array with
            xi[..., :] = ...-th parameter sample vector
         :return: w = array, normalized for sum(w) == 1.
             w[c, ...] = P{xi[..., :] generated by c-th mixture component}
             w.shape == (len(self.comp), *xi.shape[:-1])
        """
        return softmax(self.log_responsibility(xi), axis=0)

    def mean_marginal_zeta(self, xi):
        """Marginal expected value of mixture-component indicator zeta,
         given any candidate subject parameter vector(s),
         averaged across all xi samples
        :param xi: 2D array with
            xi[s, :] = s-th parameter sample vector
         :return: w = 1D array, normalized for sum(w) == 1.
             w[c] = mean_s(P{xi[s, :] generated by c-th mixture component})
             w.shape == (len(self.comp),)
        """
        return np.mean(self.mean_conditional_zeta(xi), axis=1)

    def log_responsibility(self, xi):
        """Expected log pdf for any candidate subject parameters,
        for each comp in current GMM represented by self.mix_weight and self.base.comp
        :param xi: 2D array with parameter sample vector(s)
            xi[..., j] = ...-th sample of j-th individual parameter,
        :return: lr = array with
            lr[c, ...] = E{ log P[ xi[..., :] | self.comp[c] }
            lr.shape == (len(self.comp), *xi.shape[:-1])

        Method: Leijon doc l_c(xi) from eq:LogProbXiZeta
        """
        return np.array([c.mean_logpdf(xi) + lv_c
                         for (c, lv_c) in zip(self.comp,
                                              self.mix_weight.mean_log)
                         ])

    def d_log_responsibility(self, xi):
        """Gradient of self.log_responsibility(xi) w.r.t. xi
        :param xi: 2D array with parameter sample vector(s)
            xi[..., j] = ...-th sample of j-th individual parameter,
        :return: dlr = array with
            dlr[c, ..., j] = d self.log_responsibility(xi)[c, ...] / d xi[..., j]
            dlr.shape == (len(self.comp), *xi.shape)
        """
        return np.array([c.grad_mean_logpdf(xi)
                         for c in self.comp])

    # ---------------------------- final results for display:
    def predictive_population_ind(self):
        """Predictive probability-distribution for
        sub-population represented by self
        :return: a PredictivePopulationModel object

        Method: report eq:PredictiveSubPopulation
        """
        comp = [c_m.predictive(rng=self.rng) for c_m in self.comp]
        return PredictivePopulationModel(self.base, comp, self.mix_weight.mean, self.rng)

    def predictive_population_mean(self):
        """Predictive probability-distribution for MEAN parameter vector
        in sub-population represented by self
        :return: a PredictivePopulationModel object

        Method: report eq:PredictivePopulation
        """
        comp = [c_m.mean.predictive(rng=self.rng) for c_m in self.comp]
        return PredictivePopulationModel(self.base, comp, self.mix_weight.mean, self.rng)


# ------------------------------------------------------------------
class PredictivePopulationModel:
    """Help class defining a non-Bayesian predictive mixture model
    for parameter distribution in a population,
    derived from existing trained model components
    """
    def __init__(self, base, comp, w, rng):
        """
        :param base: ref to common EmaParamBase object
        :param comp: list of predictive mixture component models
            NOT same as original base.comp
        :param w: 1D array with mixture weight values
        :param rng: random Generator instance
        """
        self.base = base
        self.comp = comp
        self.w = w
        self.rng = rng

    @property
    def mean(self):
        """Mean of parameter vector, given population mixture,
        averaged across mixture components
        and across posterior distribution of component concentration params.
        :return: 1D array
        """
        return np.dot(self.w, [c_m.mean for c_m in self.comp],
                      axes=1)

    def rvs(self, size=N_SAMPLES):
        """Generate random probability-profile samples from self
        :param size: integer number of sample vectors
        :return: xi = 2D array of parameter-vector samples
            xi[s, :] = s-th sample vector, structured as specified by self.base
        """
        n_comp = len(self.comp)
        s = self.rng.choice(n_comp, p=self.w, size=size)
        # = array of random comp indices
        ns = [np.sum(s == n) for n in range(n_comp)]
        xi = np.concatenate([c.rvs(size=n_m)
                             for (n_m, c) in zip(ns, self.comp)],
                            axis=0)
        self.rng.shuffle(xi, axis=0)
        return xi


# ------------------------------ help function for Pool multi-tasking:
def _pool_size(n):
    """Estimate number of Pool sub-processes
    :param n: total number of independent jobs to share between processes
    :return: n_processes
    """
    # NOTE: cpu_count() returns n of LOGICAL cpu cores.
    return min(os.cpu_count(), n)


# used by map or Pool().imap:
# def _adapt_subject(s_item):
#     """dispatch call to given object.adapt(...)
#     :param s_item: tuple(s_id, s_model, prior):
#     :return: tuple(s_id, s_model_adapted)
#     """
#     (s_id, s_model, prior) = s_item
#     return s_id, s_model.adapt(s_id, prior)

def _adapt_subject(s_item):
    """dispatch call to given object.adapt(...)
    :param s_item: tuple(s_id, s_model):
    :return: tuple(s_id, s_model_adapted)
    """
    (s_id, s_model) = s_item
    return s_id, s_model.adapt(s_id)
