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

# module Parapheur

import time

__author__ = 'lhameury'


def __init__():
    pass


def log_to_file(enable_log):
    global __log_to_file__
    __log_to_file__ = enable_log


def do_log(tolog, bold, end, logtype, color):
    if __log_to_file__:
        with open(__log_file__, 'a') as f:
            date = time.strftime("%d/%m/%Y %H:%M:%S")
            print("{0}  {1}  {2}".format(date, logtype, tolog), file=f)
    else:
        print(color + ("", __BOLD__)[bold] + tolog + __ENDC__, end=end)


def log(tolog, bold=False, end='\n'):
    do_log(tolog, bold, end, "LOG", "")


def header(tolog, bold=False, end='\n'):
    do_log(tolog, bold, end, "HEADER", __HEADER__)


def info(tolog, bold=False, end='\n'):
    do_log(tolog, bold, end, "INFO", __OKBLUE__)


def success(tolog, bold=False, end='\n'):
    do_log(tolog, bold, end, "SUCCESS", __OKGREEN__)


def warning(tolog, bold=False, end='\n'):
    do_log(tolog, bold, end, "WARNING", __WARNING__)


def error(tolog, bold=True, end='\n'):
    do_log(tolog, bold, end, "ERROR", __FAIL__)


__log_to_file__ = False
# Set filename and clear it
__log_file__ = "iparapheur-utils.log"
open(__log_file__, 'w').close()

__HEADER__ = '\033[95m'
__OKBLUE__ = '\033[94m'
__OKGREEN__ = '\033[92m'
__WARNING__ = '\033[93m'
__FAIL__ = '\033[91m'
__ENDC__ = '\033[0m'
__BOLD__ = '\033[1m'
__UNDERLINE__ = '\033[4m'
