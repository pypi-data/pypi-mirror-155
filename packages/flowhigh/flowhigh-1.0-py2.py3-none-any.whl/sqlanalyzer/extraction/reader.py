import json
import os

import requests

from sqlanalyzer.extraction.converters import ApiConverter
from sqlanalyzer.util.sdk_visitor import SDKVisitor


def read_sql(source: str):
    url = "https://sql.sonra.io/api/process"
    headers = {"User-Agent": "python/sqlanalyzer-0.0.1", "Content-type": "application/json"}
    data = {"sql": source, "json": True, "xml": True}
    response = requests.post(url, json=data, headers=headers)
    converter = ApiConverter()
    if response.status_code == 200:
        json_data = json.loads(response.content)
        visitor = SDKVisitor()
        parseql = converter.convert_parseql(json_data, visitor)
        parseql.accept(visitor)
        parseql.accept(visitor.lineage_visitor)
        return parseql
    else:
        raise Exception("Invalid Response")


def read_file(file: str):
    if os.path.exists(file):
        with open(file) as file:
            source = file.read()
            file.close()
    else:
        print("Invalid File")
    url = "https://sql.sonra.io/api/process"
    headers = {"User-Agent": "python/sqlanalyzer-0.0.1", "Content-type": "application/json"}
    data = {"sql": source, "json": True, "xml": True}
    response = requests.post(url, json=data, headers=headers)
    converter = ApiConverter()
    if response.status_code == 200:
        json_data = json.loads(response.content)
        visitor = SDKVisitor()
        parseql = converter.convert_parseql(json_data, visitor)
        parseql.accept(visitor)
        parseql.accept(visitor.lineage_visitor)
        return parseql
    else:
        raise Exception("Invalid Response")
