"""
string cutter handler
"""
from dfactory.core import Handler


class StringCutter(Handler):
    """cut string field with specify size"""

    def __init__(self):
        super().__init__()
        self.keys = {}

    def load_data(self, cfg: dict):
        self.keys = cfg['keys']

    @staticmethod
    def cut(src, start, end, append: str = None):
        """
        cut string
        :param src: string to cut
        :param start: start pos to cut
        :param end: end pos (end not include in sub string)
        :param append: append to result
        :return: is src is None or empty return original else return src[start:end]
        """
        if src is None or src == "":
            return src
        dst = src[start:end]
        return dst if append is None or len(src) <= end else dst + append

    def handle(self, item: dict) -> dict:
        for key, data in self.keys.items():
            item[key] = self.cut(item[key], data.get('start', 0), data['end'], data.get("append"))
        return item
