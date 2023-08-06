# SAPCX (SAP CX CLI utility)
[![Deploy to Test PyPI](https://github.com/ablil/sapcx/actions/workflows/test-pypi.yml/badge.svg?branch=dev)](https://github.com/ablil/sapcx/actions/workflows/test-pypi.yml)
[![Deploy to PyPI](https://github.com/ablil/sapcx/actions/workflows/pypi.yml/badge.svg?branch=main)](https://github.com/ablil/sapcx/actions/workflows/pypi.yml)

## Introduction
Why I built this ?? AS a SAP CX (Hybris) developer I found myself using HAC (Hybris adminstration console) a lot, and it's time consuming to open the browser, select each tab, then run simple groovy or some flexible search queries, or whatever is the task to be done.

And since I'm always on my terminal, I thought about looking for a cli for this, but unfortunately didn't find any, then I decided to build it myself for my specific needs, **& I think this is it :sweat_smile:**

## For whoever reading this

This tools is not yet stable, and still in beta version, I'm still working on it while using it in work, **please feel free to contribute, create some pull requests or open some issues for improvement**, they are always welcome

## Get started
### Prerequisites
Obviously you need a local or remote running Hybris server, and an account to access it, & **Python** installed on your machine.

### Installation

Install CLI through pip:
```
$ pip3 install --user --upgrade sapcx
```

Configure default server instance
```bash
$ sap configure
Profile identifier (default): 
Profile username (admin): 
Profile password (nimda): 
Profile server (127.0.0.1): 
Profile port (9002) :
Is secured with ssl [Y/n]: Y
Profile webroot (/): 
```

### Usage
```
usage: sap [-h] [-i IMPORT_IMPEX] [-e EXECUTE_GROOVY] [-q QUERY]
           [--profile PROFILE]
           {configure} ...

positional arguments:
  {configure}           Sub commands help
    configure           Configure different profiles for your servers

optional arguments:
  -h, --help            show this help message and exit

console:
  -i IMPORT_IMPEX, --import IMPORT_IMPEX
                        Impex file to import
  -e EXECUTE_GROOVY, --execute EXECUTE_GROOVY
                        Groovy script file to execute
  -q QUERY, --query QUERY
                        Run flexible search query

server:
  --profile PROFILE
```

## Contribution
Please switch to `dev` branch since most of the work is done there, and there is a github action that automatically push the current vesion to Test PyPI.

