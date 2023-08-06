"""This module defines classes to access and store recorded EMA data,
and methods and functions to read and write such data.

Each EMA Record includes nominal and ordinal elements, defining
* a subject ID label,
* a single SCENARIO specified by selected categories in ONE or MORE Scenario Dimension(s),
* ordinal RATING(s) for ZERO, ONE, or MORE perceptual ATTRIBUTE(s) in the current scenario.

*** Class Overview:

EmaFrame: defines layout and category labels of data in each EMA Record.
    Some properties of an EmaFrame instance can also define selection criteria
    for a subset of data to be included for analysis.

EmaDataSet: container of all data to be used as input for statistical analysis.

*** File Formats:

Data may be stored in various table-style file formats allowed by package pandas,
e.g., xlsx, txt, csv.
A single data file may include EMA records from ONE or SEVERAL subjects.
The subject id may be stored in a designated column of the table,
otherwise the file name can be used as subject id,
or (in Excel files) the subject may be identified by the sheet name.

However, EmaDataSet.save(...) method always creates ONE file for ONE subject.


*** Input Data Files:

All input files from an experiment must be stored in ONE directory tree.

If results are to be analyzed for more than one GROUP of test subjects,
the data for each group must be stored in separate sub-directories
within the specified top directory.

Groups are identified by a tuple of pairs (group_factor, group_category), where
group_factor is a grouping dimension, e.g., 'Age', or 'Gender', and
group_category is a category label within the factor, e.g., 'old', or 'female'.

A sequence of one element from each group-factor pair must define a unique path
to files containing data for subjects in ONE group.
Group directories must have names like, e.g., 'Age_old' for group = ('Age', 'old')

Subject file names are arbitrary, although they may be somehow associated with
the encoded name of the participant, to facilitate data organisation.

Each subject in the same group must have a unique subject ID.

Different files in the same sub-directory
may include data for the same subject in the group,
e.g., results obtained in different test phases,
or simply for replicated EMA responses from the same subject.

Subjects in different groups may have the same subject ID values,
because the groups are separated anyway,
but normally the subject IDs should be unique across all groups.

*** Example Directory Tree:

Assume we have data files in the following directory structure:
~/ema_study / Age_old / Gender_male, containing files Data_EMA_64.xlsx and Response_Data_LAB_64.xlsx
~/ema_study / Age_old / Gender_female, containing files Subjects_EMA_64.xlsx and Data_EMA_65.xlsx
~/ema_study / Age_young / Gender_male,  containing files EMA_64.xlsx and EMA_65.xlsx
~/ema_study / Age_young / Gender_female, containing files EMA_64.xlsx and EMA_65.xlsx

Four separate groups may then be defined by factors Age and Gender,
and the analysis may be restricted to data in files with names including 'EMA_64'.


*** Accessing Input Data for Analysis:
*1: Create an EmaFrame object defining the experimental layout, e.g., as:

emf = EmaFrame(scenarios={'CoSS': [f'C{i}' for i in range(1, 8)],
                          'Important': ('Slightly', 'Medium', 'Very'),
                          },  # nominal variables
               attribute_grades={'Speech': ('Very Hard', 'Fairly Hard', 'Fairly Easy','Very Easy')},
        )
NOTE: Letter CASE is always distinctive, i.e., 'Male' and 'male' are different categories.

*2: Load all test results into an EmaDataSet object:

ds = EmaDataSet.load(emf, path='~/ema_study',
                    grouping={'Age': ('young', 'old'),
                              'Gender': ('female', 'male'),
                              'Test': ('EMA_64',)}
                    fmt='xlsx',
                    subject='sheet',    # xlsx sheet title is subject ID
                    )
Package Pandas is used for reading, allowing several file formats and recoding options.

The object ds can then be used as input for analysis.
The parameter emf is a EmaFrame object that defines the variables to be analyzed.

*** Selecting Subsets of Data for Analysis:
It is possible to define a data set including only a subset of recorded data files.

For example, assume we want to analyze only two groups, old males, and old females.
and only responses for Scenario dimension 'CoSS'.
Then we must define a new EmaFrame object, and load only a subset of group data:

emf = EmaFrame(scenarios={'CoSS': [f'C{i}' for i in range(1, 8)],
                          },  # nominal variables
               attribute_grades={'Speech': ('Very Hard', 'Fairly Hard', 'Fairly Easy','Very Easy')},
        )
ds = EmaDataSet.load(emf, path='~/ema_study',
                    grouping={'Age': ('old',),
                              'Gender': ('female', 'male'),
                              'Test': ('EMA_64',)}
                    fmt='xlsx',
                    subject='sheet',    # xlsx sheet title is subject ID
                    )


*** Version History:
* Version 0.9.2:
2022-06-16, minor fix in EmaDataSet.mean_attribute_table, nap_table
2022-06-03, changed variable name stage -> phase everywhere
2022-05-21, clearer logger info for valid- and missing-data input

* Version 0.9:
2022-03-17, use Pandas CategoricalDtype instances in EmaFrame scenarios and attributes
2022-03-18, use Pandas DataFrame format in EmaDataSet, to allow many input file formats

* Version 0.8.3:
2022-03-08, minor fix for FileReadError error message

* Version 0.8.1:
2021-02-27, fix EmaDataSet.load(), _gen_group_file_paths(), _groups(), for case NO group_by

* Version 0.5.1:
2021-11-26, EmaDataSet.load warning for input argument problems

* Version 0.5:
2021-10-15, first functional version
2021-11-18, group_by moved from EmaFrame -> EmaDataSet.load
2021-11-20, EmaDataSet.ensure_complete
2021-11-23, Group dir name MUST include both (g_factor, g_cat), e.g., 'Age_old'
2021-11-xx, allow empty attribute_grades
"""
# *** Allow EmaFrame.attributes with tied response alternatives across several attributes ? ***
# *** EmaDataSet.initialize + add method ? load = initialize + add
# *** save EmaDataSet as ONE big DataFrame file ?
# *** EmaDataSet store groups / subgroups hierarchically in tree structure ?

import numpy as np
from pathlib import Path
import pandas as pd
# from pandas.io.formats.style import Styler

from itertools import product
import logging

from EmaCalc.ema_file import ema_gen, Table, FileReadError, FileWriteError
from EmaCalc.ema_nap import nap_pandas

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


# ------------------------------------------------------------------
class EmaFrame:
    """Defines types and categories of all data elements
    recorded by each respondent in an EMA study.
    The allowed categories of each EMA variable is stored as a pd.CategoricalDtype instance.
    """
    def __init__(self,
                 scenarios=None,
                 phase_key='Phase',  # default scenario key for test phase
                 attribute_grades=None,
                 ):
        """
        :param scenarios: (optional) dict or iterable with elements (scene_factor, category_list), where
            scene_factor is a string label identifying one scenario "dimension",
            category_list is an iterable of labels for NOMINAL categories within this scene_factor.
        :param attribute_grades: (optional) dict or iterable with elements (attribute, grades),
            attribute is string id of a rated perceptual attribute,
            grades is an iterable with ORDINAL categories, strings or integer.
        :param phase_key: (optional) scenario key for the test phase, with
            scenarios[phase_key] = list of test phases (e.g., before vs after treatment),
                specified by experimenter, i.e., NOT given as an EMA response
            scenarios[phase_key] is automatically added with a SINGLE value,
            if not already defined in given scenarios.

        NOTE: scenarios and attribute_grades may define a subset of
            data columns in input data files, if not all variants are to be analyzed.
            MUST be specified EXACTLY as stored in data files,
            case-sensitive, i.e., 'A', and 'a' are different categories.
            If needed, the EmaDataSet.load(...) method allows
            argument 'converters' to pandas reader function,
            defining a dict with function(s) to make saved data fields agree with pre-defined categories.
            Column headers in the data files may also be re-named, if needed,
            as specified by argument rename_cols to the EmaDataSet.load(...) method.
        """
        self.phase_key = phase_key
        if scenarios is None:
            scenarios = dict()
        else:
            scenarios = dict(scenarios)
        if self.phase_key not in scenarios.keys():
            scenarios[self.phase_key] = ('',)  # just a single category
        scenarios = dict((sc, pd.CategoricalDtype(categories=sc_list,
                                                  ordered=False))
                         for (sc, sc_list) in scenarios.items())
        # = allowing mixed types for categories, e.g., strings, integers
        # re-order to ensure first scenario key == self.phase_key:
        phase_dict = {self.phase_key: scenarios.pop(self.phase_key)}
        self.scenarios = phase_dict | scenarios  # **** requires python >= 3.9

        if attribute_grades is None:
            attribute_grades = dict()
        else:
            attribute_grades = dict(attribute_grades)
        self.attribute_grades = dict((a, pd.CategoricalDtype(categories=a_list,
                                                             ordered=True))
                                     for (a, a_list) in attribute_grades.items())
        # = allowing mixed types for categories, e.g., strings, integers

    def __repr__(self):
        return (self.__class__.__name__ + '(\n\t\t' +
                ',\n\t\t'.join(f'{key}={repr(v)}'
                               for (key, v) in vars(self).items()) +
                '\n\t\t)')

    @property
    def dtypes(self):
        """
        :return: dict with all defined ema variable types
        """
        return self.scenarios | self.attribute_grades

    @property
    def scenario_shape(self):
        """tuple with number of nominal categories for each scenario factor"""
        return tuple(len(sc_cat.categories)
                     for sc_cat in self.scenarios.values())

    @property
    def n_scenarios(self):  # **** needed ?
        return np.prod(self.scenario_shape, dtype=int)

    # def n_categories(ema_dim) for any scenario or attribute ???

    def scenario_axes(self, sc):
        """
        :param sc: sequence of one or more scenario keys
        :return: tuple of corresponding numerical axes
        """
        sc_keys = list(self.scenarios.keys())
        sc_ind = []
        for sc_i in sc:
            try:
                sc_ind.append(sc_keys.index(sc_i))
            except ValueError:
                logger.warning(f'{repr(sc_i)} is not a scenario key')
        return sc_ind

    @property
    def rating_shape(self):
        """tuple with number of ordinal response levels for each attribute
        """
        return tuple(len(r_cat.categories)
                     for r_cat in self.attribute_grades.values())

    @property
    def n_phases(self):
        # == scenario_shape[0]
        return len(self.scenarios[self.phase_key].categories)

    def required_vars(self):
        return [*self.scenarios.keys()] + [*self.attribute_grades.keys()]

    def required_types(self):
        return self.scenarios | self.attribute_grades

    def filter(self, ema):
        """Check and filter EMA data for ONE subject, to ensure that
        it includes the required columns, with required data types.
        :param ema: a pd.DataFrame instance
        :return: a pd.DataFrame instance with complete data
            or an empty DataFrame if no usable EMA records were found
        """
        try:
            ema = ema[self.required_vars()]
            ema = ema.astype(self.required_types(), errors='raise')
            # *** this sets NaN if cell contents not in defined categories ***
            # if np.any(ema.isna()):
            #     logger.warning('Some input data is NaN:\n'
            #                    + str(ema.head(10)))
            # # ******* delete rows with NaN not needed? NaNs excluded by DataFrame.value_counts()
        except KeyError as e:
            raise FileReadError(f'Some missing required data column(s). Error {e}')
        except ValueError as e:
            raise FileReadError(f'Incompatible data type. Error {e}')
        return ema

    # def scenario_index(self, r):  # ************************** needed?
    #     """Encode an EMA record into an index tuple identifying the scenario
    #     :param r: dict with (key, value) pairs of scenarios and attribute_grades
    #     :return: sc_i = tuple (k_0, k_1, k_2, ...), where
    #         k_0 = test-phase index,
    #         k_i = index of i-th scenario
    #         len(sc_i) == len(self.scenarios)
    #     """
    #     try:
    #         return tuple(_index_matching(sc_list, r[sc_key])
    #                      for (sc_key, sc_list) in self.scenarios.items())
    #     except (KeyError, ValueError):
    #         return None

    def count_scenarios(self, ema):
        """Count EMA scenario occurrences for analysis
        :param ema: np.DataFrame instance with all EMA records for ONE respondent,
            with columns including self.scenarios.keys()
        :return: z = mD array with scenario_counts
            z[k0, k1,...] = number of recordings in (k0, k1,...)-th scenario category
            z.shape == self.scenario_shape
        """
        # 2022-05-24, Arne Leijon: verified manually with input data
        z = ema.value_counts(subset=list(self.scenarios.keys()), sort=False)
        # = pd.Series including only non-zero counts, indexed by scenario or tuple(scenarios)
        ind = pd.MultiIndex.from_product([sc.categories
                                          for sc in self.scenarios.values()])
        # ind as EmaFrame method?
        z = z.reindex(index=ind, fill_value=0)
        # must reindex to include zero counts
        # ****** use z.to_numpy ? *********
        return np.array(z).reshape(self.scenario_shape)

    # def rating_index(self, r):  # *************************** needed?
    #     """Encode an EMA record into an index tuple identifying rating responses
    #     :param r: dict with (key, value) pairs of scenarios and attribute_grades
    #     :return: y = tuple, with
    #         y[i] = scalar integer = ordinal value of i-th rating response
    #         y[i] = None, if response is missing
    #         len(y) == len(self.attribute_grades)
    #     """
    #     try:
    #         return tuple(_index_matching(r_list, r[r_key])
    #                      for (r_key, r_list) in self.attribute_grades.items())
    #     except (KeyError, ValueError):
    #         return None

    def count_grades(self, a, ema):
        """Count grade occurrences for given attribute
        :param a: attribute key
        :param ema: np.DataFrame instance with all EMA records for ONE respondent,
            with columns including all self.scenarios.keys() and self.attribute_grade.keys()
        :return: y = 2D array with
            y[l, k] = number of responses at l-th ordinal level,
            given k-th <=> (k0, k1, ...)-th scenario category
        """
        # 2022-05-24, Arne Leijon: verified manually with input data
        z = ema.value_counts(subset=[a] + list(self.scenarios.keys()), sort=False)
        ind = pd.MultiIndex.from_product([self.attribute_grades[a].categories]
                                         + [sc.categories
                                            for sc in self.scenarios.values()])
        z = z.reindex(index=ind, fill_value=0)
        return np.array(z).reshape((ind.levshape[0], -1))


# ------------------------------------------------------------
class EmaDataSet:
    """Container of all data input for one complete EMA study.
    """
    def __init__(self, emf, groups):
        """
        :param emf: an EmaFrame instance
        :param groups: dict with elements (group_id: group_dict), where
            group_id = tuple with one or more pairs (g_factor, g_category),
                identifying the sub-population,
            group_dict = dict with elements (subject, ema_df), where
            ema_df = a pd.DataFrame instance with one column for each variable,
            and one row for each EMA record.
            ema_df.shape == (n_records, n Scenario dimensions + n Attributes)
        """
        self.emf = emf
        self.groups = groups

    def __repr__(self):
        def sum_n_records(g_subjects):
            """Total number of EMA records across all subjects in group"""
            return sum(len(s_ema) for s_ema in g_subjects.values())
        # ---------------------------------------------------------------
        return (self.__class__.__name__ + '(\n\t'
                + f'emf= {self.emf},\n\t'
                + 'groups= {' + '\n\t\t'
                + '\n\t\t'.join((f'{g}: {len(g_subjects)} subjects '
                                 + f'with {sum_n_records(g_subjects)} EMA records in total,')
                                for (g, g_subjects) in self.groups.items())
                + '\n\t\t})')

    # *** separate classmethod initialize, method add; load = initialize + add

    @classmethod
    def load(cls, emf, path,
             subject='file',
             grouping=None,
             fmt=None,
             ema_vars=None,
             **kwargs):
        """Create one class instance with selected data from input files.
        :param emf: EmaFrame instance
        :param path: string or Path defining top of directory tree with all data files
        :param subject: string defining where to find subject ID in specific file object,
            = 'file', column name, or 'sheet' if fmt == xlsx
        :param grouping: (optional) dict or iterable with elements (group_dim, category_list),
            where
            group_dim is a string label identifying one "dimension" of sub-populations,
            category_list is a list of labels for allowed categories within group_factor.
            If None, only ONE (unnamed) group is included.
        :param fmt: (optional) string with file suffix for accepted data files.
            If None, all files are tried, so mixed file formats can be used as input.
        :param ema_vars: (optional) *** only for warning, no longer used
        :param kwargs: (optional) any additional arguments for pandas file_reader
        :return: a single cls object

        NOTE: Scenario and Attribute grades in input files must agree EXACTLY
            with categories defined in emf.
            Use argument 'converters' to pandas reader function
            with function(s) to make saved data fields agree with pre-defined categories.
            Use argument 'rename_cols' to translate file column headers to desired names.
        """
        if ema_vars is not None:  # warning for backwards incompatibility
            logger.warning('EmaCalc v. >= 0.9: ema_vars not used to select EMA variables. '
                           + 'Using file header instead. \n'
                           + 'Change column names by "rename_cols" argument, if needed.')
        path = Path(path)
        if grouping is None:
            grouping = dict()
        else:
            grouping = dict(grouping)
        groups = {g: dict() for g in _groups(grouping)}
        # = dict with empty dict for subjects in each group
        # **** up to here -> classmethod initialize
        # **** following: -> add method, to allow collecting data from different file formats ?
        ema_types = emf.scenarios | emf.attribute_grades  # = emf.required_types()
        if emf.n_phases == 1:  # might cause error trying to read it from file(s)
            ema_types.pop(emf.phase_key)
        for (g, g_path) in _gen_group_file_paths(path, fmt, [*grouping.items()]):
            logger.info(f'Reading {g_path}')
            try:
                ema_file = ema_gen(g_path,
                                   subject=subject,
                                   **kwargs)
                for (s, ema) in ema_file:
                    # add phase if only one allowed and not specified in the file
                    # *** what if several are specified in file, but only one used ? ********
                    if emf.n_phases == 1:  # *** check for phase-code unspecified ? ******
                        ema[emf.phase_key] = emf.scenarios[emf.phase_key].categories[0]
                    ema = emf.filter(ema) # ensure it conforms to given emf
                    logger.info(f'Subject {repr(s)}: {ema.shape[0]} EMA records. '
                                + ('Some missing data. Valid data count =\n'
                                   + _table_valid(ema) if np.any(ema.isna()) else ''))
                    # if np.any(ema.isna()):
                    #     logger.debug(f'Subject {repr(s)} ({ema.shape[0]} records): '
                    #                    + 'Missing data count =\n'
                    #                    + _table_missing(ema))
                    # ******* delete rows with NaN not needed!
                    # NaNs excluded later by pandas.DataFrame.value_counts()
                    logger.debug(f'Subject {repr(s)}:\n' + ema.to_string())
                    if not ema.empty:
                        if s not in groups[g]:
                            groups[g][s] = ema
                        else:
                            groups[g][s] = pd.concat(groups[g][s], ema)
            except FileReadError as e:
                logger.warning(e)  # and just try next file
        return cls(emf, groups)

    # def add method, to include data from new files with different layout ???

    def save(self, dir, allow_over_write=False, fmt='csv', **kwargs):  # *******
        """Save self.groups in a directory tree with one folder for each group,
        with one file for each subject.
        :param dir: Path or string defining the top directory where files are saved
        :param allow_over_write: boolean switch, over-write files if True
        :param fmt: string label specifying file format
        :return: None
        """
        # *** allow save as ONE big pd.DataFrame instance ? *********
        dir = Path(dir)
        for (g, group_data) in self.groups.items():
            g = _dir_name(g, '/')
            if len(g) == 0:
                g_path = dir
            else:
                g_path = dir / g
            g_path.mkdir(parents=True, exist_ok=True)
            for (s_id, s_df) in group_data.items():
                try:
                    p = (g_path / str(s_id)).with_suffix('.' + fmt)  # one file per subject
                    Table(s_df).save(p, allow_over_write, **kwargs)
                except FileWriteError as e:
                    raise RuntimeError(f'Could not save {self.__class__.__name__} in {repr(fmt)} format. '
                                       + f'Error: {e}')

    def ensure_complete(self):
        """Check that we have at least one subject in every sub-population category,
        with at least one ema record for each subject (already checked in load method).
        :return: None

        Result:
        self.groups may be reduced:
        subjects with no records are deleted,
        groups with no subjects are deleted
        logger warnings for missing data.
        """
        for (g, g_subjects) in self.groups.items():
            incomplete_subjects = set(s for (s, s_ema) in g_subjects.items()
                                      if len(s_ema) == 0)
            for s in incomplete_subjects:
                logger.warning(f'No EMA data for subject {repr(s)} in group {repr(g)}. Deleted!')
                del g_subjects[s]
        incomplete_groups = set(g for (g, g_subjects) in self.groups.items()
                                if len(g_subjects) == 0)
        for g in incomplete_groups:
            logger.warning(f'No subjects in group {repr(g)}. Deleted!')
            del self.groups[g]
        if len(self.groups) == 0:
            raise RuntimeError('No EMA data in any group.')
        for attr in self.emf.attribute_grades.keys():
            a_count = self.attribute_grade_distribution(attr)
            # = pd.DataFrame with all groups, all subjects
            _check_ratings(attr, a_count)

    def join_df(self):
        """Join all EMA data into ONE single pd.DataFrame instance
        for all groups and all subjects
        :return: a single pd.DataFrame instance
        """
        df_list = []
        for (g_tuple, g_data) in self.groups.items():
            for (s, s_ema) in g_data.items():
                df = Table(s_ema.copy())
                df['Subject'] = s
                for g in g_tuple:
                    df[g[0]] = g[1]
                df_list.append(df)
        return pd.concat(df_list, ignore_index=True)

    def attribute_grade_distribution(self, a, group_by=None):
        """Collect distribution of grades for ONE attribute,
        for each (group, subject), optionally sub-divided by scenario
        :param a: selected attribute key
        :param group_by: (optional) single scenario dimension or sequence of such keys
            for which separate attribute-means are calculated.
            Results are aggregated across any OTHER scenario dimensions.
        :return: a pd.DataFrame object with all grade counts,
            with one row for each (group, subject, group_by case
        """
        if group_by is None:
            group_by = []
        elif group_by in self.emf.scenarios.keys():
            group_by = [group_by]
        else:
            group_by = list(group_by)
        df = self.join_df()
        g_cols = list(set([g[0] for g_tuple in self.groups.keys() for g in g_tuple]))
        if len(g_cols) == 1 and len(g_cols[0]) == 0:
            g_cols = []
        group_by = g_cols + ['Subject'] + group_by
        df_count = df.groupby(group_by)[a].value_counts(sort=False).unstack()
        return Table(df_count)

    def mean_attribute_table(self, a=None, group_by=None):
        """Average raw attribute grades, encoded numerically as (1,.., n_grades)
        :param a: (optional) attribute label or sequence of attribute,
            if None, include all attributes
        :param group_by: (optional) single scenario dimension or iterable of such keys
            for which separate attribute-means are calculated.
            Results are aggregated across any OTHER scenario dimensions.
        :return: a pd.DataFrame instance with all mean Attribute grades,
            with rows Multi-indexed for Group(s), Subject, and selected Scenario dimensions.
            with one column for selected attribute(s).
        """
        def recode_attr(df, a):
            """Recode ordinal attribute grades to numerical (1,...,n_grades)
            :param df: a pd.DataFrame instance
            :param a: list of attribute column names in df
            :return: None; df recoded in place
            """
            # *** allow external user-defined recoding function ?
            for a_i in a:
                c = df[a_i].array.codes.copy().astype(float)
                c[c < 0] = np.nan
                df[a_i] = c + 1
        # -------------------------------------------
        if a is None:
            a = list(self.emf.attribute_grades.keys())
        elif isinstance(a, str):  # a in self.emf.attribute_grades.keys():
            a = [a]
        a = [a_i for a_i in a if a_i in self.emf.attribute_grades.keys()]
        if group_by is None:
            group_by = []
        elif isinstance(group_by, str):  # in self.emf.scenarios.keys():
            group_by = [group_by]
        group_by = [gb for gb in group_by if gb in self.emf.scenarios.keys()]
        df = self.join_df()
        g_cols = list(set([g[0] for g_tuple in self.groups.keys() for g in g_tuple]))
        if len(g_cols) == 1 and len(g_cols[0]) == 0:
            g_cols = []
        group_by = g_cols + ['Subject'] + group_by
        recode_attr(df, a)  # in place
        return Table(df.groupby(group_by).mean())

    def nap_table(self, sc=None, nap_cat=None,
                  a=None, group_by=None, p=0.95):
        """Calculate proportion of Non-overlapping Pairs = NAP result
        in ONE scenario dimension with EXACTLY TWO categories, X and Y,
        = estimate of P(attribute grade in X < attribute grade in Y),
        given observed ordinal i.i.d. grade samples for attribute in scenarios X and Y.
        :param sc: ONE scenario dimension with TWO categories to be compared
        :param nap_cat: (optional) sequence of TWO categories (X, Y) in scenario dimension sc.
            If None, sc MUST be categorical with exactly TWO categories.
        :param a: (optional) attribute name or list of attribute names
        :param group_by: (optional) single scenario key or iterable of such keys
            for which separate NAP results are calculated.
            Results are aggregated across any OTHER scenario dimensions.
        :param p: (optional) scalar confidence level for NAP result
        :return: a pd.DataFrame instance with all NAP results,
            with rows Multi-indexed for Group(s), Subject, grouping Scenario-dimension(s),
            columns Multi-indexed with three NAP results for each Attribute:
            (lower conf-interval limit, point estimate, upper conf-interval limit)
        """
        if a is None:
            a = list(self.emf.attribute_grades.keys())
        elif isinstance(a, str):  # single attribute
            a = [a]
        a = [a_i for a_i in a
             if a_i in self.emf.attribute_grades.keys()]
        if group_by is None:
            group_by = []
        elif isinstance(group_by, str):
            group_by = [group_by]
        group_by = [gb for gb in group_by if gb in self.emf.scenarios.keys()]
        df = self.join_df()
        g_cols = list(set([g[0] for g_tuple in self.groups.keys() for g in g_tuple]))
        if len(g_cols) == 1 and len(g_cols[0]) == 0:
            g_cols = []
        group_by = g_cols + ['Subject'] + group_by
        return Table(nap_pandas(df, col=sc, nap_cat=nap_cat,
                                group_cols=group_by, grade_cols=a, p=p))


# -------------------------------------------- module help functions

def _dir_name(g, sep='_'):  # ***
    """Convert group id to a directory path string
    :param g: string or tuple of strings
    :return: string to be used as directory path
    """
    if type(g) is tuple:  # one or more (g_factor, g_cat) tuples
        g = sep.join(_dir_name(g_s, sep='_')
                     for g_s in g)
    return g


def _groups(group_factors):
    """Generate group labels from group_factors tree
    :param group_factors: dict or iterable with elements (group_factor, category_list),
    :return: generator of all combinations of (gf, gf_category) pairs from each group factor
        Generated pairs are sorted as in group_factors
    """
    if len(group_factors) == 0:  # NO grouping
        return [tuple()]  # ONE empty group label
    else:
        return product(*(product([gf], gf_cats)
                         for (gf, gf_cats) in group_factors.items())
                       )


def _gen_group_file_paths(path, fmt, group_factors, g_tuple=()):
    """Generator of group keys and corresponding file Paths, recursively, for all groups
    :param path: Path instance defining top directory to be searched
    :param fmt: file suffix of desired files
    :param group_factors: list of tuples (g_factor, labels)
    :param g_tuple: list of tuples (g_factor, factor_label),
        defining a combined group label or a beginning of a complete such label
    :return: generator of tuples (group_key, file_path), where
        group_key is an element of emf.groups,
        file_path is a Path object to a file that may hold count data for the group.
    """
    # exclude files like .xxx and require exact suffix match ************
    def file_ok(f):
        """Check if file is acceptable
        :param f: file path
        :return: True if acceptable
        """
        if fmt is None:
            return f.stem[0] != '.'
        else:
            return fmt == f.suffix[1:] and f.stem[0] != '.'
    # ----------------------------------------------------

    for f in path.iterdir():
        if len(group_factors) == 0:  # now at lowest grouping level in directory tree
            if f.is_file():  # include all files here and in sub-directories
                if file_ok(f):  # fmt in f.suffix:
                    # print(f'Reading file {f}')
                    yield g_tuple, f
            elif f.is_dir():  # just search sub-tree recursively
                yield from _gen_group_file_paths(f, fmt,
                                                 group_factors,
                                                 g_tuple)
        else:  # len(grouping) >=1
            g_factor_key = group_factors[0][0]
            for g_cat in group_factors[0][1]:
                factor_cat = (g_factor_key, g_cat)
                # = new tuple to be included in final group label
                if f.is_dir():
                    # if f.name.find(g_cat) == 0:
                    if (f.name.find(g_factor_key) == 0
                            and f.name.find(g_cat) == len(g_factor_key) + 1):
                        # iterate recursively in sub-directory
                        yield from _gen_group_file_paths(f, fmt,
                                                         group_factors[1:],
                                                         (*g_tuple, factor_cat))
                elif f.is_file() and len(group_factors) == 1:
                    # at final sub-directory level, also accept group category in file name:
                    if (g_factor_key in f.name) and (g_cat in f.name) and file_ok(f):  # fmt in f.suffix:
                        # print(f'Reading file {f}')
                        yield (*g_tuple, factor_cat), f


def _table_valid(ema: pd.DataFrame):
    """Count valid data elements for all columns
    :param ema: Pandas.DataFrame instance with input EMA data
    :return: table string for logger output
    """
    return pd.DataFrame([ema.count()]).to_string(index=False)


def _table_missing(ema: pd.DataFrame):  # *** needed ?
    """make logger warning
    :param ema: Pandas.DataFrame instance with input EMA data
    :return: string for logger output
    """
    missing = pd.DataFrame({key: [sum(val.isna())]
                            for key, val in ema.iteritems()})
    return missing.to_string(index=False)


def _check_ratings(a, a_count):
    """Warning about zero rating counts in some categories
    :param a: attribute key
    :param a_count: pd.DataFrame with count distribution for this attribute
    :return: None
    """
    max_zero = 0.5  # proportion of all subjects
    n_rows = a_count.shape[0]
    zero_subjects = np.sum(a_count.to_numpy() == 0, axis=0)
    if np.any(zero_subjects == n_rows):
        logger.warning(f'Attribute {a}: Some grades unused by ALL subjects! '
                       + 'Consider merging grades?\n\t'
                       + f'{a} grades=\n'
                       + a_count.to_string())
    elif np.any(zero_subjects > max_zero * n_rows):
        logger.warning(f'Attribute {a}: Some grades unused by some subjects! '
                       + 'Consider merging grades?')


# -------------------------------------------- TEST:
if __name__ == '__main__':
    import ema_logging
    # ------------------------ Set up working directory and result logging:
    work_path = Path.home() / 'Documents' / 'EMA_sim'  # or whatever...
    data_path = work_path / 'data'  # to use simulation data generated by run_sim.py
    # result_path = work_path / 'result'  # or whatever

    # model_file = 'test_ema_model.pkl'  # name of saved model file (if saved)

    ema_logging.setup()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # ------ 1: Define Experimental Framework: Scenarios, Attributes, and Grades

    # NOTE: This example uses data generated by template script run_sim.py
    # Edit as needed for any other EMA data source

    sim_scenarios = {'phase': ('',),  # only ONE Test phase with empty label
                     'HA': ('A', 'B'),  # Two Hearing-aid programs
                     'CoSS': [f'C{i}' for i in range(1, 8)],    # Seven CoSS categories
                     }  # nominal variables, same for all (Sub-)Populations
    # NOTE: First scenario dimension is always phase, even if only ONE category
    # User may set arbitrary phase_key label
    # Dimension 'phase' may be omitted, if only one category

    emf = EmaFrame(scenarios=sim_scenarios,
                   phase_key='Phase',
                   attribute_grades={'Speech': ['Very Hard',
                                                'Hard',
                                                'Easy',
                                                'Very Easy',
                                                'Perfect'],
                                     'Comfort': ['Bad',
                                                 'Not Good',
                                                 'Not Bad',
                                                 'Good']},  # ordinal rating categories
                   )

    print('emf=\n', emf)
    print(f'emf.n_phases= {emf.n_phases}')
    print(f'emf.scenario_shape= {emf.scenario_shape}')
    print(f'emf.rating_shape= {emf.rating_shape}')

    # group_factors = {'Age': ['young', 'old'],
    #                  'Gender': ['male', 'female'],
    #                  'ORCA': ['AR_64']}
    grouping = {'Age': ('old',),  # analyze only Age=old
                }
    # grouping={'Age': ('young','old')},  # analyze both Age groups separately
    for (g, g_path) in _gen_group_file_paths(data_path, 'xlsx', [*grouping.items()]):
        print('g= ', g, ': g_path= ', g_path)

    ds = EmaDataSet.load(emf, data_path, fmt='xlsx',
                         grouping=grouping,
                         subject='file',
                         dtype={'CoSS': 'string'},
                         # converters={'CoSS': lambda c: str(c)}
                         )
    print('ds= ', ds)

    test = ds.mean_attribute_table(group_by=('HA', 'CoSS'))
    test.to_string(work_path / 'test_attribute_table.txt')
    print('mean_rating=\n', test)

    nap = ds.nap_table(sc='HA', group_by=('CoSS',))
    nap.to_string(work_path / 'test_nap_table.txt', float_format='%.3f')
    nap.to_latex(work_path / 'test_nap_table.tex', float_format='%.2f')
    # Styler(nap, precision=3).to_latex(work_path / 'test_nap_table.txt')
    print('NAP(HA B > A)=\n', nap)

    # ***** TEST Empty scenarios or Empty attribute_grades ***********
