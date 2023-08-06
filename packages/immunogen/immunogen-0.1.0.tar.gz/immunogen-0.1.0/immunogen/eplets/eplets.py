import configparser
import inspect
import pathlib
import pickle
import typing
from collections import defaultdict

import pandas

from immunogen.utils.MetaLogger import MetaLogger

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources


class Eplets(metaclass=MetaLogger):
    """
    Class which maintains internal dictionaries of Allele to Eplet mappings.
    Includes precomputed mappings while permitting skilled users to supply different mappings.
    """

    def __init__(self) -> None:
        self._config = None
        self._eplets = None
        self._eplet_types = None

    @property
    def config(self):
        """
        Property reads configuration file for file paths to Allele/Eplet raw data.
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

        :param value:
        :return:
        """
        self.config = value

    @property
    def eplets(self) -> typing.Dict[str, str]:
        """
        Property contains Allele to Eplet mappings.

        Returns
        -------
        dictionary
            A dictionary of allele values with mapped eplets.
        """
        if self._eplets is None:
            try:
                self.__logger.info(
                    f"Pickle found, reading {inspect.stack()[0][3]} from source."
                )
                file = pkg_resources.open_binary("immunogen.data.pickles", "eplets.p")
                self._eplets = pickle.load(file)
            except (ValueError, FileNotFoundError):
                self.__logger.info(
                    f"No pickle found, building {inspect.stack()[0][3]} from source."
                )
                self.eplets = None
        return self._eplets

    @eplets.setter
    def eplets(self, value: typing.Union[str, pathlib.Path]) -> None:
        """

        :param value:
        :return:
        """
        if value is None:
            value = pathlib.Path(__file__).parent.parent / self.config.get(
                "eplets", "eplets"
            )
        self._make_eplets(ref_data=value)
        pickle.Pickler(
            open((pathlib.Path("../../../immunogen/immunogen/data/pickles") / "eplets.p"), "wb"),
            protocol=pickle.HIGHEST_PROTOCOL,
        ).dump(self.eplets)

    def _make_eplets(self, ref_data: typing.Union[str, pathlib.Path]) -> None:
        """

        :param ref_data:
        :return:
        """
        eplet_dataframe = pandas.read_csv(ref_data)

        eplet_dict = defaultdict(list)

        for i, r in eplet_dataframe.iterrows():
            eplet_dict[r["Allele"]].append(r["Eplet"])

        self._eplets = eplet_dict

    @property
    def eplet_types(self) -> typing.Dict[str, str]:
        """
        Property contains eplet to eplet type mappings.

        Returns
        -------
        dictionary
            A dictionary of eplet values with mapped eplet types.
        """
        if self._eplet_types is None:
            try:
                file = pkg_resources.open_binary(
                    "immunogen.data.pickles", "eplet_types.p"
                )
                self._eplet_types = pickle.load(file)
            except (ValueError, FileNotFoundError):
                self.__logger.info(
                    f"No pickle found, building {inspect.stack()[0][3]} from source."
                )
                self.eplet_types = None
        return self._eplet_types

    @eplet_types.setter
    def eplet_types(self, value: typing.Union[str, pathlib.Path]) -> None:
        """

        :param value:
        :return:
        """
        if value is None:
            value = pathlib.Path(__file__).parent.parent / self.config.get(
                "eplets", "eplet_types"
            )
        self._make_eplet_types(ref_data=value)
        pickle.Pickler(
            open((pathlib.Path("../../../immunogen/immunogen/data/pickles") / "eplet_types.p"), "wb"),
            protocol=pickle.HIGHEST_PROTOCOL,
        ).dump(self.eplet_types)

    def _make_eplet_types(self, ref_data: typing.Union[str, pathlib.Path]) -> None:
        """

        :param ref_data:
        :return:
        """
        eplet_type_dataframe = pandas.read_csv(ref_data)

        eplet_type_dict = defaultdict(set)

        for i, r in eplet_type_dataframe.iterrows():
            eplet_type_dict[r["Eplet"]].add(r["Eplet_Type"])

        self._eplet_types = eplet_type_dict

    def compare(self, left: typing.List[str], right: typing.List[str]):
        """
        Returns a tuple of the list of eplets associated with the left alleles and the list of eplets associated with the right alleles.

        Parameters
        ----------
        left
            list of alleles
        right
            list of alleles
        Returns
        -------
        tuple
            A tuple of eplets associated with the unique alleles of both the left list of alleles and right list of alleles.
        """
        self.__logger.info(f"{inspect.stack()[0][3]}")
        duplicates = list(set(left).intersection(right))
        left_unique = list(filter(lambda x: x not in duplicates, left))
        right_unique = list(filter(lambda x: x not in duplicates, right))

        left_eplets = set()

        for item in left_unique:
            eplets = self.eplets.get(item, [])
            for eplet in eplets:
                left_eplets.add(eplet)

        right_eplets = set()

        for item in right_unique:
            eplets = self.eplets.get(item, [])
            for eplet in eplets:
                right_eplets.add(eplet)

        return left_eplets, right_eplets

    def get_eplet_type(self, left: typing.List[str], right: typing.List[str]):
        """
        Returns the overall mismatch scores between the left and right sets of eplets.
        The mismatch scores are divided into Oth and Abv type mismatches.

        Parameters
        ----------
        left
            list of eplets
        right
            list of eplets

        Returns
        -------
            tuple
                Abv mismatch total, Oth mismatch total, list of Abv mismatched eplets, list of Oth mismatched eplets
        """
        AbvMismatch = 0
        OthMismatch = 0
        Abv_Desc = []
        Oth_Desc = []
        for eplet in left:
            eplet_type = self.eplet_types[eplet]
            if eplet not in right:
                if "AbV" in eplet_type:
                    AbvMismatch += 1
                    Abv_Desc.append(eplet)
                else:
                    OthMismatch += 1
                    Oth_Desc.append(eplet)
        return AbvMismatch, OthMismatch, Abv_Desc, Oth_Desc
