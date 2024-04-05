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
from data_type import PortType, PortDir, SVInst, SVParam, SVPort, SVModule, SVFile
import global_para


class SVFileParser(object):
    def __init__(self):
        self.src_files = []
        self.sv_files = []
        self.vb_parser = VeribleParser(global_para.VERIBLE_SYNTAX)

    def clear(self):
        self.src_files = []
        self.sv_files = []

    def update_files(self, files: List[str]):
        self.src_files = files

    def gen_ast(self):
        if len(self.src_files) > 0:
            res = self.vb_parser.parse_files(self.src_files)
            for path, data in res.items():
                self.parse(path, data)

    def parse(self, path: str, data: SyntaxData):
        if not data.tree:
            return

        inc_infos = []
        for inc in data.tree.iter_find_all({'tag': ['kPreprocessorInclude']},
                                           iter_=anytree.PreOrderIter):
            if inc:
                tmp_inc = inc.find({'tag': ['TK_StringLiteral']})
                inc_infos.append(tmp_inc.text)

        mod_infos = []
        # Collect information about each module declaration in the file
        for module in data.tree.iter_find_all({'tag': 'kModuleDeclaration'}):
            mod_info = SVModule('', '', [], [], [])

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

            # Get the list of parameters
            for param in header.iter_find_all({'tag': ['kParamDeclaration']}):
                param_pt = param.find({'tag': ['kParamType']})
                param_dt = param_pt.find({'tag': ['kTypeInfo']})
                param_id = param_pt.find({'tag': ['SymbolIdentifier']})
                param_ta = param.find({'tag': ['kTrailingAssign']})
                param_defval = param_ta.find({'tag': ['kExpression']})
                mod_info.params.append(
                    SVParam(param_dt.text, param_id.text, param_defval.text))

            # Get the list of ports
            for port in header.iter_find_all(
                {'tag': ['kPortDeclaration', 'kPort']}):
                port_id = port.find({'tag': ['SymbolIdentifier']})
                if_node = port.find({'tag': ['kInterfacePortHeader']})
                if if_node:
                    mod_info.ports.append(
                        SVPort(PortType.IF, PortDir.IN, '', port_id.text))
                else:
                    mod_info.ports.append(
                        SVPort(PortType.STD, PortDir.IN, '', port_id.text))

            # Get the lists of module insts
            for v in module.iter_find_all({'tag': ['kGateInstance']}):
                inst = v.parent.parent
                inst_it = inst.find({'tag': ['kInstantiationType']})
                inst_mid = inst_it.find({'tag': ['SymbolIdentifier']})
                inst_aid = v.find({'tag': ['SymbolIdentifier']})
                mod_info.insts.append(SVInst(inst_mid.text, inst_aid.text))

            mod_infos.append(mod_info)
        self.sv_files.append(SVFile(path, inc_infos, mod_infos))

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
            print(f'parameters: {mod.params}')
            print(f'ports:      {mod.ports}')
            # print(f'imports:    {mod["imports"]}')
            # print(f'raw:         {mod.raw}')

            res = mod.name
            # res = 'apb4_uart '
            if len(mod.params) > 0:
                res += ' #('
                for v in enumerate(mod.params):
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
    svfile_parser.update_files([
        '/home/liaoyuchi/Desktop/oscc/asic/gen/oscc-t28-202404-soc/perip/uart/rtl/apb4_uart.sv',
        '/home/liaoyuchi/Desktop/oscc/asic/gen/oscc-t28-202404-soc/perip/uart/rtl/uart_tx.sv'
    ])
    svfile_parser.gen_ast()

    for v in svfile_parser.sv_files:
        print(v)


if __name__ == '__main__':
    sys.exit(main())
