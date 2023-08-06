import json
import os

import requests

from flowhigh.extraction.converters import ApiConverter
from flowhigh.util.sdk_visitor import SDKVisitor


def parse_sql(source: str):
    url = "https://sql.sonra.io/api/process"
    headers = {"User-Agent": "python/flowhigh-0.0.1", "Content-type": "application/json", "Authentication": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im9XWlBLbUk2clFPQ2ZQMUdERFVUSiJ9.eyJpc3MiOiJodHRwczovL2F1dGguc29ucmEuaW8vIiwic3ViIjoiYXV0aDB8NjI4ODQxNGI4YjkzYTQwMDY4ZWYwZDk2IiwiYXVkIjpbImh0dHBzOi8vc3FsLnNvbnJhLmlvL2FwaS8iLCJodHRwczovL3NvbnJhLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NTUzMDQzMTMsImV4cCI6MTY1NTMxMTUxMywiYXpwIjoibXNmZXBrQU01amlLY0pqSkZZM3pkbk5jdERkcmhuYmQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIn0.WM6K9PgdBOmWaf3AZIygQIR6LEu-NA2CGwpJemA5_XIkXuZxx6nDpsXeLegrjplNN7t8kkHKSHCbL_qBRhDSAzLnSR2ERtXWfIjFw3T-yrPU-WTZJC4By805QgBHQTBJ68eUVDrUi73Y2W8LzOmA47mtGq9KCO0UpsBaQBxyCHKHVsQH-fioT4HQtTZns4UdetnJEYg0fHJwn_Fskuwpfhb5oP4o84xCi44vqHBnxk1nNu7NMZ8vN39kX0G6f6L3dbL5vuXUUT_5cZtpCeczbfHNg21mf7ottcw5WskTjs-vwhNV_hQfZt8v589q_KIOQgzoMeb8qHhhBxwuwJ-zVw"}
    data = {"sql": source, "json": True, "xml": True}
    response = requests.post(url, json=data, headers=headers)
    converter = ApiConverter()
    if response.status_code == 200:
        json_data = json.loads(response.content)
        visitor = SDKVisitor()
        parseql = converter.convert_parseql(json_data, visitor)
        parseql.accept(visitor)
        parseql.accept(visitor.lineage_visitor)
        for statement in parseql.statement:
            statement.accept(statement.visitor)
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
    headers = {"User-Agent": "python/flowhigh-0.0.1", "Content-type": "application/json"}
    data = {"sql": source, "json": True, "xml": True}
    response = requests.post(url, json=data, headers=headers)
    converter = ApiConverter()
    if response.status_code == 200:
        json_data = json.loads(response.content)
        visitor = SDKVisitor()
        parseql = converter.convert_parseql(json_data, visitor)
        parseql.accept(visitor)
        parseql.accept(visitor.lineage_visitor)
        for statement in parseql.statement:
            statement.accept(statement.visitor)
        return parseql
    else:
        raise Exception("Invalid Response")
