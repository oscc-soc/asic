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
import verible_parser


class ModuleInfo(object):
    def __init__(self, path: str, raw: str, inc: str, name: str,
                 para: List[str], ports: List[str]):
        self.path = path
        self.raw = raw
        self.inc = inc
        self.name = name
        self.para = para
        self.ports = ports

    def __str__(self) -> str:
        return f'path: {self.path} name: {self.name} para: {self.para}'


def process_file_data(path: str, data: verible_parser.SyntaxData):
    if not data.tree:
        return

    mod_infos = []
    # Collect information about each module declaration in the file
    for module in data.tree.iter_find_all({'tag': 'kModuleDeclaration'}):
        mod_info = ModuleInfo(path, '', '', '', [], [])

        for inc in data.tree.iter_find_all({'tag': ['kPreprocessorInclude']},
                                           iter_=anytree.PreOrderIter):
            if inc:
                tmp_inc = inc.find({'tag': ['TK_StringLiteral']})
                print(f'tmp_inc: {tmp_inc.text}')
        # Find module header
        header = module.find({'tag': 'kModuleHeader'})
        if not header:
            continue

        mod_info.raw = header.text

        # Find module name
        name = header.find({'tag': ['SymbolIdentifier', 'EscapedIdentifier']},
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
            mod_info.para.append(param_id.text)

        # Get the list of imports
        # for pkg in module.iter_find_all({'tag': ['kPackageImportItem']}):
        #     modi
        #     module_info['imports'].append(pkg.text)

        mod_infos.append(mod_info)

    with open('sub_system.sv', 'a+', encoding='utf-8') as fp:
        for inst_info in mod_infos:
            print(f'path:       {inst_info.path}')
            print(f'name:       {inst_info.name}')
            print(f'parameters: {inst_info.para}')
            print(f'ports:      {inst_info.ports}')
            # print(f'imports:    {inst_info["imports"]}')
            # print(f'raw:         {inst_info.raw}')

            res = inst_info.name
            # res = 'apb4_uart '
            if len(inst_info.para) > 0:
                res += ' #('
                for v in enumerate(inst_info.para):
                    if v[0] > 0:
                        res += ','
                    res += f'.{v[1]}({v[1]})'
                res += ')'

            res += f' u_{inst_info.name}('
            for v in enumerate(inst_info.ports):
                if v[0] > 0:
                    res += ','
                res += f'.{v[1]}({v[1]})'
            res += ');'
            # print(f'res: {res}')
            fp.writelines(res)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} VERILOG_FILE [VERILOG_FILE [...]]")
        return 1

    verible_bin_path = '/home/liaoyuchi/Desktop/verible-v0.0-3410-g398a8505/bin'
    parser_path = f'{verible_bin_path}/verible-verilog-syntax'
    format_path = f'{verible_bin_path}/verible-verilog-format'
    files = sys.argv[1:]

    parser = verible_parser.VeribleParser(exec_path=parser_path)
    data = parser.parse_files(files)

    with open('sub_system.sv', 'w+', encoding='utf-8') as fp:
        res = 'module sub_system();'
        fp.writelines(res)

    for file_path, file_data in data.items():
        process_file_data(file_path, file_data)

    fmt_cfg = '--assignment_statement_alignment align --case_items_alignment align --class_member_variable_alignment align --distribution_items_alignment align --enum_assignment_statement_alignment align --formal_parameters_alignment align --module_net_variable_alignment align --named_parameter_alignment align --named_port_alignment align --port_declarations_alignment align --struct_union_members_alignment align'
    fmt_cfg += ' --inplace'
    # print(f'fmt_cfg: {fmt_cfg}')

    with open('sub_system.sv', 'a+', encoding='utf-8') as fp:
        fp.writelines('endmodule')

    os.system(f'{format_path} {fmt_cfg} sub_system.sv')


if __name__ == '__main__':
    sys.exit(main())
