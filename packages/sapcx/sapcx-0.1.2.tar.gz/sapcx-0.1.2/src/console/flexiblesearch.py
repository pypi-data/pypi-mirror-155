#!/usr/bin/env python3
import json

from src import api


class QueryResult:
    def __init__(self, content: dict):
        self.content = content

        self.__validate_attribute('headers')
        self.__validate_attribute('resultList')
        self.__validate_attribute('query')

    def __validate_attribute(self, attribute: str):
        if attribute not in self.content.keys():
            raise TypeError(f"Invalid content, attribute {attribute} not found")

    def is_ok(self):
        return not self.content['exceptionStackTrace']

    def get_errors(self):
        return self.content['exceptionStackTrace']

    def get_result(self):
        res = ', '.join(list(self.content['headers']))
        res += '\n'
        for line in self.content['resultList']:
            res += ', '.join(line)

        return res


class FlexibleSearch:
    def __init__(self, api_client: api.SAPAPI):
        self.api = api_client

    def execute(self, query: str, max_count=200, user='admin', locale='en', data_source='master',
                commit=False) -> QueryResult:
        request_body = {
            'flexibleSearchQuery': query,
            'scriptType': 'flexibleSearch',
            'sqlQuery': '',
            'maxCount': max_count,
            'user': user,
            'locale': locale,
            'dataSource': data_source,
            'commit': 'true' if commit else 'false'
        }

        response = self.api.post('/console/flexsearch/execute', request_body)
        return QueryResult(json.loads(response.content.decode(response.encoding)))
