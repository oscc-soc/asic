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

SRC_DIR = f'{os.getcwd()}'
ROOT_DIR = f'{SRC_DIR}/..'
VERIBLE_PATH = '/home/liaoyuchi/Desktop/verible-v0.0-3410-g398a8505'
VERIBLE_BIN_PATH = f'{VERIBLE_PATH}/bin'
VERIBLE_SYNTAX = f'{VERIBLE_BIN_PATH}/verible-verilog-syntax'
VERIBLE_FORMAT = f'{VERIBLE_BIN_PATH}/verible-verilog-format'
