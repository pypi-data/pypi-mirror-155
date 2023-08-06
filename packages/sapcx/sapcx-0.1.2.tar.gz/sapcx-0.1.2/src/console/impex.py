#!/usr/bin/env python3
import os

from bs4 import BeautifulSoup

from src import api


class Impex:
    def __init__(self, content_or_file: str, is_file=False):
        self.content = content_or_file
        self.filepath = None

        if is_file and not os.path.exists(content_or_file):
            raise FileNotFoundError(f"File {content_or_file} not found !")
        else:
            self.filepath = content_or_file
            with open(content_or_file, 'r') as f:
                self.content = f.read()


class ImpexResult:
    def __init__(self, content: str):
        self.content = content
        self.soup = BeautifulSoup(self.content, features='lxml')

    def is_ok(self):
        res = self.soup.find('span', attrs={'id': 'impexResult'})
        if res and res.attrs['data-level'] == 'error':
            return False
        return True

    def get_errors(self):
        res = self.soup.find('pre')
        return res.text.strip()


class ImpexEngine:
    def __init__(self, client_api: api.SAPAPI):
        self.api = client_api

    def impex_import(self, impex: Impex) -> ImpexResult:
        data = {
            'scriptContent': impex.content,
            'validationEnum': 'IMPORT_STRICT',
            'maxThreads': 8,
            'encoding': "UTF-8",
            '_legacyMode': 'on',
            '_enableCodeExecution': 'on',
            '_distributedMode': 'on',
            '_sldEnabled': 'on'
        }

        response = self.api.post('/console/impex/import', data)
        return ImpexResult(response.content.decode(response.encoding))
