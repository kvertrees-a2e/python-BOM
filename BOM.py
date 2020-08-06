# MIT License
# 
# Copyright (c) 2020 Rob Siegwart
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Build a multi-level and flattened BOM based on elemental data stored in Excel
files.

Call this program with the the name of the top level BOM file. Output files will
be put into a new sub-directory "publish".

    $ pybom [OPTIONS] TOPLEVELBOM

    Options:
        --supplier     Create individual supplier BOMs
        --tree         Create an ASCII representation of the BOM structure.
        --help         Show this message and exit.
'''

import sys
import glob
import os
# import configparser
import pandas as pd
from numpy import ceil
import click
from anytree import NodeMixin, RenderTree


class BOMProject:
    '''
    The main entry point for assembling BOMs and getting derived information.

    All Excel files in source directory whose name is not in ``MASTER_FILE`` are
    treated as sub-assemblies.

    :param str directory:   The source directory containing BOM files.
    '''
    MASTER_FILE = ['parts list', 'parts_list', 'master']
    """These are the names which identify a file as being a master parts list
    file"""

    def __init__(self, directory):
        self.directory = directory
        self.xlsx_files = [ os.path.split(fn)[-1] for fn in glob.glob(os.path.join(directory, '*.xlsx')) ]
        self.subassem_files = list(filter(lambda x: self.fn_stub(x).lower() not in self.MASTER_FILE, self.xlsx_files))
        self.master_file = list(filter(lambda x: self.fn_stub(x).lower() in self.MASTER_FILE, self.xlsx_files))[0]

        self.subassemblies = [ BOM.from_filename(os.path.join(self.directory, file), name=file) for file in self.subassem_files ]
        self.master = BOM.from_filename(os.path.join(self.directory, self.master_file), name=self.master_file)
    
    def fn_stub(self, filename):
        return '.'.join(filename.split('.')[:-1])

    def generate_structure
    

class BOM(NodeMixin):
    '''
    A Bill-of-material. Can be a parent of another BOM or have several child
    BOMs. At minimum there must be a "PN" column denoting the part name and a
    "QTY" column denoting the quantity of that part. Other columns maybe added
    and are passed through.

        PN        Description   QTY
        --------- ------------- -----
        17954-1   Wheel         2
        17954-2   Axle          1

    :param DataFrame data:      input BOM data
    :param str name:            optional BOM name
    :param BOM parent:          another ``BOM`` object which is the parent
                                assembly
    :param list children:       list of ``BOM`` objects which are sub-assemblies
    '''
    def __init__(self, data, name=None, parent=None, children=None):
        super().__init__()
        self.data = data
        self.name = name
        self.parent = parent
        self.children = children or []

    @classmethod
    def from_filename(cls, filename, **kwargs):
        data = pd.read_excel(filename)
        return cls(data, **kwargs)

    @property
    def fields(self):
        return list(self.data.columns)
    
    @property
    def parts(self):
        return list(self.data['PN'])

    def __repr__(self):
        return f'{self.name} ({len(self.data)} items)' if self.name else f'BOM with {len(self.data)} items'
    
    def __str__(self):
        return self.name + '\n\n' + str(self.data) + '\n'