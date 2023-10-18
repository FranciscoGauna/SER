from typing import List, Dict, Tuple, Any

from lantz.core.log import get_logger
from pimpmyclass.mixins import LogMixin
from scipy.io import savemat
import pandas as pd


class DataRepository(LogMixin):

    def __init__(self):
        self.logger = get_logger("SER.Core.Dispatcher")
        self.data: List[Dict[str, Dict[str, Any]]] = []

    def next(self):
        self.data.append({})

    def add_datum(self, name: str, datum: Dict[str, Any]):
        self.data[-1][name] = datum

    def get_datum_index(self, index):
        return self.data[index]

    def to_dataframe(self) -> pd.DataFrame:
        header: set[Tuple[str, str]] = set()
        for item in self.data:
            for k, v in item.items():
                for sub_k in v:
                    header.add((k, sub_k))

        vals = []
        for line in self.data:
            line_val = {}
            for k, v in header:
                if k in line:
                    line_val[f"{k}_{v}"] = line[k][v]
                elif len(vals) > 0 and f"{k}_{v}" in vals[-1]:
                    line_val[f"{k}_{v}"] = vals[-1][f"{k}_{v}"]
                else:
                    line_val[f"{k}_{v}"] = float("NaN")
            vals.append(line_val)

        df = pd.DataFrame(vals)
        return df[sorted(df.columns)]

    def to_csv(self, filename: str):
        self.to_dataframe().to_csv(filename)

    def to_matlab(self, filename: str):
        df = self.to_dataframe()
        mat_dict = {}
        for column in df.columns:
            column: str
            column = column.replace(" ", "_")
            if column in mat_dict:
                self.log_error("Matlab column name collision!")
            mat_dict[column] = df[column].to_numpy(copy=True)
        savemat(filename, mat_dict)
