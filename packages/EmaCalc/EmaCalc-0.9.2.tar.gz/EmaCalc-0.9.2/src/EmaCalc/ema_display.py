"""This module defines classes and functions to display analysis results
given an EmaModel instance,
learned from a set of data from an EMA study.

Results are shown as figures and tables.
Figures can be saved in any file format allowed by Matplotlib, e.g.,
    'pdf', 'png', 'jpg', 'eps'.
Tables can be saved in any file format allowed by Pandas, e.g.,
    'txt', 'tex', 'csv', 'xlsx'.
Thus, both figures and tables can be easily imported into a LaTeX or word-processing document.

*** Main Class:

EmaDisplaySet = a structured container for all display results

Each display element can be accessed and modified by the user, before saving.

The display set can include data for three types of predictive distributions:
*: a random individual in the (Sub-)Population from which a group of respondents were recruited,
    (most relevant for an experiment aiming to predict the success of a new product,
    among individual potential customers in a population)
*: the mean (=median) in the (Sub-)Population from which a group of test subjects were recruited
    (with interpretation most similar to a conventional significance test)
*: each individual respondent in a Group of test subjects, with observed EMA data


*** Usage Example:
    See main scripts run_ema and run_sim

Figures and tables are automatically assigned descriptive names,
and saved in sub-directories with names constructed from labels of Groups.

If there is more than one Group,
    one sub-directory is created for each group,
    and one sub-sub-directory for each requested population / subject predictive result.

Thus, after saving, the display files are stored in a directory structure as, e.g.,
result_path / group / 'population_individual' / attributes / ....
result_path / group / 'population_individual' / scenarios / ....
result_path / group / 'subjects' / subject_id / attributes / ....
result_path / group / 'subjects' / subject_id / scenarios / ....
result_path / 'group_effects' / 'population_mean' / attributes / ...  (if more than one group)

*** Version History:
* Version 0.9.2:
2022-06-17, enforce y_min=0 in scenario probability percentile plot
2022-06-04, no FMT['and_head'], not used in ema_display_format.tab_credible_diff

* Version 0.9.1:
2022-04-04, no NAP calculations here, done by EmaDataSet instead
2022-04-04, no module-global formatting parameters in ema_display_format, only here
2022-04-04, EmaDisplaySet.save(...) takes file-format arguments
2022-04-04, make result tables as pandas DataFrame objects
2022-03-20, adapted to using Pandas CategoricalDtype instances in EmaFrame

* Version 0.8:
2022-02-15, minor cleanup of scenario profile tables

* Version 0.7:
2021-12-19, include table(s) of individual subject NAP results
2021-12-17, display aggregated Attribute effects weighted by Scenario probabilities

* Version 0.6:
2021-12-08, minor checks against numerical overflow

* Version 0.5.1
2021-11-27, allow NO Attributes in model, check display requests, minor cleanup

* Version 0.5
2021-11-05, copied from PairedCompCalc, modified for EmaCalc
2021-11-09, first functional version
"""
# ***** methods display -> create ?? ****
# ***** local superclass for pretty-printed repr() ?
# ***** allow several Attributes in single plot ?

import numpy as np
from pathlib import Path
import logging
from itertools import product
import string

from . import ema_display_format as fmt

from samppy.credibility import cred_diff, cred_group_diff

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # *** TEST

# N_SAMPLES = 1000

# ---------------------------- Default display parameters
FMT = {'scenarios': (),     # list of scenario dimensions to display
       'attributes': (),    # list of (attribute, scenario_effect) to display
       'percentiles': [5., 50., 95.],  # allowing 1, 2, 3, or more percentiles
       'grade_thresholds': True,  # include median response thresholds in plots
       'credibility_limit': 0.7,  # min probability of jointly credible differences
       'sc_probability': 'Probability',  # label in figs and tables
       'population_individual': True,  # show result for random individual in population
       'population_mean': True,  # show result for population mean
       'subjects': False,   # show results for each respondent
       'scale_unit': '',  # scale unit for attribute plot axis
       'credibility': 'Credibility',  # heading in difference table
       'high_low': ('Higher', 'Lower'),  # labels to distinguish difference columns
       # 'and_head': ('Diff.', 'jointly'), # NOT USED header of AND column in credible-diff tables
       'colors': 'rbgk',  # to distinguish results in plots, cyclic use
       'markers': 'oxs*_',  # corresponding markers, cyclic use
       }

DEFAULT_FIGURE_FORMAT = 'pdf'
DEFAULT_TABLE_FORMAT = 'txt'
# ******* allow only ONE format at each save(...) call ? ****************


def set_format_param(**kwargs):
    """Set / modify format parameters
    Called before any displays are generated.
    :param kwargs: dict with any formatting variables
    :return: None
    """
    other_fmt = dict()
    for (k, v) in kwargs.items():
        k = k.lower()
        if k in FMT:
            FMT[k] = v
        else:
            other_fmt[k] = v
    FMT['percentiles'].sort()  # ensure increasing values
    if len(other_fmt) > 0:
        logger.warning(f'Parameters {other_fmt} unknown, not used.')


# -------------------------------- Main Module Function Interface
# def display(ema_model, **kwargs):  # *** not needed ? ***
#     """Main function to display default set of EMA analysis results.
#     :param: ema_model: a single EmaModel object
#     :param: kwargs: (optional) any user-defined display format parameters
#     :return: single QualityDisplaySet instance with display results
#     """
#     return EmaDisplaySet.show(ema_model, **kwargs)


# ------------------------------------------------ Elementary Display Class:
class Profile:
    """Container for ONE selected profile display
    for ONE tuple of one or more scenario dimensions,
    OR for ONE (attribute, scenario_effect)
    """
    def __init__(self, plot=None, tab=None, diff=None,
                 path=None):
        """
        :param plot: (optional) ema_display_format.FigureRef instance with profile plot
        :param tab: (optional) ema_display_format.TableRef instance with same results tabulated.
        :param diff: (optional) ema_display_format.TableRef instance with credible differences.
        :param path: (optional) Path to directory containing all saved files from this Profile,
            to be assigned by save() method.
            file names are defined by sub-objects.
        """
        self.plot = plot
        self.tab = tab
        self.diff = diff
        self.path = path

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                '\n\t'.join(f'{k}= {repr(v)},'
                            for (k, v) in self.__dict__) +
                '\n\t)')

    def save(self, path,
             figure_format=None,
             table_format=None,
             **kwargs):
        """Save plot and table displays to files.
        May be called repeatedly with different file formats and kwargs.
        :param path: path to directory for saving files
        :param figure_format: (optional) single figure-file format string
        :param table_format: (optional) single table-file format string
        :param kwargs: (optional) additional parameters passed to TableRef.save() method.
            NOTE: NO extra kwargs allowed for plot.save() method!
        :return: None
        """
        if figure_format is None and table_format is None:
            figure_format = DEFAULT_FIGURE_FORMAT
            table_format = DEFAULT_TABLE_FORMAT
        path.mkdir(parents=True, exist_ok=True)
        self.path = path
        if figure_format is not None:
            if self.plot is not None:
                self.plot.save(path, figure_format=figure_format)
        if table_format is not None:
            if self.tab is not None:
                self.tab.save(path, table_format=table_format, **kwargs)
            if self.diff is not None:
                self.diff.save(path, table_format=table_format, **kwargs)


# ---------------------------------------------------------- Top Display Class:
class EmaDisplaySet:
    """Root container for all displays
    of selected predictive scenario and attribute results
    from one ema_model.EmaModel instance learned from an ema_data.EmaDataSet instance.

    All display elements can be saved as files in a selected directory three.
    The complete instance can also be serialized and dumped to a single pickle file,
    then re-loaded, edited, and re-saved, if user needs to modify some display object.
    """
    def __init__(self, groups, group_effects=None):
        """
        :param groups: dict with (group_id, GroupDisplaySet) elements
        :param group_effects: (optional) single GroupEffectSet instance,
            showing jointly credible differences between groups,
            IFF there is more than one group
        """
        self.groups = groups
        self.group_effects = group_effects

    def __repr__(self):  # *** general superclass for repr?
        return (self.__class__.__name__ + '(' +
                '\n\t'.join(f'{k}= {repr(v)},'
                            for (k, v) in self.__dict__.items()) +
                '\n\t)')

    def save(self, dir_top, **kwargs):
        """Save all displays in a directory tree
        :param dir_top: Path or string with top directory for all displays
        :param kwargs: (optional) dict with any additional format parameters, e.g.,
            figure_format, table_format, and any Pandas file-writer parameters.
        :return: None
        """
        dir_top = Path(dir_top)
        for (g, g_display) in self.groups.items():
            g = _dir_name(g, sep='/')
            if len(g) == 0 or all(s in string.whitespace for s in g):
                g_display.save(dir_top, **kwargs)
            else:
                g_display.save(dir_top / g, **kwargs)
        if self.group_effects is not None:
            self.group_effects.save(dir_top / 'group_effects', **kwargs)

    @classmethod
    def show(cls, emm,
             scenarios=None,
             attributes=None,
             **kwargs):
        """Create displays for all results from an EMA study,
        and store all display elements in a single structured object.
        :param emm: single ema_model.EmaModel instance, with
            emm.groups[group] = ema_model.EmaGroupModel instance,
            emm.groups[group][subject_id] = ema_model.EmaSubjectModel instance
        :param scenarios: (optional) list with selected scenario dimensions to be displayed.
            scenarios[i] = a selected key in emm.emf.scenarios, or a tuple of such keys.
        :param attributes: (optional) list with selected attribute displays to be displayed.
            attributes[i] = a tuple (attribute_key, sc_effect), where
                attribute_key is one key in emm.emf.attribute_grades,
                sc_effect is a scenario key in emm.emf.scenarios, or a tuple of such keys.
                A single key will yield the main effect of the named scenario dimension.
                An effect tuple will also show interaction effects between dimensions,
                IFF the model has been trained to estimate such interaction effects.
        :param: kwargs: (optional) dict with any other display formatting parameters
            either for ema_display.FMT or(***?) ema_display_format.FMT
        :return: a cls instance filled with display objects
        """
        # get default scale_unit from emm, if not in kwargs:
        if 'scale_unit' not in kwargs:
            kwargs['scale_unit'] = emm.base.rv_class.unit_label
        if scenarios is None:
            scenarios = [*emm.base.emf.scenarios.keys()]
            # default showing only main effects for each scenario dimension
        scenarios = [(sc,) if isinstance(sc, str) else sc
                     for sc in scenarios]
        # *** check that requested scenarios exist in model:
        missing_sc = [sc_i for sc_i in scenarios
                      if any(sc_ij not in emm.base.emf.scenarios.keys()
                             for sc_ij in sc_i)]
        for sc in missing_sc:
            logger.warning(f'Scenario dimension {sc} unknown in the learned model.')
            scenarios.remove(sc)
        if attributes is None:
            attributes = []
        attributes = [(a, sc) if type(sc) is tuple else (a, (sc,))
                      for (a, sc) in attributes]
        # *** check that requested attribute effects exist in model
        missing_attr = [a_sc for a_sc in attributes
                        if a_sc[0] not in emm.base.emf.attribute_grades.keys()]
        for a_sc in missing_attr:
            logger.warning(f'Attribute effect {a_sc} unknown in the learned model.')
            attributes.remove(a_sc)
        # if nap is None:
        #     nap = []
        # else:
        #     nap = [(a, sc) if type(sc) is tuple else (a, (sc,))
        #            for (a, sc) in nap]
        set_format_param(scenarios=scenarios,
                         attributes=attributes,
                         **kwargs)
        # display separate results for each group
        groups = {g: GroupDisplaySet.display(emm_g)
                  for (g, emm_g) in emm.groups.items()}

        if len(groups) > 1:
            group_effects = GroupEffectSet.display(emm)
        else:
            group_effects = None
        logger.info(fig_comments())
        logger.info(table_comments())
        return cls(groups, group_effects)


class GroupDisplaySet:
    """Container for all quality displays related to ONE experimental group:
    Predictive results for the population from which the subjects were recruited,
    and descriptive data for each individual subject, if requested by user.
    """
    def __init__(self,
                 population_mean=None,
                 population_individual=None,
                 subjects=None):
        """
        :param population_mean: dict with (a_label: AttributeDisplay object), for population mean,
        :param population_individual: dict with (a_label: AttributeDisplay object), for random individual,
        :param subjects: dict with (s_id: EmaDisplay instance) for participants in one group
            with scenario and attribute results.
        """
        self.population_mean = population_mean
        self.population_individual = population_individual
        self.subjects = subjects

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                '\n\t'.join(f'{k}= {repr(v)},'
                            for (k, v) in self.__dict__.items()) +
                '\n\t)')

    def save(self, path, **kwargs):
        """Save all stored display objects in their corresponding sub-trees
        """
        if self.population_mean is not None:
            self.population_mean.save(path / 'population_mean', **kwargs)
        if self.population_individual is not None:
            self.population_individual.save(path / 'population_individual', **kwargs)
        if self.subjects is not None:
            for (s, s_disp) in self.subjects.items():
                s_disp.save(path / 'subjects' / str(s), **kwargs)

    @classmethod
    def display(cls, emm_g):
        """Generate all displays for ONE group
        :param emm_g: dict with elements (a_label: pc_result.PairedCompGroupModel)
        :return: cls instance with all displays for this group
        """
        pop_ind = None
        pop_mean = None
        subjects = None  # ***** empty dict in case no subjects shown
        if FMT['population_individual']:
            pop_ind = EmaDisplay.display(emm_g.predictive_population_ind())
        if FMT['population_mean']:
            pop_mean = EmaDisplay.display(emm_g.predictive_population_mean())
        if FMT['subjects']:
            # logger.debug('Displaying subjects:')
            subjects = {s: EmaDisplay.display(s_model)
                        for (s, s_model) in emm_g.subjects.items()}
        return cls(population_mean=pop_mean,
                   population_individual=pop_ind,
                   subjects=subjects)


# ------------------------------------- Secondary-level displays
class EmaDisplay:
    """Container for all scenario and attribute displays for ONE (Sub-)Population
    either random-individual or mean,
    OR for ONE subject.
    """
    def __init__(self, scenarios, attributes):
        """
        :param scenarios: dict with (scenario_tuple, profile), where
            profile is a Profile instance for the selected scenario_tuple
        :param attributes: dict with (attr_effect, profile), where
            profile is an Profile instance for the selected attr_effect
        """
        self.scenarios = scenarios
        self.attributes = attributes

    def save(self, path, **kwargs):
        """Save all stored display objects in specified (sub-)tree
        :param path: path to directory for saving
        :return: None
        """
        if len(self.scenarios) > 0:
            for (d, sc_display) in self.scenarios.items():
                sc_display.save(path / 'scenarios', **kwargs)
        if len(self.attributes) > 0:
            for (d, a_display) in self.attributes.items():
                a_display.save(path / 'attributes', **kwargs)

    @classmethod
    def display(cls, m_xi):
        """
        :param m_xi: probability model for ema_model parameter vector xi
            either for population-individual, population-mean, or individual subject
        :return: a cls instance
        """
        xi = m_xi.rvs()
        scenarios = {sc: ScenarioProfile.display(xi, m_xi, sc)  # *** m_xi -> base
                     for sc in FMT['scenarios']}
        attributes = {a_effect: AttributeProfile.display(xi, m_xi, a_effect)  # *** m_xi -> base
                      for a_effect in FMT['attributes']}
        return cls(scenarios, attributes)


# ----------------------------------------------------------------------
class ScenarioProfile(Profile):
    """Container for all displays of ONE scenario effect
    in ONE (Sub-)Population, OR for ONE respondent.
    NOTE: Scenario profiles are displayed as
    CONDITIONAL probability of categories in ONE scenario dimension,
    GIVEN categories in other dimension(s), if requested.
    """
    @classmethod
    def display(cls, xi, m_xi, sc_keys):
        """Generate a probability-profile display for selected distribution and factor
        :param xi: 2D array of parameter-vector samples drawn from m_xi
        :param m_xi: a population or individual model instance
        :param sc_keys: tuple of one or more key(s) selected from emf.scenarios.keys()
        :return: single cls instance showing CONDITIONAL probabilities
            for sc_keys[0], GIVEN each combination (j1,..., jD) for sc_keys[1], ...
        """
        emf = m_xi.base.emf
        u = m_xi.base.scenario_prob(xi)
        u /= u.shape[1]  # = JOINT prob mass, incl. TestPhase: sum(u) == 1
        u = _aggregate_scenario_prob(u, emf, sc_keys)
        # Now with reordered and aggregated joint probabilities
        # for selected subset of scenario dimensions, such that
        # u[s, j0, j1, ...] = s-th sample of joint probability for
        # emf.scenario[sc_keys[0]][j0], emf.scenario[sc_keys[1]][j1], ... etc.
        # u.shape == (u.shape[0], *emf.scenario_shape[emf.scenario_axes(sc_keys)])
        if len(sc_keys) > 1:
            s = np.sum(u, axis=1, keepdims=True)
            # too_small = s <= 0
            n_underflow = np.sum(s <= 0.)
            if n_underflow > 0:
                logger.warning(f'Scenario display: {n_underflow} prob. sample(s) == 0, '
                               + f'with {sc_keys}. '
                               + 'Should not happen! Maybe too few EMA records?')
                s = np.maximum(s, np.finfo(float).tiny)
            u /= s
            # u[:, i, ...] = samples for CONDITIONAL probability of i-th category in sc_keys[0],
            # GIVEN ...-th category product of sc_keys[1:]
            u = u.reshape((*u.shape[:2], -1))
            # now linear-indexed in 3D with
            # u[:, :, j] = prob given j-th product of sc_keys[2:], if any given
            # case_labels[2] = all sc_keys[2:] joined  # ****************** !!!!
        q = np.percentile(u, FMT['percentiles'], axis=0)
        # --------------------------------------- percentile table as DataFrame:
        case_labels = dict(_case_labels(emf.scenarios, sc_keys))
        df = fmt.tab_percentiles(q, perc=FMT['percentiles'],
                                 case_labels=case_labels,
                                 )
        perc = fmt.fig_percentiles(df, case_labels=case_labels,
                                   y_label=FMT['sc_probability'],
                                   file_label='',
                                   colors=FMT['colors'],
                                   markers=FMT['markers'],
                                   y_min=0.
                                   )
        # ---------------------------------------- sc_keys differences
        # NOTE: Comparing CONDITIONAL probabilities of categories in FIRST sc_keys dimension,
        # GIVEN categories in other dimensions.
        d = cred_diff(u, diff_axis=1, sample_axis=0, case_axis=2,
                      p_lim=FMT['credibility_limit'])
        diff_df = fmt.tab_credible_diff(d,
                                        y_label=FMT['sc_probability'],
                                        diff_head=sc_keys[0:1],
                                        diff_labels=_product_labels(emf.scenarios, sc_keys[0:1]),
                                        cred_head=FMT['credibility'],
                                        case_head=sc_keys[1:],
                                        case_labels=_product_labels(emf.scenarios, sc_keys[1:]),
                                        high_low=FMT['high_low'],
                                        # and_head=FMT['and_head']
                                        )
        # ---------------------------------------------------------------------
        return cls(plot=perc, tab=df, diff=diff_df)


class AttributeProfile(Profile):
    """Container for displays of ONE attribute, and scenario_effect(s),
    in ONE (Sub-)Population, OR for ONE respondent.

    NOTE: Latent-variable results are displayed for each Attribute,
    GIVEN Scenario categories in requested Scenario dimensions,
    averaged across all OTHER Scenario dimension,
    weighted by Scenario probabilities in those dimensions.
    """
    # **** allow several attributes in one display ? *****
    @classmethod
    def display(cls, xi, m_xi, a_effect):
        """Create displays for a single attribute and requested scenario effects
        :param xi: 2D array of parameter-vector samples drawn from m_xi
        :param m_xi: a population or individual model instance
        :param a_effect: tuple(attribute_key, sc_keys)
        :return: single cls instance with all displays
        """
        emf = m_xi.base.emf
        u = m_xi.base.scenario_prob(xi)
        u /= u.shape[1]  # = JOINT prob mass, incl. TestPhase: sum(u) == 1
        (a, sc) = a_effect
        # a = attribute key, sc_keys = tuple of scenario keys
        # file_name = a + '_vs_' + '*'.join(sc)
        theta = m_xi.base.attribute_theta(xi, a)
        # theta[s, k0, k1,...] = s-th sample of attribute a, given (k0, k1,...)-th scenario
        theta = _aggregate_scenario_theta(theta, u, emf, sc)
        # theta[s, j0, j1,...] = s-th sample of attribute a,
        #   given (scenarios[sc_keys[0]][j0], scenarios[sc_keys[1]][j1], ...)
        if FMT['grade_thresholds']:
            tau = np.median(m_xi.base.attribute_tau(xi, a), axis=0)
            # tau[l] = l-th median rating threshold for attribute a
        else:
            tau = None
        q = np.percentile(theta, FMT['percentiles'], axis=0)
        # --------------------------------------- percentile table:
        case_labels = dict(_case_labels(emf.scenarios, sc))
        df = fmt.tab_percentiles(q, perc=FMT['percentiles'],
                                 case_labels=case_labels,
                                 file_label=a
                                 )  # *** replacing tab_perc... ?
        perc = fmt.fig_percentiles(df, case_labels=case_labels,
                                   y_label=a + ' (' + FMT['scale_unit'] + ')',
                                   file_label=a,  # *** needed ?
                                   cat_limits=tau,
                                   colors=FMT['colors'],
                                   markers=FMT['markers']
                                   )
        # ---------------------------------------- attr differences
        # NOTE: comparing all scenario-categories, in all requested sc dimensions
        th_1 = theta.reshape((theta.shape[0], -1))
        # all sc_keys dimensions flattened into th_1[:, 1]
        d = cred_diff(th_1, diff_axis=1, sample_axis=0,
                      p_lim=FMT['credibility_limit'])
        diff_df = fmt.tab_credible_diff(d,
                                        y_label=a,  # for table header
                                        file_label=a,
                                        diff_head=sc,
                                        diff_labels=_product_labels(emf.scenarios, sc),
                                        cred_head=FMT['credibility'],
                                        high_low=FMT['high_low'],
                                        # and_head=FMT['and_head']
                                        )
        return cls(plot=perc, tab=df, diff=diff_df)


# --------------------------------- classes for differences between groups
class GroupEffectSet:
    """Container for displays of differences between populations,
    as represented by subjects in separate groups
    """
    def __init__(self, population_mean=None, population_individual=None):
        """
        :param population_mean: dict with elements (a_label, AttributeGroupEffects instance)
        :param population_individual: dict with elements (a_label, AttributeGroupEffects instance)
            both with results separated by groups
        """
        self.population_mean = population_mean
        self.population_individual = population_individual

    def save(self, path, **kwargs):
        """Save all stored display objects in their corresponding sub-trees
        """
        if self.population_mean is not None:
            self.population_mean.save(path / 'population_mean', **kwargs)
        if self.population_individual is not None:
            self.population_individual.save(path / 'population_individual', **kwargs)

    @classmethod
    def display(cls, emm):
        """Generate all displays for ONE group
        :param emm: ema_model.EmaModel instance with several groups
        :return: cls instance with all displays of differences
            between predictive distributions for
            population random individual, AND/OR
            population mean
        """
        pop_ind = None
        pop_mean = None
        if FMT['population_individual']:
            pop_ind = EmaGroupDiff.display(emm,
                                           {g: emm_g.predictive_population_ind()
                                            for (g, emm_g) in emm.groups.items()})
        if FMT['population_mean']:
            pop_mean = EmaGroupDiff.display(emm,
                                            {g: emm_g.predictive_population_mean()
                                             for (g, emm_g) in emm.groups.items()})
        return cls(population_mean=pop_mean,
                   population_individual=pop_ind)


class EmaGroupDiff:
    """Container for displays of differences between (Sub-)Populations
    represented by separate ema_model.EmaGroupModel instances.
    """
    def __init__(self, scenarios, attributes):
        """
        :param scenarios: dict with (scenario_tuple, diff_profile), where
            profile is a Profile instance for the selected scenario_tuple
        :param attributes: dict with (attr_effect, diff_profile), where
            profile is a Profile instance for the selected attr_effect
        """
        self.scenarios = scenarios
        self.attributes = attributes

    def save(self, path, **kwargs):
        """Save all stored display objects in specified (sub-)tree
        """
        if len(self.scenarios) > 0:
            for (d, sc_display) in self.scenarios.items():
                sc_display.save(path / 'scenarios', **kwargs)
        if len(self.attributes) > 0:
            for (d, a_display) in self.attributes.items():
                a_display.save(path / 'attributes', **kwargs)

    @classmethod
    def display(cls, emm, groups):
        """
        :param emm: ema_model.EmaModel instance with several groups
        :param groups: dict with elements (g_id, g_model), where
            g_id is a tuple of one or more tuple(group_factor, factor_category),
            g_model is a predictive ema_model.PredictivePopulationModel instance
            i.e. NOT emm.groups
        :return: single cls instance
        """
        xi = [g_model.rvs()
              for g_model in groups.values()]
        # xi[g][s, :] = s-th sample of parameter vector for g-th group
        scenarios = {sc: ScenarioDiff.display(xi, emm, sc)
                     for sc in FMT['scenarios']}
        attributes = {a_effect: AttributeDiff.display(xi, emm, a_effect)
                      for a_effect in FMT['attributes']}
        return cls(scenarios, attributes)


class ScenarioDiff(Profile):
    @classmethod
    def display(cls, xi, emm, sc_keys):
        """Generate a probability-profile display for selected distribution and factor
        :param xi: list of 2D arrays of parameter-vector samples
            len(xi) == len(emm.groups)
        :param emm: ema_model.EmaModel object
        :param sc_keys: tuple of one or more key(s) selected from emf.scenarios.keys()
        :return: single cls instance
        """
        emf = emm.base.emf
        u = [emm.base.scenario_prob(xi_g) for xi_g in xi]
        # u[g][s, k0, k1, ...] = s-th sample of (k0, k1,...)-th scenario prob in g-th population
        for u_g in u:
            u_g /= u_g.shape[1]  # = JOINT prob mass, incl. k0 = TestPhase index:
            # sum(u_g) == 1
        u = [_aggregate_scenario_prob(u_g, emf, sc_keys)
             for u_g in u]
        # Now with reordered and aggregated joint probabilities
        # for selected subset of scenario dimensions, such that
        # u[g, s, j0, j1, ...] = s-th sample of joint probability for
        # emf.scenario[sc_keys[0]][j0], emf.scenario[sc_keys[1]][j1], ... etc.
        # file_name = '_'.join(sc_keys)
        if len(sc_keys) > 1:
            u_check = []
            for u_g in u:
                s = np.sum(u_g, axis=1, keepdims=True)
                n_underflow = np.sum(s <= 0.)
                if n_underflow > 0:
                    logger.warning(f'ScenarioDiff display: {n_underflow} prob. sample(s) == 0. '
                                   + 'Should not happen! Maybe too few responses?')
                    s = np.maximum(s, np.finfo(float).tiny)
                u_check.append(u_g / s)
            u = u_check
            # u = [u_g / np.sum(u_g, axis=1, keepdims=True)
            #      for u_g in u]
            # u[g][s, i, ...] = samples for CONDITIONAL probability of i-th category in sc_keys[0],
            # GIVEN ...-th category product of sc_keys[1:]
            u = [u_g.reshape((u_g.shape[0], -1))
                 for u_g in u]
            # now each u_g linear-indexed in 2D with
            # u[g][s, j] = j-th product of sc_keys
        # ---------------------------------------- sc_keys differences
        # NOTE: Comparing CONDITIONAL probabilities of categories in FIRST sc_keys dimension,
        # GIVEN categories in other dimensions.
        d = cred_group_diff(u, sample_axis=0, case_axis=1,
                            p_lim=FMT['credibility_limit'])
        # diff_old = fmt.tab_credible_diff(d,
        #                                  diff_labels=emm.groups.keys(),
        #                                  case_labels=_product_tuples(emf.scenarios, sc_keys)
        #                                  )
        group_head = [tuple(gk[0] for gk in g_key)
                      for g_key in emm.groups]  # [0] all same
        group_cat = [tuple(gk[1] for gk in g_key)
                     for g_key in emm.groups]
        diff = fmt.tab_credible_diff(d,
                                     y_label=FMT['sc_probability'],
                                     diff_head=group_head[0],
                                     diff_labels=group_cat,
                                     case_head=sc_keys,
                                     case_labels=_product_labels(emf.scenarios, sc_keys),
                                     cred_head=FMT['credibility'],
                                     high_low=FMT['high_low'],
                                     # and_head=FMT['and_head']
                                     )
        # ---------------------------------------------------------------------
        return cls(diff=diff)


class AttributeDiff(Profile):  # **************** not tested
    """Container for all displays of group differences in ONE Attribute-by-Scenario effect
    """
    # **** allow several attributes in one display ? ***************
    @classmethod
    def display(cls, xi, emm, a_effect):
        """Create displays for a single attribute and requested scenario effects
        :param xi: list of 2D arrays of parameter-vector samples
            len(xi) == len(emm.groups)
        :param a_effect: tuple (attr_key, sc_keys), where
            sc_keys is a tuple of one or more key(s) selected from emf.scenarios.keys()
        :param emm: ema_model.EmaModel object
        :return: single cls instance
        """
        emf = emm.base.emf
        u = [emm.base.scenario_prob(xi_g) for xi_g in xi]
        # u[g][s, k0, k1, ...] = s-th sample of (k0, k1,...)-th scenario prob in g-th population
        for u_g in u:
            u_g /= u_g.shape[1]  # = JOINT prob mass, incl. k0 = TestPhase index:
            # sum(u_g) == 1
        (a, sc) = a_effect
        # a = attribute key, sc_keys = tuple of scenario keys
        # file_name = a + '_vs_' + '*'.join(sc)
        theta = [emm.base.attribute_theta(xi_g, a)
                 for xi_g in xi]
        # theta[g][s, k0, k1,...] = s-th sample of attribute a, given (k0, k1,...)-th scenario
        theta = [_aggregate_scenario_theta(theta_g, u_g, emf, sc)
                 for (theta_g, u_g) in zip(theta, u)]
        # theta[s, j0, j1,...] = s-th sample of attribute a,
        #   given (scenarios[sc_keys[0]][j0], scenarios[sc_keys[1]][j1], ...)
        #   averaged across OTHER scenarios, weighted by scenario-probabilities.
        # ---------------------------------------- attr differences
        # NOTE: comparing all scenario-categories, in all requested sc dimensions
        th_1 = [theta_g.reshape((theta_g.shape[0], -1))
                for theta_g in theta]
        # all sc_keys dimensions flattened into th_1[g][s, :]
        d = cred_group_diff(th_1, sample_axis=0, case_axis=1,
                            p_lim=FMT['credibility_limit'])
        # diff_old = fmt.tab_credible_diff(d,
        #                              y_label=a,
        #                              file_label=a,
        #                              diff_labels=emm.groups.keys(),
        #                              case_labels=_product_tuples(emf.scenarios, sc)
        #                              )
        group_head = [tuple(gk[0] for gk in g_key)
                      for g_key in emm.groups]  # [0] all same
        group_cat = [tuple(gk[1] for gk in g_key)
                     for g_key in emm.groups]
        diff = fmt.tab_credible_diff(d,
                                     y_label=a,
                                     file_label=a,
                                     diff_head=group_head[0],
                                     diff_labels=group_cat,
                                     case_head=sc,
                                     case_labels=_product_labels(emf.scenarios, sc),
                                     cred_head=FMT['credibility'],
                                     high_low=FMT['high_low'],
                                     # and_head=FMT['and_head']
                                     )
        # ---------------------------------------------------------------------
        return cls(diff=diff)


# ---------------------------------- Help functions:
def _aggregate_scenario_prob(u, emf, sc):
    """Aggregate probability-mass samples to keep only selected factor axes
    :param u: multi-dim array with probability-mass samples
        u[s, k0, k1,...] = s-th sample of JOINT prob
            for (k0, k1,...)-th scenario, as defined by emf.scenarios.items()
        u.shape == (n_samples, *emf.scenario_shape)
    :param emf: ema_data.EmaFrame instance for model generating u
    :param sc: tuple with selected scenario keys to display
    :return: array uf with aggregated joint probabilities
        uf[s, j0, j1, ...] = s-th sample of joint probability for
        scenario[sc[0]][j0], scenario[sc[1]][j1], ... etc.
        uf.shape == (u.shape[0], *emf.scenario_shape[emf.scenario_axes(sc)])
    """
    axes = tuple(1 + i for i in emf.scenario_axes(sc))
    uf = np.moveaxis(u, axes, tuple(range(1, 1+len(axes))))
    # with desired sc_keys axes first after 0
    sum_axes = tuple(range(1+len(axes), uf.ndim))
    uf = np.sum(uf, axis=sum_axes)
    # summed across all OTHER axes, except those in sc_keys
    return uf


def _aggregate_scenario_theta(th, u, emf, sc):
    """Aggregate attribute location sample arrays to keep only selected factor axes
    :param th: multi-dim array with attribute-location samples
        th[s, k0, k1,...] = s-th sample of latent variable theta
            in (k0, k1,...)-th scenario, as defined by emf.scenarios.items()
        th.shape == (n_samples, *emf.scenario_shape)
    :param u: multi-dim array with corresponding samples of normalized scenario probabilities
        u[s, k0, k1, ...] = s-th sample of normalized probability of (k0, k1,...)-th scenario
        sum_(k0, k1, ...) u[s, k0, k1, ...] == 1, for all s
        u.shape == th.shape
    :param emf: ema_data.EmaFrame instance for model generating u
    :param sc: tuple with selected scenario keys to display
    :return: th_a = array with aggregated attribute locations
        th_a[s, j0, j1, ...] = s-th sample of conditional attribute location,
        GIVEN scenario[sc[0]][j0], scenario[sc[1]][j1], ... etc.
        averaged across all OTHER Scenarios not included in sc.
        th_a.shape == (n_samples, *emf.scenario_shape[emf.scenario_axes(sc)])

    2021-12-17, probability-averaged across non-included Scenarios
    """
    keep_axes = tuple(1 + i for i in emf.scenario_axes(sc))
    w = np.sum(u, axis=keep_axes, keepdims=True)
    # = normalized scenario prob, for every sample
    th = np.moveaxis(th, keep_axes, tuple(range(1, 1 + len(keep_axes))))
    w = np.moveaxis(w, keep_axes, tuple(range(1, 1 + len(keep_axes))))
    # th and w now with desired sc_keys axes first after sample-axis = 0
    aggregate_axes = tuple(range(1+len(keep_axes), th.ndim))
    # = all OTHER axes, except those in sc_keys
    # th_old = np.mean(th, axis=aggregate_axes)
    # # averaged across all aggregate_axes. version <= 0.6
    th = np.sum(th * w, axis=aggregate_axes)
    # = probability-averaged across all aggregate_axes. version >= 0.7
    return th


def _case_labels(label_dict, key_list):  # v 0.9
    """Selected case Labels
    :param label_dict: a dict with elements (factor_key, factor_cat), where
        factor_key is a key to a EmaFrame scenarios or attribute_grades,
        factor_cat is a pd.CategoricalDtype instance defining factor_key categories
    :param key_list: sequence of factor_key cases to be included
    :return: labels = list of tuples, with
        i-th tuple = (key_list[i], label_dict[key_list[i].categories)
    """
    # **** return dict instead ??? **************
    return [(gf, label_dict[gf].categories) for gf in key_list]


def _product_labels(label_dict, key_list):  # v 0.9
    """Iterator of tuples, each
    a product of one category from each desired factor dimension
    :param label_dict: a dict with elements (factor_key, factor_cat), where
        factor_key is a key to a EmaFrame scenarios or attribute_grades,
        factor_cat is a pd.CategoricalDtype instance defining factor_key categories
    :param key_list: list of keys to label_dict
    :return: labels = list with tuples, with
        ...-th tuple = (label_dict[keys[0][i0], ..., label_dict[keys[D][iD])
        where D = len(keys)
        with last index iD varying fastest, i0 slowest, in the product tuples
    """
    return [*product(*(label_dict[gf].categories for gf in key_list))]


def _dir_name(g, sep='_'):
    """make sure group name is a possible directory name
    :param g: string or tuple of strings
    :return: string to be used as directory
    """
    if type(g) is tuple:  # several strings
        g = sep.join(_dir_name(g_s, sep='_')
                     for g_s in g)
    return g


def fig_comments():
    """Generate figure explanations.
    :return: comment string
    """
    p_min = np.amin(FMT['percentiles'])
    p_max = np.amax(FMT['percentiles'])
    c = f"""Figure Explanations:
    
Figure files with names like
someScenarioName_xxx.pdf, someAttributeName_xxx.pdf or xxx.jpg, or similar,
display user-requested percentiles (markers) and credible intervals (vertical bars) 
The vertical bars show the range between {p_min:.1f}- and {p_max:.1f}- percentiles.

Median ordinal grade thresholds for perceptual Attributes, if requested,
are indicated by thin lines extending horizontally across the graph.

These displayed ranges include all uncertainty
caused both by real inter-individual perceptual differences
and by the limited number of responses by each listener.
"""
    return c


def table_comments():
    c = """Table Explanations:

*** Tables of Percentiles:
Files with names like someScenarioName_xxx.tex, someAttributeName_xxx.tex or *.txt
show numerical versions of the information in corresponding percentile plots.
Percentiles, credible ranges, and marginal probabilities for negative and positive values are shown.

*** Tables of Credible Differences:
Files with names like someAttribute-diff_xxx.tex or *.txt 
show a list of Attribute (in Scenario) pairs
which are ALL JOINTLY credibly different
with the tabulated credibility.
The credibility value in each row is the JOINT probability
for the pairs in the same row and all rows above it.
Thus, the joint probability values already account for multiple comparisons,
so no further adjustments are needed.
"""
    return c
