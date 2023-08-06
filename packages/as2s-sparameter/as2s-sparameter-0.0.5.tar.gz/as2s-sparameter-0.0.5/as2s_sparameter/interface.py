# -*- coding: utf-8 -*-

import os

import skrf as rf
from pandas import DataFrame
from skrf import Network


class Interface:
    def __init__(self) -> None:
        pass

    # def csv_2_network(path: str) -> Network:

    # def csv_2_touchstone(path: str) -> str:

    # def dataframe_2_network(df: DataFrame) -> Network:

    # def dataframe_2_touchstone(df: DataFrame) -> str:

    @staticmethod
    def network_2_csv(
        ntwk: Network, output_dir: str = '', output_name: str = '', form: str = ''
    ) -> str:
        if not output_dir:
            output_dir = os.getcwd()
        if not output_name:
            output_name = f'{ntwk.name}.csv'
        path = os.path.join(output_dir, output_name)
        if not form:
            form = 'db'
        rf.network_2_spreadsheet(ntwk, file_name=path, file_type='csv', form=form)
        return path

    @staticmethod
    def network_2_dataframe(
        ntwk: Network, attrs: list[str] = [], ports: list[tuple[int, int]] = [(0, 0)]
    ) -> DataFrame:
        """
        Convert network to a pandas DataFrame.

        Parameters
        ----------
        ntwk : :class:`~skrf.network.Network` object
            the network to write
        attrs : list Network attributes
            like ['s_db','s_deg']
        ports : list of tuples
            list of port pairs to write.
            (like [(1,1)] = S11)

        Returns
        -------
        df : pandas DataFrame Object
        """
        if not attrs:
            attrs = ['s_db', 's_deg']

        if ports == [(0, 0)]:
            ports = ntwk.port_tuples
        else:
            ports = [(m - 1, n - 1) for m, n in ports]

        df = rf.network_2_dataframe(ntwk=ntwk, attrs=attrs, ports=ports)
        # set index name : Freq[(freq_unit)]
        df.index.name = f'Freq[{ntwk.frequency.unit}]'
        return df

    @staticmethod
    def network_2_touchstone(
        ntwk: Network, output_dir: str = '', output_name: str = '', form: str = ''
    ) -> str:
        if not output_dir:
            output_dir = os.getcwd()
        if not output_name:
            output_name = ntwk.name
        if not form:
            form = 'db'
        ntwk.write_touchstone(dir=output_dir, filename=output_name, form=form)
        return os.path.join(output_dir, f'{output_name}.s{ntwk.number_of_ports}p')

    @classmethod
    def touchstone_2_csv(
        cls,
        input_path: str,
        output_dir: str = '',
        output_name: str = '',
        form: str = '',
    ) -> str:
        ntwk = cls.touchstone_2_network(input_path=input_path)
        return cls.network_2_csv(
            ntwk=ntwk, output_dir=output_dir, output_name=output_name, form=form
        )

    @classmethod
    def touchstone_2_dataframe(
        cls,
        input_path: str,
        attrs: list[str] = [],
        ports: list[tuple[int, int]] = [(0, 0)],
    ) -> DataFrame:
        ntwk = cls.touchstone_2_network(input_path=input_path)
        return cls.network_2_dataframe(ntwk=ntwk, attrs=attrs, ports=ports)

    @staticmethod
    def touchstone_2_network(input_path: str) -> Network:
        return rf.Network(file=input_path)

    @classmethod
    def touchstone_2_touchstone(
        cls,
        input_path: str,
        output_dir: str = '',
        output_name: str = '',
        form: str = '',
    ) -> str:
        ntwk = cls.touchstone_2_network(input_path)
        return cls.network_2_touchstone(
            ntwk=ntwk, output_dir=output_dir, output_name=output_name, form=form
        )
