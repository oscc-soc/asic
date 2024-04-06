#!/bin/python

# Copyright (c) 2023 Beijing Institute of Open Source Chip
# asic is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#             http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import os
from typing import List
import global_para
from data_type import SVModule


class SVFileGen(object):
    def __init__(self, file_path: str, mod_name: str,
                 inst_mods: List[SVModule]):
        self.file_path = file_path
        self.mod_name = mod_name
        self.inst_mods = inst_mods

    def format(self, file_path: str):
        fmt_cfg = '--assignment_statement_alignment align --case_items_alignment align --class_member_variable_alignment align --distribution_items_alignment align --enum_assignment_statement_alignment align --formal_parameters_alignment align --module_net_variable_alignment align --named_parameter_alignment align --named_port_alignment align --port_declarations_alignment align --struct_union_members_alignment align'
        fmt_cfg += ' --inplace'
        os.system(f'{global_para.VERIBLE_FORMAT} {fmt_cfg} {file_path}')

    def gen(self):
        def_res = ''
        inc_res = ''
        mod_res = f'module {self.mod_name}();'
        for mod in self.inst_mods:
            print(f'name:       {mod.name}')
            print(f'parameters: {mod.params}')
            print(f'ports:      {mod.ports}')
            mod_res += mod.name
            # # mod_res = 'apb4_uart '
            if len(mod.params) > 0:
                mod_res += ' #('
                for v in enumerate(mod.params):
                    if v[0] > 0:
                        mod_res += ','
                    mod_res += f'.{v[1].name}({mod.name.upper()}_{v[1].name})'
                    def_res += f'`define {mod.name.upper()}_{v[1].name} = {v[1].defval}\n'
                mod_res += ')'
            mod_res += f' u_{mod.name}('
            for v in enumerate(mod.ports):
                if v[0] > 0:
                    mod_res += ','
                mod_res += f'.{v[1].name}({mod.name}_{v[1].name})'
            mod_res += ');\n\n'
            # print(f'mod_res: {mod_res}')
        mod_res += 'endmodule'

        abs_file_path = f'{self.file_path}/{self.mod_name}.sv'
        with open(abs_file_path, 'w+', encoding='utf-8') as fp:
            fp.writelines(f'{def_res}\n\n')
            fp.writelines(f'{inc_res}\n\n')
            fp.writelines(mod_res)

        self.format(abs_file_path)
