#!/usr/bin/env python3
import os
import re

import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class SAPAPI:
    def __init__(self, username='admin', password='nimda', hacurl='https://localhost:9002'):
        self.username = username
        self.password = password
        self.hacurl = hacurl

        self.sessionid = None

        # create cache file
        self.cache_dir = os.path.join(os.path.expanduser('~'), '.sap-cli')
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        # try loading session id from cache
        # self.sessionid = self.__load_session_id_from_cache()

    @staticmethod
    def __get_csrf_token(hacurl, sessionid) -> str:
        r = requests.get(hacurl, verify=False, cookies={'JSESSIONID': sessionid})
        if r.ok:
            csrfs = re.findall(r'<meta name="_csrf" content="(.*)" />', r.text)
            return csrfs[0]

        return None

    @staticmethod
    def __get_session_id(hacurl) -> str:
        r = requests.get(hacurl, verify=False, allow_redirects=False)
        if r.ok:
            return r.cookies.get('JSESSIONID')

        return None

    def get(self, path, params) -> requests.Response:
        self.__validate_session_id()

        r = requests.get(self.hacurl + path, verify=False, params=params, cookies={'JSESSIONID': self.sessionid},
                         allow_redirects=False, timeout=5)
        if not r.ok:
            raise ConnectionError(f"Get request to {path} failed with status code {r.status_code}")

        return r

    def post(self, path, data) -> requests.Response:
        self.__validate_session_id()

        csrf = self.__get_csrf_token(self.hacurl, self.sessionid)

        r = requests.post(self.hacurl + path, verify=False, data=data, headers={'X-CSRF-TOKEN': csrf},
                          cookies={'JSESSIONID': self.sessionid}, allow_redirects=False, timeout=5)
        if r.ok and r.cookies.get('JSESSIONID'):
            self.sessionid = r.cookies.get('JSESSIONID')

        if not r.ok:
            raise ConnectionError(f"Post request to {path} failed with status code {r.status_code}")

        return r

    def login(self):
        self.sessionid = self.__get_session_id(self.hacurl)
        self.__save_session_id_to_chache(self.sessionid)
        self.__validate_session_id()

        csrf = self.__get_csrf_token(self.hacurl + '/login', self.sessionid)
        data = {
            'j_username': self.username,
            'j_password': self.password,
            '_csrf': csrf
        }

        r = self.post('/j_spring_security_check', data)
        if r.status_code == 302:
            location = r.headers.get('Location')
            if location and re.match(r'.*login_error.*', location):
                raise ConnectionError("Invalid username/password")

    def __load_session_id_from_cache(self):
        cache_file = os.path.join(self.cache_dir, 'session')
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as c:
                data = c.read().strip()
                return data

        return None

    def __save_session_id_to_chache(self, sessionid):
        cache_file = os.path.join(self.cache_dir, 'session')
        with open(cache_file, 'w+') as c:
            c.write(sessionid)

    def __validate_session_id(self):
        if not self.sessionid or not len(self.sessionid):
            raise ConnectionError("Missing session id")
