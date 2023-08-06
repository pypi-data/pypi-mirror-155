#!/usr/bin/env python3

import json
import os.path

from src import api


class Script:
    def __init__(self, content_or_file: str, script_type='groovy', commit=False, is_file=False):
        self.content = content_or_file
        self.isFile = is_file
        self.filepath = None

        if is_file and not os.path.exists(content_or_file):
            raise FileNotFoundError(f"File {content_or_file} not found !")
        else:
            self.filepath = content_or_file
            with open(content_or_file, 'r') as f:
                self.content = f.read()

        self.script_type = script_type
        self.commit = commit


class ScriptResult:
    def __init__(self, content: dict):
        self.content = content

        self.__validate_attribute('stacktraceText')
        self.__validate_attribute('executionResult')
        self.__validate_attribute('outputText')

        self.result = self.content['executionResult']
        self.stacktrace = self.content['stacktraceText']
        self.output = self.content['outputText']

    def __validate_attribute(self, attribute: str):
        if attribute not in self.content.keys():
            raise TypeError(f"Attribute {attribute} is missing !")

    def is_ok(self):
        return not self.stacktrace

    def get_errors(self):
        return self.stacktrace


class Scripting:
    def __init__(self, client_api: api.SAPAPI):
        self.api = client_api

    def execute(self, script: Script) -> ScriptResult:
        data = {
            'script': script.content,
            'scriptType': script.script_type,
            'commit': 'true' if script.commit else 'false'
        }

        api_response = self.api.post('/console/scripting/execute', data)
        return ScriptResult(json.loads(api_response.content))
