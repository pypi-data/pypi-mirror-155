import numpy as np
import pandas
import pandas as pd
from collections import namedtuple


class ExcelFile:
    def __init__(self, excel_fp: str):
        self.df: pd.DataFrame = pandas.read_excel(excel_fp)
        self.all_series: list[DataSeries] = []

    def get_series(self):
        for col in self.df.columns:
            series_in_row: list[DataSeries] = []
            for i in self.df[col]:
                if type(i) == str:
                    s = DataSeries()
                    series_in_row.append(s)
                    s.name = i
                    s.data = []
                elif not pd.isna(i) and type(i) != str:
                    if len(series_in_row):
                        series_in_row[-1].data.append(i)
                    else:
                        continue
            for series in series_in_row:
                if len(series.data):
                    self.all_series.append(series)
        return self.all_series


class DataSeries:
    __slots__ = ('name', 'data')
    name: str
    data: list

    def __init__(self):
        pass

    def __str__(self):
        return f"{self.name} {self.data}"
