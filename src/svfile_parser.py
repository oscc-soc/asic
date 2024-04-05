#!/bin/python

# Copyright 2017-2020 The Verible Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# -- Adaptable modifications are redistributed under compatible License --
#
# Copyright (c) 2023 Beijing Institute of Open Source Chip
# asic is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#             http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import sys
import os
from typing import List
import anytree
from verible_parser import VeribleParser, SyntaxData
from data_type import ModuleInfo, SVFileInfo
import global_para


class SVFileParser(object):
    def __init__(self):
        self.files = []
        self.vb_parser = VeribleParser(global_para.VERIBLE_SYNTAX)

    def update_files(self, path: List[str]):
        self.files = path

    def gen_ast(self):
        res = self.vb_parser.parse_files(self.files)
        for path, data in res.items():
            self.parse(path, data)

    def parse(self, path: str, data: SyntaxData):
        if not data.tree:
            return

        file_info = SVFileInfo(path, [], [])

        inc_infos = []
        for inc in data.tree.iter_find_all({'tag': ['kPreprocessorInclude']},
                                           iter_=anytree.PreOrderIter):
            if inc:
                tmp_inc = inc.find({'tag': ['TK_StringLiteral']})
                inc_infos.append(tmp_inc.text)

        mod_infos = []
        # Collect information about each module declaration in the file
        for module in data.tree.iter_find_all({'tag': 'kModuleDeclaration'}):
            mod_info = ModuleInfo('', '', [], [])

            # Find module header
            header = module.find({'tag': 'kModuleHeader'})
            if not header:
                continue

            mod_info.raw = header.text

            # Find module name
            name = header.find(
                {'tag': ['SymbolIdentifier', 'EscapedIdentifier']},
                iter_=anytree.PreOrderIter)
            if not name:
                continue

            mod_info.name = name.text

            # Get the list of ports
            for port in header.iter_find_all(
                {'tag': ['kPortDeclaration', 'kPort']}):
                port_id = port.find(
                    {'tag': ['SymbolIdentifier', 'EscapedIdentifier']})
                mod_info.ports.append(port_id.text)

            # Get the list of parameters
            for param in header.iter_find_all({'tag': ['kParamDeclaration']}):
                param_id = param.find(
                    {'tag': ['SymbolIdentifier', 'EscapedIdentifier']})
                mod_info.paras.append(param_id.text)

            # Get the list of imports
            # for pkg in module.iter_find_all({'tag': ['kPackageImportItem']}):
            #     modi
            #     module_info['imports'].append(pkg.text)

            mod_infos.append(mod_info)

        file_info.inc = inc_infos
        file_info.mod = mod_infos

    def format(self):
        fmt_cfg = '--assignment_statement_alignment align --case_items_alignment align --class_member_variable_alignment align --distribution_items_alignment align --enum_assignment_statement_alignment align --formal_parameters_alignment align --module_net_variable_alignment align --named_parameter_alignment align --named_port_alignment align --port_declarations_alignment align --struct_union_members_alignment align'
        fmt_cfg += ' --inplace'
        os.system(f'{global_para.VERIBLE_FORMAT} {fmt_cfg} sub_system.sv')


def integ_soc():
    with open('sub_system.sv', 'w+', encoding='utf-8') as fp:
        res = 'module sub_system();'
        fp.writelines(res)

    with open('sub_system.sv', 'a+', encoding='utf-8') as fp:
        for inc in file_info.inc:
            print(f'inc: {inc}')
            fp.writelines(f'`include {inc}')

        for mod in file_info.mod:
            print(f'name:       {mod.name}')
            print(f'parameters: {mod.paras}')
            print(f'ports:      {mod.ports}')
            # print(f'imports:    {mod["imports"]}')
            # print(f'raw:         {mod.raw}')

            res = mod.name
            # res = 'apb4_uart '
            if len(mod.paras) > 0:
                res += ' #('
                for v in enumerate(mod.paras):
                    if v[0] > 0:
                        res += ','
                    res += f'.{v[1]}({v[1]})'
                res += ')'

            res += f' u_{mod.name}('
            for v in enumerate(mod.ports):
                if v[0] > 0:
                    res += ','
                res += f'.{v[1]}({v[1]})'
            res += ');'
            # print(f'res: {res}')
            fp.writelines(res)

    with open('sub_system.sv', 'a+', encoding='utf-8') as fp:
        fp.writelines('endmodule')


def main():
    svfile_parser = SVFileParser()


if __name__ == '__main__':
    sys.exit(main())
