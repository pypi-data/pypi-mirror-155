#!/usr/bin/env python3

import argparse

cli = argparse.ArgumentParser()
subclis = cli.add_subparsers(help='Sub commands help', dest='subcli')

# sub commands
config_cli = subclis.add_parser('configure', help='Configure different profiles for your servers')

# console
console_group = cli.add_argument_group('console')
console_group.add_argument('-i', '--import', help='Impex file to import', dest='import_impex')
console_group.add_argument('-e', '--execute', help="Groovy script file to execute", dest='execute_groovy')
console_group.add_argument('-q', '--query', help="Run flexible search query", dest='query')

# server config
server_group = cli.add_argument_group('server')
server_group.add_argument('--profile', default='default')
# sub-commands
