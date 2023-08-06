"""
JsonWriter
"""
import json

from dfactory.core import CondHandler
from dfactory.handlers.matches import Match
from dfactory.utils.jsonutils import JsonEncoder


class JsonWriter(CondHandler):
    """
    JsonWriter
    write item to json file
    one item per line
    if save_key is specified the save item[save_key] instead of whole object
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.filename = kwargs.get("path", "")
        self.file = None
        self.headers = kwargs.get('headers', [])
        self.save_key = None
        self.match = None

    def is_created(self) -> bool:
        """check if writer ready to write"""
        return self.file is not None

    def __enter__(self):
        """prepare data"""
        self.file = open(self.filename, "w", encoding="utf-8")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        close file if necessary
        """
        if self.file is not None:
            self.file.close()
        self.file = None

    def check(self, item: dict) -> bool:
        return self.match is None or self.match.match(item)

    @staticmethod
    def from_dict(cfg: dict):
        """
        create a CsvWriter from data
        :param cfg: cfg data
        :return: new CsvWriter object
        """
        return JsonWriter(**cfg)

    def load_data(self, cfg: dict):
        """
        load data
        :param cfg: config data
        :return: None
        """
        self.file = None
        self.filename = cfg.get("path")
        self.headers = cfg.get("headers", [])
        self.save_key = cfg.get('save_key')
        match = cfg.get('match')
        self.match = None if match is None else Match.from_dict(match)

    def operate(self, item: dict):
        """
        save item to csv file
        :param item: item to handle
        :return: the same item
        """
        try:
            data = item if self.save_key is None else item[self.save_key]
            obj = data if len(self.headers) == 0 else {k: data[k] for k in self.headers}
            self.file.write(json.dumps(obj, ensure_ascii=False, cls=JsonEncoder))
            self.file.write("\n")
        except IOError:
            pass
        return item
