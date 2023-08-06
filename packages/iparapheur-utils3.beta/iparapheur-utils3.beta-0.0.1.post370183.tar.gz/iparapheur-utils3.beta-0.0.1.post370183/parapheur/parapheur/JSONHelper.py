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

import json
import sys

__author__ = 'lhameury'

req_version = (3, 0)
cur_version = sys.version_info
isp3 = cur_version >= req_version


class ParapheurParseType(type):
    def __str__(self):
        toprint = []
        attrs = vars(self)
        for var in attrs.items():
            if "__" not in var[0]:
                toprint.append(var)
        return ', '.join("%s: %s" % item for item in toprint).encode('utf-8')

    def __getitem__(self, key):
        attrs = vars(self)
        for item in attrs.items():
            if key == item[0]:
                return item[1]
        return ""

    def __iter__(self):
        for each in self.__dict__.keys():
            if each[:2] != '__':
                yield self.__getitem__(each)

    def iterkeys(self):
        for each in self.__dict__.keys():
            if each[:2] != '__':
                yield each

    def items(self):
        return [(key, self.__getitem__(key)) for key in self.iterkeys()]

    def copy(self):
        return dict((k, v) for k, v in self.items())


# JSON Helper
def json_to_obj(s):
    def h2o(x):
        if isinstance(x, dict):
            n = {}
            if isp3:
                for k, v in x.items():
                    n[k] = h2o(v)
            else:
                # noinspection PyCompatibility
                for k, v in iter(x.items()):
                    n[k] = h2o(v)
            return ParapheurParseType('jo', (), n)
        if isinstance(x, list):
            element = []
            for v in x:
                element.append(h2o(v))
            return element
        if isinstance(x, str):
            return x.encode('utf-8')
        else:
            return x

    return h2o(json.loads(s))
