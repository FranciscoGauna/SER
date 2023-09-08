from typing import List, Dict, Tuple, Any

from lantz.core.log import get_logger
from pimpmyclass.mixins import LogMixin


class DataRepository(LogMixin):

    def __init__(self):
        self.logger = get_logger("SER.Core.Dispatcher")
        self.data: List[Dict[str, Dict[str, Any]]] = []

    def next(self):
        self.data.append({})

    def add_datum(self, name: str, datum: Any):
        self.data[-1][name] = datum


    def to_file(self):
        header: List[Tuple[str, str]] = []
        for k, v in self.data[0].items():
            for sub_k in v:
                header.append((k, sub_k))

        vals = []
        for line in self.data:
            line_val = {}
            for k, v in header:
                if k in line:
                    line_val[f"{k}_{v}"] = line[k][v]
                else:
                    line_val[f"{k}_{v}"] = vals[-1][f"{k}_{v}"]
            vals.append(line_val)

        with open("output.txt", "w+", encoding="utf8") as file:
            file.write(repr(vals))

