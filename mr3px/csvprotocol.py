# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Read and write values in csv format. 

Primarily useful for reading from raw input files. 
Can also output csv if that is your kind of thing.

Definitely NOT recommended for use as an internal protocol. 
"""

import csv
import six

from .common import decode_string


class CsvProtocol(object):

    QUOTABLE_TYPES = [six.text_type, six.string_types, six.binary_type]

    def __init__(self, delimiter=',', quotechar='"'):
        self.delimiter = delimiter
        self.quotechar = quotechar

    def read(self, line):
        """
        read a line of csv data and output a list of values
        converts to unicode using common.decode_string
        """
        data = []
        if six.PY3 and type(line) == six.binary_type:
            line = line.decode('utf-8')

        csv_reader = csv.reader(six.StringIO(line),
                       delimiter=self.delimiter,
                       quotechar=self.quotechar,
                       skipinitialspace=True)
        for cr in csv_reader:
            data = [decode_string(f).strip() for f in cr]
            break

        return None, data

    def write(self, _, data):
        """
        Output a list of values as a comma-separated string
        """
        out = [self.fmt(d) for d in data]
        return ",".join(out).encode('utf-8')

    def fmt(self, val):
        """
        Format the values for common CSV output
        """
        if type(val) in self.QUOTABLE_TYPES:
            s = decode_string(val)
            return u"{0}{1}{2}".format(self.quotechar, s, self.quotechar)
        else:
            return decode_string(str(val))


class CsvSingleQuotedProtocol(CsvProtocol):
    # retaining this for backwards-compatability
    def __init__(self, delimiter=','):
        self.delimiter = delimiter
        self.quotechar = "'"
    

