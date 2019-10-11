#!/usr/bin/env python

from configparser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

# Read config.ini and store into variables
HOST = config.get('app', 'HOST')
PORT = int(config.get('app', 'PORT'))
DEBUG = config.get('app', 'DEBUG')

OPENHUBUSER = config.get('openhub', 'OPENHUBUSER')
OPENHUBPASS = config.get('openhub', 'OPENHUBPASS')
