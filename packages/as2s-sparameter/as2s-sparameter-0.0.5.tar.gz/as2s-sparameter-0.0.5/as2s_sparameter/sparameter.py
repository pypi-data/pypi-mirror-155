# -*- coding: utf-8 -*-


import re

from pandas import DataFrame
from skrf import Network

from .constants import CONVERT_TYPES, NTWK_ATTR_FORMS
from .interface import Interface


class Sparameter:
    def __init__(self) -> None:
        pass

    @property
    def ntwk(self) -> Network:
        return self.__ntwk

    @property
    def port(self) -> int:
        return self.__ntwk.number_of_ports

    def read(self, input_path: str) -> str:
        self.__ntwk = Interface.touchstone_2_network(input_path=input_path)
        return self.__ntwk.__str__()

    def write(self, file_name: str = '', dir: str = '', form: str = '') -> str:
        return Interface.network_2_touchstone(
            ntwk=self.__ntwk, output_dir=dir, output_name=file_name, form=form
        )

    @staticmethod
    def convert(
        convert_from: str | DataFrame | Network,
        convert_to: str,
        output_dir: str = '',
        output_name: str = '',
        attrs: list[str] = [],
        ports: list[tuple[int, int]] = [(0, 0)],
        form: str = '',
    ) -> str | DataFrame | Network:
        """
        Convert touchstone file to a pandas DataFrame or a touchstone file or csv.

        Parameters
        ----------
        convert_from : file path / DataFrame / Network
            file path is full path of a touchstone or csv file.
            DataFrame is pandas DataFrame Object.
            Network is a n-port electrical network Object.
        convert_to : the kind of output data
            parameter = ['csv', 'df', 'nk', 'ts']
        output_name : output file name
            blank = [convert_from].name
        output_dir : save directory path
            blank = current directory
        attrs : list of Network attributes, optional
            parameter = ['s_re', 's_im', 's_mag', 's_db', 's_deg']
            blank = ['s_db','s_deg']
        ports : list of tuples
            list of port pairs to write.
            blank = [(1,1)] = S11
        form : s-parameter form
            blank = ['db']

        Returns
        -------

        """
        from_type = ''
        obj_name = type(convert_from).__name__
        match obj_name:
            case 'str':
                # find pattern of extension
                pattern_ts = re.compile(r'\.s[0-9]+p')
                pattern_csv = re.compile(r'\.csv')
                # check convert_from type
                # TouchStone, csv
                path = str(convert_from)
                if len(pattern_ts.findall(path)) > 0:
                    from_type = 'ts'
                elif len(pattern_csv.findall(path)) > 0:
                    from_type = 'csv'
                else:
                    raise ValueError(f'convert_from: path: [{path}] is not [ts | csv].')
            case 'DataFrame':
                from_type = 'df'
            case 'Network':
                from_type = 'nk'
            case _:
                raise ValueError(
                    'convert_from is not [csv | DataFrame | Network | TouchStone].'
                )

        # check convert_to
        if convert_to not in CONVERT_TYPES:
            raise ValueError(f'convert_type parameter should be either:{CONVERT_TYPES}')

        # check attrs
        for attr in attrs:
            if attr not in NTWK_ATTR_FORMS:
                raise ValueError(
                    f'attrs[ {attr} ] parameter should be either:{NTWK_ATTR_FORMS}'
                )

        rtn = None

        # match interface
        match from_type:
            case 'csv':
                rtn = 'from_csv'
            case 'df':
                match convert_to:
                    case 'csv':
                        rtn = 'from_df_to_csv'
                    case 'nk':
                        rtn = 'from_df_to_nk'
                    case 'ts':
                        rtn = 'from_df_to_ts'
                    case _:
                        rtn = 'not match'
            case 'nk':
                match convert_to:
                    case 'csv':
                        rtn = Interface.network_2_csv(ntwk=convert_from)
                    case 'df':
                        rtn = Interface.network_2_dataframe(ntwk=convert_from)
                    case 'ts':
                        rtn = Interface.network_2_touchstone(
                            ntwk=convert_from, output_dir=output_dir, form=form
                        )
                    case _:
                        rtn = 'not match'
            case 'ts':
                match convert_to:
                    case 'csv':
                        rtn = Interface.touchstone_2_csv(
                            input_path=str(convert_from), output_dir=output_dir
                        )
                    case 'df':
                        rtn = Interface.touchstone_2_dataframe(
                            input_path=str(convert_from)
                        )
                    case 'nk':
                        rtn = Interface.touchstone_2_network(
                            input_path=str(convert_from)
                        )
                    case 'ts':
                        rtn = Interface.touchstone_2_touchstone(
                            input_path=str(convert_from), form=form
                        )
                    case _:
                        rtn = 'not match'
        return rtn
