"""This module defines a Bayesian probabilistic model of EMA data.
The model is learned using observed EMA recordings from all subjects,
stored in an ema_data.EmaDataSet instance.

This model version uses a mixture of Gaussian distributions
for the parameter vectors in each population of respondents,
represented by one group of subjects,
with different GMMs for each population.

Individual parameter distributions are approximated by sampling.
The population mixture model is common prior for all individuals in
the group recruited from the same population.

The model can NOT use Bayesian sequential learning.
It must be trained in a single run from a single batch of EMA data,
which is usually quite sufficient for practical applications.
However, the learn(...) method can be called several times, if needed.

*** Class Overview:

EmaModel: Defines posterior distributions of scenario probabilities,
    and locations of latent variables for perceptual attribute(s),
    learned from EMA data in an ema_data.EmaDataSet instance.
    The EMA study may include data from different groups of participants,
    represented by a EmaGroupModel instance for each population / participant group.
    Each EmaGroupModel instance contains all individual response-probability models,
    as implemented by an EmaSubjectModel instance for each subject,
    assumed recruited from the SAME population.

ema_group.EmaGroupModel: Defines a GMM for ONE population,
    and contains all individual response-probability models,
    implemented by an EmaSubjectModel instance for each subject,
    in ONE group of test subjects, assumed recruited from the SAME population.

ema_subject.EmaSubjectModel: Distribution of individual parameter vector
    assumed to determine the observed EMA data for ONE subject,
    including, in each EMA record,
    (1) a nominal (possibly multi-dimensional) Scenario category, and
    (2) ordinal Ratings for zero, one, or more subjective Attributes.
    The parameter distribution is represented by an array xi with many samples.

ema_base.EmaParamBase: common properties defining
    indexing into array of parameter vectors, and
    a prior GaussianRV instance for all GMM components.

*** Model Theory: The present model is theoretically similar to
the model of the PairedCompCalc package, partly described in
A. Leijon, M. Dahlquist, and K. Smeds (2019):
Bayesian analysis of paired-comparison sound quality ratings. JASA 146(5):3174–3183.

EXCEPT for the present use of a mixture model for the population(s).

Detailed math documentation is presented in
A Leijon et al. (2022):
Bayesian Analysis of Ecological Momentary Assessment (EMA) Data in python
Journal manuscript in preparation 2022-xx-xx

*** Version History:
* Version 0.8.3:
2022-03-08, minor cleanup

* Version 0.8.1
2022-02-26, cleanup logger output, cleanup comments
2022-02-26, class def EmaGroupModel -> module ema_group, EmaSubjectModel -> ema_subject
2022-02-26, complete separate GMM for each group, GMM components -> EmaGroupModel property comp

* Version 0.8
2022-02-12, Changed VI factorization for better approximation,
    with individual indicators conditional on parameter samples,
    defining variational q(zeta_n, xi_n) = q(zeta_n | xi_n) q(xi_n)

* Version 0.7.2
2022-01-31, Different random Generator for each EmaSubjectModel sampler, spawned from same seed

* Version 0.7.1
2022-01-30, NO module-global random Generator object here
2022-01-30, seed input to EmaModel.initialize, for reproducible results
2022-01-29, random.Generator argument to EmaSubjectModel.initialize
2022-01-11, minor update EmaSubjectModel.adapt_xi, restrict_xi

* Version 0.7:
2021-12-15, new method EmaSubjectModel.mean_attribute_grade
2021-12-20, new method EmaSubjectModel.nap_diff, calculate NAP distance

* Version 0.6:
2021-12-06, Allow user control switches: restrict_attribute OR restrict_threshold
2021-12-08, restrict_attribute: sensory-variable location average forced -> 0.
            restrict_threshold: response-threshold median forced -> 0.

* Version 0.5:
2021-11-03, first functional version
2021-11-04, removed EmaGroupModel.initialize_weights and EmaSubjectModel.initialize_weights
2021-11-05, Hamiltonian sampler -> EmaSubjectModel property -> better stepsize optimization
2021-11-07, store EmaParamBase object as property, so it gets pickled automatically
2021-11-18, cleanup comments
"""
import datetime as dt
import logging

import numpy as np

from EmaCalc.dirichlet_point import JEFFREYS_CONC
# = Jeffreys prior concentration for Dirichlet distribution

from EmaCalc.ema_base import EmaParamBase
from EmaCalc.ema_group import EmaGroupModel
from EmaCalc.ema_latent import Bradley


# -------------------------------------------------------------------
__ModelVersion__ = "2022-02-28"

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # *** TEST


# ------------------------------------------------------------------
class EmaModel:
    """Defines probability distributions of EMA recordings
    for all populations from which subjects were recruited,
    and for all subjects in each group,
    given all included EMA data,
    as collected in one ema_data.EmaDataSet instance.

    Model parameters define estimated probabilities for nominal SCENARIOS,
    and estimated latent sensory variables that determine ordinal subjective ratings
    on given ATTRIBUTE questions.
    The sensory variables have continuous values on an INTERVAL scale, as defined by the model,
    although all subjective Attribute ratings are discrete on ORDINAL scales.

    The ATTRIBUTE sensory variables may depend on one or more scenario dimensions,
    as estimated by an ordinal regression model,
    including main and interaction effects as requested by the user.

    The model allows for the possibility that different respondents
    might interpret and use the ordinal rating scales in different ways,
    by including separate response-threshold parameters for each individual.
    """
    def __init__(self, base, groups, rng):
        """
        :param base: single common EmaParamBase object, used by all model parts
        :param groups: dict with EmaGroupModel instances, stored as
            groups[group] = one EmaGroupModel instance, where
                group = dict key = tuple of tuple(s) = (group_factor, factor_category)
            groups[group].subjects[s_id] = an EmaSubjectModel instance, where
            s_id is a key identifying the subject.
        :param rng: random Generator object
        """
        self.base = base
        self.groups = groups
        self.rng = rng

    def __repr__(self):
        return self.__class__.__name__ + '(groups=groups)'

    @classmethod
    def initialize(cls, ds, effects,
                   max_n_comp=None,
                   rv_class=Bradley,
                   restrict_attribute=False,
                   restrict_threshold=False,
                   seed=None):
        """Create a crude initial model from all available count-profile data.
        :param ds: a single ema_data.EmaDataSet instance with all EMA data for analysis
        :param effects: iterable with desired estimated effects of scenario on attribute attribute_grades.
            Each effect element = a key in ds.emf.scenarios, or a tuple of such keys.
        :param max_n_comp: (optional) max number of profile clusters in learned model
            = max number of mixture components in the population model
            The number of actually used components may be reduced during VI learning.
        :param rv_class: (optional) class of latent sensory random variable
        :param restrict_attribute: (optional) boolean switch
            to force restriction on attribute sensory-variable locations
        :param restrict_threshold: (optional) boolean switch
            to force restriction on response-threshold locations
        :param seed: (optional) integer to get reproducible random sequences
        :return: a cls instance
        """
        ds.ensure_complete()
        if not (restrict_attribute or restrict_threshold):
            logger.warning('Either restrict_attribute or restrict_threshold '
                           + 'should be True, to avoid artificial variance')
        if restrict_attribute and restrict_threshold:
            restrict_attribute = False  # ONLY ONE restriction allowed
            logger.warning(f'Only ONE restriction allowed: using restrict_threshold={restrict_threshold}')
        base = EmaParamBase.initialize(ds.emf, effects, rv_class,
                                       restrict_attribute=restrict_attribute,
                                       restrict_threshold=restrict_threshold)
        # = all base variables, to be used by all model objects
        seed_seq = np.random.SeedSequence(seed)
        rng = np.random.default_rng(seed_seq)
        # = main Generator for all random numbers, EXCEPT EmaSubjectModel instances
        # Same rng for all EmaGroupModel instances, but separate for EmaSubjectModel-s
        group_seeds = seed_seq.spawn(len(ds.groups))
        groups = {g: EmaGroupModel.initialize(max_n_comp, base, g_data, g_seed, rng)
                  for ((g, g_data), g_seed) in zip(ds.groups.items(),
                                                   group_seeds)}
        logger.info('EmaModel initialized with ' +
                    f'{len(groups)} group(s); ' +
                    f'{base.n_parameters} model parameters;\n\t' +
                    f'restrict_attribute = {restrict_attribute}; '
                    f'restrict_threshold = {restrict_threshold};')
        if seed is None:
            logger.debug(f'*** Using seed={seed}')
        else:
            logger.warning(f'*** Using seed={seed} -> reproducible results.')
        return cls(base, groups, rng)

    # ------------------------------------------ General VI learn algorithm:
    def learn(self,
              min_iter=10,
              min_step=0.1,
              max_iter=np.inf,
              max_hours=0.,
              max_minutes=0.,
              callback=None):
        """Learn all individual and population parameter distributions
        from all observed EMA data stored in self.groups[...].subjects[...],
        using Variational Inference (VI).

        This method adapts Gaussian distributions for all mixture components in self.base.comp,
        and Dirichlet distributions for GMM mixture weights in all EmaGroupModel instances,
        and a sampled approximation of parameter distribution in all EmaSubjectModel instances.

        VI maximizes a lower bound to the total likelihood of all observed data.
        The resulting sequence of likelihood values is guaranteed to be non-decreasing,
        except for minor random variations caused by the sampling.

        :param min_iter: (optional) minimum number of learning iterations
        :param min_step: (optional) minimum data log-likelihood improvement,
                 over the latest min_iter iterations,
                 for learning iterations to continue.
        :param max_iter: (optional) maximum number of iterations, regardless of result.
        :param max_hours = (optional) maximal allowed running time, regardless of result.
        :param max_minutes = (optional) maximal allowed running time, regardless of result.
        :param callback: (optional) function to be called after each iteration step.
            If callable, called as callback(self, log_prob)
            where log_prob == scalar last achieved value of VI log-likelihood lower bound
        :return: log_prob = list of log-likelihood values, one for each iteration.

        Result: updated all properties of
        self.groups[...].pop_gmm properties comp, mix_weight
        self.groups[...].subjects[...].xi = parameter sample array
        """
        if max_hours == 0. and max_minutes == 0.:
            max_minutes = 30.
        logger.info('Learning the model. Might take some time! '
                    + f'Max {max_hours:.0f} hours {max_minutes:.0f} minutes.')
        min_iter = np.max([min_iter, 1])
        end_time = dt.datetime.now() + dt.timedelta(hours=max_hours,
                                                    minutes=max_minutes)
        # = last allowed time to start new VI iteration
        log_prob = []
        while (len(log_prob) <= min_iter
               or (log_prob[-1] - log_prob[-1 - min_iter] > min_step
                   and (len(log_prob) < max_iter)
                   and (dt.datetime.now() < end_time))):
            log_prob.append(self.adapt())
            if callable(callback):
                callback(self, log_prob[-1])
            logger.info(f'Done {len(log_prob)} iterations. LL={log_prob[-1]:.2f}')
        if dt.datetime.now() >= end_time:
            logger.warning('Learning stopped at time limit, possibly not yet converged')
        if len(log_prob) >= max_iter:
            logger.warning('Learning stopped at max iterations, possibly not yet converged')
        return log_prob

    def prune(self, min_weight=JEFFREYS_CONC):
        """Prune model to keep only active profile clusters
        :param min_weight: scalar, smallest accepted value for sum individual weight
        :return: None
        Result: all groups pruned with same criterion
        """
        for (g_name, g_model) in self.groups.items():
            # logger.info(f'Pruning group {g_name}:')
            g_model.prune(g_name, min_weight)

    def adapt(self):
        """One VI adaptation step for all groups
        :return: ll = scalar VI lower bound to data log-likelihood,
            incl. negative contributions for parameter KLdiv re priors
        """
        return sum(g_model.adapt(g_name)
                   for (g_name, g_model) in self.groups.items())


# ------------------------------------------------- TEST:
# if __name__ == '__main__':
