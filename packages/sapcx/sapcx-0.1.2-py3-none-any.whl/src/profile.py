#!/usr/bin/env python3
import json
import os.path


class Profile:
    config_path = os.path.join(os.path.expanduser('~'), '.sap-cli')
    profile_path = os.path.join(config_path, 'profiles')

    def __init__(self, identifier, username='admin', password='nimda', server='127.0.0.1', port=9002, ssl=True,
                 webroot='/'):
        self.identifier: str = identifier
        self.username: str = username
        self.password: str = password
        self.server: str = server
        self.port: int = int(port)
        self.ssl: bool = ssl
        self.webroot: str = webroot

        if not os.path.exists(self.config_path):
            os.mkdir(self.config_path)

        if not os.path.exists(self.profile_path):
            with open(self.profile_path, 'w') as f:
                pass

    def save(self):
        profiles = dict()
        with open(self.profile_path, 'r+') as f:
            content = f.read()
            if content and len(content):
                profiles.update(json.loads(content))

        profiles[self.identifier] = {
            'username': self.username,
            'password': self.password,
            'server': self.server,
            'port': self.port,
            'ssl': self.ssl,
            'webroot': self.webroot
        }

        with open(self.profile_path, 'w') as f:
            json.dump(profiles, f)

    def remove(self):
        with open(self.profile_path, 'w+') as f:
            profiles = json.load(f)
            if self.identifier in profiles.keys():
                del profiles[self.identifier]
                json.dump(profiles, f)

    def load(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r+') as f:
                profiles = json.load(f)
                if self.identifier in profiles.keys():
                    profile = profiles[self.identifier]
                    self.username = profile['username'],
                    self.password = profile['password'],
                    self.ssl = profile['ssl'],
                    self.server = profile['server'],
                    self.port = profile['port'],
                    self.webroot = profile['webroot']
                else:
                    if self.identifier == 'default':
                        print("Please configure default profile !!!")
                        exit(1)
                    else:
                        raise AttributeError(f"Profile {self.identifier} does NOT exists !!!")

    def get_hac_url(self):
        url = "http"
        if self.ssl:
            url += 's'
        url += '://'
        url += self.server[0]
        url += ':'
        url += str(self.port[0])
        url += '/'
        url += self.webroot
        return url
def get_profile_from_user():
    identifier = str(input('Profile identifier (default): ')) or 'default'
    username = str(input('Profile username (admin): ')) or 'admin'
    password = str(input('Profile password (nimda): ')) or 'nimda'
    server = str(input('Profile server (127.0.0.1): ')) or '127.0.0.1'
    port = input('Profile port (9002) :') or 9002
    ssl = False if str(input('Is secured with ssl [Y/n]: ')) == 'n' else True
    webroot = str(input("Profile webroot (/): ")) or '/'

    return Profile(identifier, username, password, server, port, ssl, webroot)
