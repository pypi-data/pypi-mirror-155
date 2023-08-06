# coding=utf-8

#  i-Parapheur Utils
#  Copyright (C) 2017-2022 Libriciel-SCOP
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

# module ParapheurModule

import os
from shutil import copyfile
from .Client import Client
from .Webservice import Webservice

import requests
from configparser import ConfigParser

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

__author__ = 'lhameury'

# Récuperation du fichier de propriétés
config = ConfigParser()
real_config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'script.cfg')
if os.path.isfile("./iparapheur-utils.cfg"):
    real_config_path = "./iparapheur-utils.cfg"
config.read(real_config_path)


def copyconfig(filename, path):
    configpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../configs', filename + '.cfg')
    copyfile(configpath, os.path.join(path, "iparapheur-utils.cfg"))


def setconfig(path):
    global config, real_config_path
    # Récuperation du fichier de propriétés
    config = ConfigParser()
    config.read([real_config_path, path])


def setconfigproperty(section, propertyname, value):
    config.set(section, propertyname, value)


def getrestclient():
    return Client(config)


def getsoapclient(user=None, password=None):
    if user is not None and password is not None:
        return Webservice(config, user, password)
    else:
        return Webservice(config)
