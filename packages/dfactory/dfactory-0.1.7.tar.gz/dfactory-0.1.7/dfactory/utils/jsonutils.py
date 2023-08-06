# -*- coding: utf-8 -*-

"""
json utils
"""
import json
from json import JSONEncoder


class JsonEncoder(JSONEncoder):
    """json encoder"""

    def default(self, o):
        if o.__class__.__name__ in ['int64', "int32"]:
            return int(o)
        if o.__class__.__name__ in ['float64', "float32"]:
            return float(o)
        return JSONEncoder.default(self, o)


def read_json(filename, line_by_line=False):
    """
    read json file
    :param filename: json file
    :param line_by_line: file with format of json one item per line
    :return: list or dict
    """
    with open(filename, encoding="utf-8") as fin:
        if not line_by_line:
            return json.loads(fin.read())
        array = []
        for line in fin:
            array.append(json.loads(line))
        return array


def read_json_by_line(filename):
    """
    read json file with format one json item per line
    :param filename: json file
    :return: generator of json item
    """
    with open(filename, encoding="utf-8") as fin:
        for line in fin:
            yield json.loads(line.strip())
