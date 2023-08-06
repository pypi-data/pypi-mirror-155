import collections
import configparser
import enum
import functools
import inspect
import itertools
import math
import pathlib
import pickle
import re
import statistics
import typing

import numpy
import pandas

from immunogen.utils.MetaLogger import MetaLogger

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources


class SequenceType(enum.Enum):
    """
    Allele Sequence Type Handler
    """
    ALIGNED = 0
    ALLELE = 1


class ImmunogenicityUtils(metaclass=MetaLogger):
    """
    Immunogenicity utilities to handle calculating mismatch scores between
    individuals.

    """

    def __init__(self):
        self._allele_conversions = None
        self._allele_mappings = None
        self._aligned_sequences = None
        self._allele_sequences = None
        self._config = None
        self._amino_acids = None
        self._haplotype_frequencies = None

    @property
    def config(self) -> typing.Dict:
        """
        Returns a data dictionary of configuration parameters.

        Returns
        -------
        dictionary
            A dictionary of configuration parameters and their associated
            values.
        """
        if self._config is None:
            try:
                self._make_config()
            except FileNotFoundError:
                self.__logger.error("No configuration file found.")
        return self._config

    @config.setter
    def config(
        self, value: typing.Optional[typing.Union[str, pathlib.Path]]
    ) -> configparser.ConfigParser():
        """
        Set the file path source for configuration file before calling
        :meth:`_make_config` to build the configuration parameters.

        Parameters
        ----------
        value
            str or Path-like representation of INI file containing configuration
            parameters.
        """
        if value is None:
            value = pathlib.Path(__file__).parent.parent / "config.ini"
        elif value is str:
            value = pathlib.Path(value)
        config = configparser.ConfigParser(allow_no_value=True)

        if len(config.read(value)) > 0:
            self._config = config
        else:
            raise FileNotFoundError

    def _make_config(self, value=None):
        """
        Construct a dictionary of configuration values from an INI file.

        Parameters
        ----------
        value
            str or Path-like representation an INI file containing configuration
            parameters.
        """
        self.config = value

    def amino_acid_details(
        self, allele: str, dict_type: SequenceType = SequenceType.ALLELE
    ) -> typing.Optional[typing.Dict]:
        """
        Returns a sequence of 276 Amino Acids(AA) for the given allele where each
        AA replaced with a pair of HB and PI

        Returns a list of lists similar to the following : [

          [0.0, 5.97], [0.3, 5.68], [-0.5, 7.47], [0.3, 5.68], [-1.3, 5.74],

          [3.0, 11.15], [-2.3, 5.66], [-2.5, 5.48], [-2.5, 5.48], [-0.4, 5.64],

          [0.3, 5.68], [-1.5, 5.96], [0.3, 5.68], [3.0, 11.15], [0.0, 6.3],

          ...

          [-1.8, 5.98], [0.0, 6.3], [3.0, 9.59], [0.0, 6.3], [-1.8, 5.98],

          [-0.4, 5.64], [-1.8, 5.98], [3.0, 11.15], [-3.4, 5.89], [3.0, 3.22],

          [-1.8, 5.98]

        ]

        where each list element is a list of HB, and PI

        Parameters
        ----------
        allele
            str of target allele
        dict_type
            str of target dictionary, currently `allele` for allele
            sequences or `aligned` for aligned sequences

        Returns
        -------
        dictionary
            A dictionary of allele values with mapped amino acids and their respective
            hydrophobicity values and isoelectric points.

        """
        if dict_type == SequenceType.ALLELE:
            return self.allele_sequences.get(allele, None)
        elif dict_type == SequenceType.ALIGNED:
            return self.aligned_sequences.get(allele, None)

    @property
    def allele_sequences(
        self,
    ) -> typing.DefaultDict[str, typing.List[typing.List[float]]]:
        """
        Returns a data lookup dictionary for allele sequences.

        Produces a dictionary similar to the following: {

          'DQB1*0201' : [[3.0, 11.15], [3.0, 2.77], ...],

          'DQB1*0202' : [[3.0, 11.15], [3.0, 2.77], ...],

          ...

          'DPA1*0303' : [[-0.5, 6.0], [0.0, 5.97], ...],

          'DPA1*0401' : [[-0.5, 6.0], [0.0, 5.97], ...],

        }

        where keys are alleles and the list is an ordered sequence of their
        amino acid hydrophobicity value and isoelectric point respectively.

        Returns
        -------
        dictionary
            A dictionary of alleles and their associated sequence of amino acid
            HB and PI values.
        """
        if self._allele_sequences is None:
            try:
                file = pkg_resources.open_binary(
                    "immunogen.data.pickles", "allele_sequences.p"
                )
                self._allele_sequences = pickle.load(file)
                file.close()
            except (ValueError, FileNotFoundError):
                self.__logger.info(
                    f"No pickle found, building {inspect.stack()[0][3]} from source."
                )
                self.allele_sequences = None
        return self._allele_sequences

    @allele_sequences.setter
    def allele_sequences(self, value: typing.Union[str, pathlib.Path]) -> None:
        """
        Set the directory path source for allele sequence definitions before
        calling :meth:`_make_allele_sequences` to build the dictionary
        representation. Additionally, a new pickle file is generating using the
        updated file definitions to reduce future computation time.

        Parameters
        ----------
        value
            str or Path-like representation of directory containing CSV files
            with definitions for allele sequences. Each file is assumed to be of
            the form:

                DPA1*0103,DPA1*0104,...,DPA1*0303,DPA1*0401

            where each column is an allele and the following rows represent the
            amino acid sequence of the respective allele.

        """
        if value is None:
            value = pathlib.Path(__file__).parent.parent / self.config.get(
                "immunogenicity", "allele_sequences"
            )
        self._make_allele_sequences(ref_data=value)
        pickle.Pickler(
            open((pathlib.Path("../../../immunogen/immunogen/data/pickles") / "allele_sequences.p"), "wb"),
            protocol=pickle.HIGHEST_PROTOCOL,
        ).dump(self.allele_sequences)

    def _make_allele_sequences(
        self,
        ref_data: typing.Union[str, pathlib.Path] = None,
    ) -> None:
        """
        Construct a dictionary of allele values with ordered sequence of amino
        acid hydrophobicity values and isoelectric points.

        Parameters
        ----------
        ref_data
            str or Path-like representation of directory of CSV file/s or a CSV
            file containing definitions for amino acids.
        """
        seq_dic = {}
        self._allele_sequences = collections.defaultdict(list)
        if type(ref_data) is str:
            ref_data = pathlib.Path(ref_data)
        if ref_data.is_dir():
            files = ref_data.glob("*.csv")
        else:
            files = ref_data
        for file in files:
            seq_dataframe = pandas.read_csv(file)
            for allele_sequence in seq_dataframe.columns:
                if allele_sequence not in seq_dic:
                    seq_dic[allele_sequence] = []
                seq_dic[allele_sequence].append(seq_dataframe[allele_sequence])
        for alleles in seq_dic.keys():
            for amino_acids in seq_dic[alleles]:
                for amino_acid in amino_acids:
                    if amino_acid not in self.amino_acids.keys():
                        self._allele_sequences[alleles].append(None)
                    else:
                        self._allele_sequences[alleles].append(
                            self.amino_acids[amino_acid]
                        )

    @property
    def aligned_sequences(self) -> typing.Dict:
        """
        Returns a data lookup dictionary for aligned allele sequences.

        Produces a dictionary similar to the following: {

          ['A*01:01': [[0.0, 5.97], [0.3, 5.68], ...],

          'A*01:02' : [[0.0, 5.97], [0.3, 5.68], ...],

          ...

          'A*68:36': [[0.0, 5.97], [0.3, 5.68], ...],

          'A*74:11': [[0.0, 5.97], [0.3, 5.68], ...]],

        }

        where keys are alleles and the list is an ordered sequence of their
        amino acid hydrophobicity value and isoelectric point respectively.

        Returns
        -------
        dictionary
            A dictionary of aligned alleles and their associated sequence of
            amino acid HB and PI values.

        """
        if self._aligned_sequences is None:
            try:
                file = pkg_resources.open_binary(
                    "immunogen.data.pickles", "aligned_sequences.p"
                )
                self._aligned_sequences = pickle.load(file)
                file.close()
            except (ValueError, FileNotFoundError):
                self.__logger.info(
                    f"No pickle found, building {inspect.stack()[0][3]} from source."
                )
                self.aligned_sequences = None
        return self._aligned_sequences

    @aligned_sequences.setter
    def aligned_sequences(self, value: typing.Union[str, pathlib.Path]) -> None:
        """
        Set the directory path source for aligned allele sequence definitions before
        calling :meth:`_make_aligned_sequences` to build the dictionary
        representation. Additionally, a new pickle file is generating using the
        updated file definitions to reduce future computation time.

        Parameters
        ----------
        value
            str or Path-like representation of directory containing CSV files
            with definitions for allele sequences. Each file is assumed to be of
            the form:

                A*01:01,A*01:02,A*01:03,...,A*02:02,A*02:03

            where each column is an aligned allele and the following rows represent the
            amino acid sequence of the respective aligned allele.

        """
        if value is None:
            value = pathlib.Path(__file__).parent.parent / self.config.get(
                "immunogenicity", "aligned_sequences"
            )
        self._make_aligned_sequences(ref_data=value)
        pickle.Pickler(
            open((pathlib.Path("../../../immunogen/immunogen/data/pickles") / "aligned_sequences.p"), "wb"),
            protocol=pickle.HIGHEST_PROTOCOL,
        ).dump(self.aligned_sequences)

    def _make_aligned_sequences(
        self,
        ref_data: typing.Union[str, pathlib.Path] = None,
    ) -> None:
        """
        Construct a dictionary of aligned allele values with ordered sequence
        of amino acid hydrophobicity values and isoelectric points.

        Parameters
        ----------
        ref_data
            str or Path-like representation of CSV file.
        """
        aligned_seq_dic = {}
        if type(ref_data) is str:
            ref_data = pathlib.Path(ref_data)
        aligned_sequence_dataframe = pandas.read_csv(ref_data)
        for aligned_sequence in aligned_sequence_dataframe.columns:
            if aligned_sequence not in aligned_seq_dic:
                aligned_seq_dic[aligned_sequence] = []
            aligned_seq_dic[aligned_sequence].append(
                aligned_sequence_dataframe[aligned_sequence]
            )
        new_dict = collections.defaultdict(list)
        aligned_seq_dic.pop("Unnamed: 0", None)
        for alleles in aligned_seq_dic.keys():
            for amino_acids in aligned_seq_dic[alleles]:
                for amino_acid in amino_acids:
                    if amino_acid not in self.amino_acids.keys():
                        new_dict[alleles].append(None)
                    else:
                        new_dict[alleles].append(self.amino_acids[amino_acid])
        self._aligned_sequences = new_dict

    @property
    def amino_acids(self) -> typing.Dict:
        """
        Returns a data lookup dictionary for amino acids.

        Returns a dictionary similar to the following: {

          'A': [-0.5, 6.0],

          'R': [3.0, 11.15],

          'N': [0.2, 5.41],

          ...

          'W': [-3.4, 5.89],

          'Y': [-2.3, 5.66],

          'V': [-1.5, 5.96]

        }

        where keys are amino acids and the list is hydrophobicity value and
        isoelectric point respectively.

        Returns
        -------
        dictionary
            A dictionary of amino acids and their associated HB and PI values.
        """
        if self._amino_acids is None:
            try:
                file = pkg_resources.open_binary(
                    "immunogen.data.pickles", "amino_acids.p"
                )
                self._amino_acids = pickle.load(file)
                file.close()
            except (ValueError, FileNotFoundError):
                self.__logger.info(
                    f"No pickle found, building {inspect.stack()[0][3]} from source."
                )
                self.amino_acids = None
        return self._amino_acids

    @amino_acids.setter
    def amino_acids(self, value: typing.Union[str, pathlib.Path] = None) -> None:
        """
        Set the file path source for amino acid definitions before calling
        :meth:`_make_amino_acids` to build the dictionary representation.
        Additionally, a new pickle file is generating using the updated
        file definitions to reduce future computation time.

        Parameters
        ----------
        value
            str or Path-like representation of CSV file containing definitions
            for amino acids. This file is assumed to be of the form:

                AA,AA_abr,HB,PI

            where the amino acid, its abbreviation, hydrophobicity value and
            isoelectric point are present

        """
        if value is None:
            value = pathlib.Path(__file__).parent.parent / self.config.get(
                "immunogenicity", "amino_acids"
            )
        if value is str:
            value = pathlib.Path(value)
        self._make_amino_acids(value)
        pickle.Pickler(
            open(
                (
                    pathlib.Path(__file__).parent.parent
                    / "data/pickles"
                    / "amino_acids.p"
                ),
                "wb",
            ),
            protocol=pickle.HIGHEST_PROTOCOL,
        ).dump(self.amino_acids)

    def _make_amino_acids(self, ref_data: typing.Union[str, pathlib.Path] = None):
        """
        Construct a dictionary of amino acids values and
        their respective hydrophobicity values and isoelectric points.

        Parameters
        ----------
        ref_data
            str or Path-like representation of CSV file containing definitions
            for amino acids.
        """
        self._amino_acids = {}
        df = pandas.read_csv(ref_data)
        for _, amino_acids in df.iterrows():
            if amino_acids[1] not in self._amino_acids:
                self._amino_acids[amino_acids[1]] = []
            self._amino_acids[amino_acids[1]].append(amino_acids[2])
            self._amino_acids[amino_acids[1]].append(amino_acids[3])

    @staticmethod
    def is_low_allele_valid(allele: bool = True):
        """
        TODO: Currently unused imputation function preserved for future use.

        Parameters
        ----------
        allele
            allele

        Returns
        -------
        boolean
            Set to return True until future implementation.
        """
        return allele

    @staticmethod
    def is_high_allele_valid(allele: bool = True):
        """
        TODO: Currently unused imputation function preserved for future use.

        Parameters
        ----------
        allele
            allele

        Returns
        -------
        boolean
            Set to return True until future implementation.
        """
        return allele

    @staticmethod
    def split_broad_antigen(allele_str: str) -> typing.Tuple[str, str]:
        """
        Helper method for separating alleles from columns where multiple alleles
        are represented similar to the form:

            A24(9)

        as can occur in nomenclature for broad antigens.

        Parameters
        ----------
        allele_str
            string representation of broad antigen nomenclature similar to
            A23(9)

        Returns
        -------
        tuple
            Separated, formatted alleles similar to A23, A9
        """
        first_allele = allele_str[: allele_str.find("(")]
        inside_paren = allele_str[allele_str.find("(") + 1 : allele_str.find(")")]
        hla_type = "".join(re.findall(r"[A-Za-z]+", first_allele))
        second_allele = hla_type + inside_paren
        return first_allele, second_allele

    @staticmethod
    def translate_race(srtr_race: str) -> typing.Union[str, None]:
        """
        Helper method for translating race from SRTR description to shortened
        form for haplotype frequency lookups. Similar to:

            "Black or African American": "AFA",

            ...

            "White": "CAU",


        Parameters
        ----------
        srtr_race
            string representation of SRTR race description.
        Returns
        -------
        string
            Representation of haplotype frequency race.
        """
        race_dict = {
            "Black or African American": "AFA",
            "Arab or Middle Eastern": "CAU",
            "Hispanic/Latino": "HIS",
            "American Indian or Alaska Native": "NAM",
            "Asian": "API",
            "Native Hawaiian or Other Pacific Islander": "API",
            "Indian Sub-continent": "API",
            "White": "CAU",
        }
        return race_dict.get(srtr_race, None)

    @staticmethod
    def haplotype_frequency(
        allele_list: typing.List[str],
        ref_data: typing.Union[str, pathlib.Path],
    ) -> typing.Dict:
        """
        Construct an ordered hierarchical dictionary which maps A~B~DR~DQ
        haplotype to frequency.

        Parameters
        ----------
        allele_list
            list of ordered string representations for the target alleles to
            read from reference data. Similar to the form:

            ["A","B","DRB1"]

        ref_data
             str or Path-like representation of CSV file.
        Returns
        -------
        dictionary
            A hierarchical dictionary of allele combinations mapped to their
            overall frequency of appearance.
        """
        if ref_data is str:
            ref_data = pathlib.Path(ref_data)
        test = pandas.read_csv(ref_data)
        df = test.groupby(allele_list).agg({"frequency": "sum"}).reset_index()

        """
        Iterative solution to generating hierarchical dictionary that ultimately
        builds a nested dictionary similar in form to:

         'A*30:07': {'B*18:01': {
                                    'DRB1*03:01': 3.2e-08,
                                    'DRB1*11:01': 3.19e-08
                                },
                     'B*51:01': {
                                    'DRB1*03:01': 3.2e-08,
                                    'DRB1*11:01': 3.19e-08
                                },
                     'B*58:01': {
                                    'DRB1*15:03': 1.2789e-07
                                },
                     'B*81:01': {
                                    'DRB1*03:02': 1.278e-07
                                }
                    },
        """
        d = {}
        for row in df.values:
            here = d
            for elem in row[:-2]:
                if elem not in here:
                    here[elem] = {}
                here = here[elem]
            here[row[-2]] = row[-1]
        return d

    @property
    def haplotype_frequencies(self) -> typing.Dict:
        """
        Returns a data lookup dictionary for racial haplotype frequencies.

        Returns a dictionary similar to the following: {

        'CAU' : {

            'A*30:07': {

                'B*18:01': {

                    'DRB1*03:01': 3.2e-08,

                    'DRB1*11:01': 3.19e-08

                    },

                'B*51:01': {

                    'DRB1*03:01': 3.2e-08,

                    'DRB1*11:01': 3.19e-08

                    },

                'B*58:01': {

                    'DRB1*15:03': 1.2789e-07

                    },

                'B*81:01': {

                    'DRB1*03:02': 1.278e-07

                }

            },

        ...,

        }

        where keys are race categories and hierarchical dictionary maps
        A~B~DR~DQ haplotype to frequency.

        Returns
        -------
        dictionary
            A hierarchical dictionary of racial categories with associated
            allele combinations mapped to their overall frequency of appearance.

        """
        if self._haplotype_frequencies is None:
            try:
                file = pkg_resources.open_binary(
                    "immunogen.data.pickles", "haplotype_frequencies.p"
                )
                self._haplotype_frequencies = pickle.load(file)
                file.close()
            except (ValueError, FileNotFoundError):
                self.__logger.info(
                    f"No pickle found, building {inspect.stack()[0][3]} from source."
                )
            self.haplotype_frequencies = None
        return self._haplotype_frequencies

    @haplotype_frequencies.setter
    def haplotype_frequencies(self, value: typing.Union[str, pathlib.Path]):
        """
        Set the directory path source for haplotype frequency definitions before
        calling :meth:`_make_haplotype_frequencies` to build the dictionary
        representation. Additionally, a new pickle file is generating using the
        updated file definitions to reduce future computation time.

        Parameters
        ----------
        value
            str or Path-like representation of directory containing CSV files
            with definitions for haplotype frequencies. Each file is assumed to
            be of the form:

                A,C,B,DRB3/4/5,DRB1,DQB1,frequency,count,

            where each row is an allele combination, frequency factor, and count.

        """
        if value is None:
            value = pathlib.Path(__file__).parent.parent / self.config.get(
                "immunogenicity", "haplotype_frequencies"
            )
        self._make_haplotype_frequencies(ref_data=value)
        with open((pathlib.Path(__file__).parent.parent / 'data/pickles' / "haplotype_frequencies.p"), "wb") as file:
            pickle.Pickler(
                file,
                protocol=pickle.HIGHEST_PROTOCOL,
            ).dump(self.haplotype_frequencies)

    def _make_haplotype_frequencies(
        self,
        ref_data: typing.Union[str, pathlib.Path] = pathlib.Path(
            "../data/haplotype_frequencies"
        ),
    ) -> None:
        """
        Construct a dictionary of racial haplotype frequencies.

        Parameters
        ----------
        ref_data
            str or Path-like representation of directory of CSV file/s or a CSV
            file containing definitions for amino acids.
        """
        self._haplotype_frequencies = {}
        if type(ref_data) is str:
            ref_data = pathlib.Path(ref_data)
        if ref_data.is_dir():
            files = ref_data.glob("*.csv")
        else:
            files = ref_data
        for filename in files:
            if filename.stem not in self._haplotype_frequencies:
                self._haplotype_frequencies[filename.stem] = self.haplotype_frequency(
                    ["A", "B", "DRB1"], filename
                )

    @property
    def allele_mappings(self):
        """
        Returns a data lookup dictionary for alleles mapped to WHO assigned
        type. Similar to the following : {

            'A9': {'A23', 'A24'},

            'A10': {'A66', 'A25', 'A34', 'A26'},

            ...

            'DQ1': {'DQ6', 'DQ5'},

            'DQ3': {'DQ7', 'DQ8', 'DQ9'}

        }

        Returns
        -------
        dictionary
            A dictionary of HLA alleles containing parentheses(broad antigens)
            to WHO assigned type.
        """
        if self._allele_mappings is None:
            try:
                file = pkg_resources.open_binary(
                    "immunogen.data.pickles", "allele_mappings.p"
                )
                self._allele_mappings = pickle.load(file)
                file.close()
            except (ValueError, FileNotFoundError):
                self.__logger.info(
                    f"No pickle found, building {inspect.stack()[0][3]} from source."
                )
                self.allele_mappings = None
        return self._allele_mappings

    @allele_mappings.setter
    def allele_mappings(self, value):
        """
        Set the file path source for allele mappings before calling
        :meth:`_make_allele_mappings` to build the dictionary representation.
        Additionally, a new pickle file is generating using the updated
        file definitions to reduce future computation time.

        Parameters
        ----------
        value
            str or Path-like representation of CSV file containing definitions
            for amino acids. This file is assumed to be of the form:

                HLA_allele, Expert, Who

            where the Allele, expert assigned type, and WHO assigned type are
            present

        """
        if value is None:
            value = pathlib.Path(__file__).parent.parent / self.config.get(
                "immunogenicity", "allele_mappings"
            )
        if value is str:
            value = pathlib.Path(value)
        self._make_allele_mappings(value)
        pickle.Pickler(
            open(
                (
                    pathlib.Path(__file__).parent.parent
                    / "data/pickles"
                    / "allele_mappings.p"
                ),
                "wb",
            ),
            protocol=pickle.HIGHEST_PROTOCOL,
        ).dump(self.allele_mappings)

    def _make_allele_mappings(
        self,
        ref_data: typing.Union[str, pathlib.Path] = None,
    ) -> None:
        """
        Construct a dictionary of allele to WHO assigned type mappings.

        Parameters
        ----------
        ref_data
            str or Path-like representation of CSV file.
        """
        self._allele_mappings = {}
        if ref_data is str:
            ref_data = pathlib.Path(ref_data)
        dictionary_reference = pandas.read_csv(ref_data)
        for _, row in dictionary_reference.iterrows():
            allele_sets = [allele.strip() for allele in row[2].split("/")]
            for allele_set in allele_sets:
                if "(" in allele_set:
                    first_allele, second_allele = self.split_broad_antigen(allele_set)
                    if second_allele not in self._allele_mappings:
                        self._allele_mappings[second_allele] = set()
                    self._allele_mappings[second_allele].add(first_allele)

    @property
    def allele_conversions(self):
        """
        Returns a data lookup dictionary for alleles mapped to expert assigned
        type. Similar to the following: {

            'A203': ['A*02:03'],

            'A210': ['A*02:10'],

            ...

            'DQ3': ['DQB1*03:06', 'DQB1*03:10', 'DQB1*03:14'],

            'DQ4': ['DQB1*04:01', 'DQB1*04:02']

        }

        Returns
        -------
        dictionary
            A dictionary of HLA alleles containing alleles to expert assigned
            type.

        """
        if self._allele_conversions is None:
            try:
                file = pkg_resources.open_binary(
                    "immunogen.data.pickles", "allele_conversions.p"
                )
                self._allele_conversions = pickle.load(file)
                file.close()
            except (ValueError, FileNotFoundError):
                self.__logger.info(
                    f"No pickle found, building {inspect.stack()[0][3]} from source."
                )
                self.allele_conversions = None
        return self._allele_conversions

    @allele_conversions.setter
    def allele_conversions(self, value: typing.Union[str, pathlib.Path] = None):
        """
        Set the file path source for allele conversions before calling
        :meth:`_make_allele_mappings` to build the dictionary representation.
        Additionally, a new pickle file is generating using the updated
        file definitions to reduce future computation time.

        Parameters
        ----------
        value
            str or Path-like representation of CSV file containing definitions
            for amino acids. This file is assumed to be of the form:

                HLA_allele, Expert, Who

            where the Allele, expert assigned type, and WHO assigned type are
            present

        """
        if value is None:
            value = pathlib.Path(__file__).parent.parent / self.config.get(
                "immunogenicity", "allele_conversions"
            )
        if value is str:
            value = pathlib.Path(value)
        self._make_allele_conversions(value)
        pickle.Pickler(
            open(
                (
                    pathlib.Path(__file__).parent.parent
                    / "data/pickles"
                    / "allele_conversions.p"
                ),
                "wb",
            ),
            protocol=pickle.HIGHEST_PROTOCOL,
        ).dump(self.allele_conversions)

    def _make_allele_conversions(
        self,
        ref_data: typing.Union[str, pathlib.Path] = None,
    ) -> None:
        """
        Construct a dictionary of allele to expert assigned type mappings.

        Parameters
        ----------
        ref_data
            str or Path-like representation of CSV file.
        """
        self._allele_conversions = {}
        dictionary_reference = pandas.read_csv(ref_data)

        for _, row in dictionary_reference.iterrows():
            blank_modified_allele = "blank" + (row[0].split("*"))[0]
            if blank_modified_allele not in self._allele_conversions:
                self._allele_conversions[blank_modified_allele] = []
            self._allele_conversions[blank_modified_allele].append(row[0])
            if "/" in row[1]:
                alleles = [
                    stripped_allele.strip() for stripped_allele in row[1].split("/")
                ]
            else:
                alleles = [row[1].strip()]

            for allele in alleles:
                if self.is_low_allele_valid(allele) and self.is_high_allele_valid(
                    allele
                ):
                    modified_allele = allele
                    if modified_allele.lower() == "blank":
                        modified_allele = modified_allele.lower() + row[0][0]
                    if modified_allele not in self._allele_conversions:
                        self._allele_conversions[modified_allele] = []
                    self._allele_conversions[modified_allele].append(row[0])

    @staticmethod
    def impute_haplotype_pairs(two_haplotypes: typing.List[str]) -> typing.List[str]:
        """
        Replace the Null value HLA with the other one, if one of the two HLAs
        of same type does not have value

        Parameters
        ----------
        two_haplotypes
            pair of haplotypes to check for Null values.

        Returns
        -------
        list
            original haplotypes or imputed replacement haplotypes
        """
        for i in range(0, len(two_haplotypes), 2):
            if two_haplotypes[i] == "" and two_haplotypes[i + 1] != "":
                two_haplotypes[i] = two_haplotypes[i + 1]
            elif two_haplotypes[i + 1] == "" and two_haplotypes[i] != "":
                two_haplotypes[i + 1] = two_haplotypes[i]
        return two_haplotypes

    def to_high_resolution(
        self, race: str, alleles: typing.List[float], allele_type_list: typing.List[str]
    ):
        """
        Convert supplied alleles into high resolution equivalents

        Parameters
        ----------
        race
            string representation of race
        alleles
            list of float SRTR allele values to convert to high resolution
        allele_type_list
            list of type of alleles supplied e.g. ['A','B','DR','DQ']

        Returns
        -------
        list
            high resolution alleles derived from haplotype frequency
            dictionaries.
        """
        haplotypes = []
        for i in range(len(allele_type_list)):
            for j in alleles[2 * i : 2 * i + 2]:
                if not math.isnan(j):
                    haplotypes.append(str(allele_type_list[i]) + str(int(j)))
                else:
                    haplotypes.append("")

        if any(
            haplotype
            and haplotype not in self.allele_conversions
            and haplotype not in self.allele_mappings
            for haplotype in haplotypes
        ):
            return [None] * len(allele_type_list) * 2

        two_haplotypes = [
            self.impute_haplotype_pairs(haplotypes)[::2],
            self.impute_haplotype_pairs(haplotypes)[1::2],
        ]

        formatted_haplotypes = [None] * (
            len(two_haplotypes[0]) + len(two_haplotypes[1])
        )
        formatted_haplotypes[::2] = two_haplotypes[0]
        formatted_haplotypes[1::2] = two_haplotypes[1]

        race_convert = self.translate_race(race)

        best_candidate = self._low_resolution_to_high_resolution(
            race_convert, formatted_haplotypes, allele_type_list
        )
        overall_list = []
        mid = (len(best_candidate) + 1) // 2
        for x, y in zip(best_candidate[:mid], best_candidate[mid:]):
            overall_list.append(x)
            overall_list.append(y)

        return overall_list

    # todo This function has a McCabe complexity of 12 and should be refactored
    def _low_resolution_to_high_resolution(
        self, race: str, alleles: typing.List, allele_type_list: typing.List[str]
    ):
        """
        Convert supplied alleles into high resolution equivalents

        Parameters
        ----------
        race
            string representation of race
        alleles
            list of float SRTR allele values to convert to high resolution
        allele_type_list
            list of type of alleles supplied e.g. ['A','B','DR','DQ']

        Returns
        -------
        list
            high resolution alleles derived from haplotype frequency
            dictionaries.
        """
        if race is None:
            return [None] * len(alleles)

        patient_allele_dict = {}
        for i in range(len(allele_type_list)):
            patient_allele_dict[allele_type_list[i]] = alleles[2 * i : 2 * i + 2]

        for alleleType in patient_allele_dict.keys():
            for allele in patient_allele_dict[alleleType]:
                if allele == "":
                    continue
                if (
                    allele not in self.allele_conversions
                    and allele not in self.allele_mappings
                ):
                    return [None] * len(alleles)

        combos = []
        master_list = []
        for alleleType in patient_allele_dict.keys():
            master_list.append(patient_allele_dict[alleleType])

        all_allele_combos = list(itertools.product(*master_list))
        mid = (len(all_allele_combos) + 1) // 2
        for first_haplotype, second_haplotype in zip(
            all_allele_combos[:mid], all_allele_combos[::-1]
        ):
            c1 = self._max_high_resolution_equivalent(
                self.impute_haplotype(first_haplotype, allele_type_list),
                [],
                self.haplotype_frequencies[race],
            )
            c2 = self._max_high_resolution_equivalent(
                self.impute_haplotype(second_haplotype, allele_type_list),
                [],
                self.haplotype_frequencies[race],
            )

            if c1 and c2:
                if c1[0] == c2[0]:
                    combos.append([c1[0] + c2[0], c1[1] * c2[1]])
                else:
                    combos.append([c1[0] + c2[0], 2 * c1[1] * c2[1]])
        if len(combos) == 0:
            return [None] * len(alleles)

        return max(combos, key=lambda arr: arr[1])[0]

    def _max_high_resolution_equivalent(
        self, one_haplotype, current_haplotype, frequency_dict: typing.Dict
    ):
        """
        Select highest frequency of occurrence high resolution allele from
        list of high resolution alleles corresponding to low resolution input.

        Parameters
        ----------
        one_haplotype

        current_haplotype

        frequency_dict
            dictionary of mapped allele values
        Returns
        -------

        """
        ret = []
        if type(frequency_dict) == float:
            return current_haplotype, frequency_dict
        if not one_haplotype:
            return ret
        for a in self._high_resolution_equivalents(
                one_haplotype[0], self.allele_mappings, self.allele_conversions
        ):
            if a in frequency_dict:
                val = self._max_high_resolution_equivalent(
                    one_haplotype[1:], current_haplotype + [a], frequency_dict[a]
                )
                if type(val) == tuple:
                    ret.append(val)
                if type(val) == list and val != []:
                    ret += val
        if ret:
            return max(ret, key=lambda arr: arr[1])
        else:
            return

    @staticmethod
    def _high_resolution_equivalents(
        low_resolution_haplotype: str,
        mapping_dict: typing.Dict[str, str],
        hla_dict: typing.Dict[str, str],
    ):
        """
        Get a list of high resolution haplotypes equivalents based on
        low resolution input.

        Parameters
        ----------
        low_resolution_haplotype
            string representation of low resolution haplotype
        mapping_dict
            dictionary of mapped allele values based on WHO assignments
        hla_dict
            dictionary of mapped allele values based on expert assignments
        Returns
        -------
        list
            high resolution alleles corresponding to low resolution input
        """
        high_list = []
        if low_resolution_haplotype in mapping_dict:
            mapped_list = []
            for mapped_hla in list(mapping_dict[low_resolution_haplotype]) + [
                low_resolution_haplotype
            ]:
                if mapped_hla in hla_dict:
                    mapped_list.append(mapped_hla)
        else:
            mapped_list = (
                [low_resolution_haplotype]
                if low_resolution_haplotype in hla_dict
                else []
            )
        for low_resolution_haplotype in mapped_list:
            high_list.extend(hla_dict[low_resolution_haplotype])
        return list(set(high_list))

    @staticmethod
    def impute_haplotype(
        haplotype: str, allele_type_list: typing.List[str]
    ) -> typing.List[str]:
        """
        Replace Null value haplotype with string imputation.

        Parameters
        ----------
        haplotype
            string representation of haplotype being assessed.
        allele_type_list
            list of haplotype representations

        Returns
        -------
        list
            Unmodified or imputed halpotype.
        """
        new_haplotype = []
        blank_addition = {"A": "A", "B": "B", "DR": "DRB1", "DQ": "DQB1"}

        for i in range(len(haplotype)):
            if not haplotype[i].strip():
                new_haplotype.append("blank" + blank_addition[allele_type_list[i]])
            else:
                new_haplotype.append(haplotype[i])
        return new_haplotype

    def hlaii_predictor(
        self, donor_alleles: typing.List[str], recipient_alleles: typing.List[str]
    ) -> typing.Dict[str, float]:
        """
        Calculates the total electrostatic, hydrophobicity, and amino acid
        mismatch scores between a set of Donor/Recipient alleles.

        Parameters
        ----------
        donor_alleles
            List of Donor Alleles
        recipient_alleles
            List of Recipient Alleles
        Returns
        -------
        dict
            dictionary of electrostatic, hydrophobicity, and amino acid mismatch
            scores.
        """
        alpha_r = []
        beta_r = []

        for recipient_allele in recipient_alleles:
            if "A" in recipient_allele:
                alpha_r.append(recipient_allele)
            else:
                beta_r.append(recipient_allele)

        alpha_ems = []
        alpha_hms = []
        alpha_ams = []
        beta_ems = []
        beta_hms = []
        beta_ams = []
        for donor_allele in donor_alleles:
            donor_allele = donor_allele.replace(":", "")
            if "A" in donor_allele:
                recipient_allele = self._hlaii_predictor(donor_allele, tuple(alpha_r))
                alpha_ems.append(recipient_allele["ems"])
                alpha_hms.append(recipient_allele["hms"])
                alpha_ams.append(recipient_allele["ams"])
            else:
                recipient_allele = self._hlaii_predictor(donor_allele, tuple(beta_r))
                beta_ems.append(recipient_allele["ems"])
                beta_hms.append(recipient_allele["hms"])
                beta_ams.append(recipient_allele["ams"])

        beta_ems = self.mean_or_zero(beta_ems)
        beta_hms = self.mean_or_zero(beta_hms)
        beta_ams = self.mean_or_zero(beta_ams)
        alpha_ems = self.mean_or_zero(alpha_ems)
        alpha_hms = self.mean_or_zero(alpha_hms)
        alpha_ams = self.mean_or_zero(alpha_ams)

        total_ems = alpha_ems + beta_ems
        total_hms = alpha_hms + beta_hms
        total_ams = alpha_ams + beta_ams

        return {
            "hms": total_hms,
            "ems": total_ems,
            "ams": total_ams,
            "alphaHms": alpha_hms,
            "alphaEms": alpha_ems,
            "alphaAms": alpha_ams,
            "betaHms": beta_hms,
            "betaEms": beta_ems,
            "betaAms": beta_ams,
        }

    @staticmethod
    def mean_or_zero(values: typing.List[float]) -> typing.Union[float, int]:
        """
        Get the mean score of supplied amino-acid, hydrophobicity, or
        electrostatic mismatch scores. If the no scores are supplied, then the
        function instead returns zero.

        Parameters
        ----------
        values
            List of mismatch scores

        Returns
        -------
        float
            mean value of mismatch scores or zero in cases of no scores.
        """
        return statistics.mean(values) if len(values) > 0 else 0

    @functools.lru_cache()
    def _hlaii_predictor(self, donor_allele: str, recipient_alleles: typing.List[str]):
        donor_amino_acids = self.amino_acid_details(donor_allele)

        recipient_amino_acids = []
        for r in recipient_alleles:
            r = r.replace(":", "")
            details = self.amino_acid_details(r)
            if details is None:
                continue
            recipient_amino_acids.append(details)

        ams = hms = ems = 0

        if donor_amino_acids is not None:
            for _, x in enumerate(zip(donor_amino_acids, zip(*recipient_amino_acids))):

                all_diff = True
                for i in range(len(x[1])):
                    if x[0] == x[1][i]:
                        all_diff = False
                        break

                if all_diff:
                    ams += 1
                    diffs = {"hms": [], "ems": []}

                    for j in range(len(x[1])):
                        diffs["hms"].append(abs(numpy.subtract(x[0], x[1][j])[0]))
                        diffs["ems"].append(abs(numpy.subtract(x[0], x[1][j])[1]))

                    hms += min(diffs["hms"])
                    ems += min(diffs["ems"])
        return {"hms": hms, "ems": ems, "ams": ams}

    def hlai_predictor(
        self, donor_alleles: typing.List[str], recipient_alleles: typing.List[str]
    ) -> typing.Dict[str, float]:
        """
        Calculates the total electrostatic, hydrophobicity, and amino acid
        mismatch scores between a set of Donor/Recipient alleles.

        Parameters
        ----------
        donor_alleles
            List of Donor Alleles
        recipient_alleles
            List of Recipient Alleles
        Returns
        -------
        dict
            dictionary of electrostatic, hydrophobicity, and amino acid mismatch
            scores.
        """
        ems = []
        ams = []
        hms = []
        for d in donor_alleles:
            r = self._hlai_predictor(d, tuple(recipient_alleles))

            ems.append(r["ems"])
            hms.append(r["hms"])
            ams.append(r["ams"])

        total_ems = statistics.mean(ems)
        total_hms = statistics.mean(hms)
        total_ams = statistics.mean(ams)

        return {"hms": total_hms, "ems": total_ems, "ams": total_ams}

    @functools.lru_cache()
    def _hlai_predictor(
        self, donor_allele: str, recipient_alleles: typing.List[str]
    ) -> typing.Dict[str, float]:
        """
        Calculates the total electrostatic, hydrophobicity, and amino acid
        mismatch scores between a Donor allele and a set of Recipient alleles.

        Parameters
        ----------
        donor_allele
            List of Donor Alleles
        recipient_alleles
            List of Recipient Alleles
        Returns
        -------
        dict
            dictionary of electrostatic, hydrophobicity, and amino acid mismatch
            scores.
        """
        donor_amino_acids = self.amino_acid_details(
            donor_allele, dict_type=SequenceType.ALIGNED
        )

        recipient_amino_acids = []
        for recipient_allele in recipient_alleles:
            details = self.amino_acid_details(
                recipient_allele, dict_type=SequenceType.ALIGNED
            )
            if details is None:
                continue
            recipient_amino_acids.append(details)

        hms = ems = ams = 0

        if donor_amino_acids is not None:

            for x in zip(donor_amino_acids, zip(*recipient_amino_acids)):
                all_diff = True

                for i in range(len(x[1])):
                    if x[0] == x[1][i]:
                        all_diff = False
                        break

                # If they are all different
                if all_diff:

                    ams += 1

                    diffs = {"hms": [], "ems": []}

                    for j in range(0, len(x[1])):
                        diffs["hms"].append(
                            round(abs(numpy.subtract(x[0], x[1][j])[0]), 2)
                        )
                        diffs["ems"].append(
                            round(abs(numpy.subtract(x[0], x[1][j])[1]), 2)
                        )
                    hms += min(diffs["hms"])
                    ems += min(diffs["ems"])

        return {"hms": hms, "ems": ems, "ams": ams}
