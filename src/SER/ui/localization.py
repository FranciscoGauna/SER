from os import path
import yaml

from lantz.core.log import get_logger
from pimpmyclass.mixins import LogMixin


class Localizator(LogMixin):
    locale_dict: dict[str, str]

    def __init__(self, locale="en", file_path=None):
        self.logger = get_logger("SER.Core.MainWindow")
        self.set(locale, file_path)

    def set(self, locale="en", file_path=None):
        if file_path is None:
            file_path = path.join(path.dirname(path.realpath(__file__)), "locale", f"{locale}.yml")
        with open(file_path, "r+") as file:
            self.locale_dict = yaml.safe_load(file)

    def get(self, key: str) -> str:
        if key in self.locale_dict:
            return self.locale_dict[key]
        else:
            self.log_error(msg=f"Key missing: {key}")
            return key


localizator = Localizator()
