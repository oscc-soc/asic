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
import anytree
import verible_parser


def process_file_data(path: str, data: verible_parser.SyntaxData):
    if not data.tree:
        return

    modules_info = []
    # Collect information about each module declaration in the file
    for module in data.tree.iter_find_all({'tag': 'kModuleDeclaration'}):
        module_info = {
            'header_text': "",
            'name': "",
            'ports': [],
            'parameters': [],
            'imports': [],
        }

        # Find module header
        header = module.find({'tag': 'kModuleHeader'})
        if not header:
            continue
        module_info['header_text'] = header.text

        # Find module name
        name = header.find({'tag': ['SymbolIdentifier', 'EscapedIdentifier']},
                           iter_=anytree.PreOrderIter)
        if not name:
            continue
        module_info['name'] = name.text
        print(f'name.text={name.text}')
        # Get the list of ports
        for port in header.iter_find_all(
            {'tag': ['kPortDeclaration', 'kPort']}):
            port_id = port.find(
                {'tag': ['SymbolIdentifier', 'EscapedIdentifier']})
            module_info['ports'].append(port_id.text)

        # Get the list of parameters
        for param in header.iter_find_all({'tag': ['kParamDeclaration']}):
            param_id = param.find(
                {'tag': ['SymbolIdentifier', 'EscapedIdentifier']})
            module_info['parameters'].append(param_id.text)

        # Get the list of imports
        for pkg in module.iter_find_all({'tag': ['kPackageImportItem']}):
            module_info['imports'].append(pkg.text)

        modules_info.append(module_info)

    # Print results
    if len(modules_info) > 0:
        print(path)

    def print_entry(key, values):
        print(key)
        print(values)

    for module_info in modules_info:
        print_entry("name:       ", [module_info['name']])
        print_entry("ports:      ", module_info['ports'])
        print_entry("parameters: ", module_info['parameters'])
        print_entry("imports:    ", module_info['imports'])
        print(f"\033[97m{module_info['header_text']}\033[0m\n")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} VERILOG_FILE [VERILOG_FILE [...]]")
        return 1

    parser_path = '/home/liaoyuchi/Desktop/verible-v0.0-3410-g398a8505/bin/verible-verilog-syntax'
    files = sys.argv[1:]

    parser = verible_parser.VeribleParser(exec_path=parser_path)
    data = parser.parse_files(files)

    for file_path, file_data in data.items():
        process_file_data(file_path, file_data)


if __name__ == '__main__':
    sys.exit(main())
