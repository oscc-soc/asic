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

from typing import List


class ModuleInfo(object):
    def __init__(self, raw: str, name: str, paras: List[str],
                 ports: List[str]):
        self.raw = raw
        self.name = name
        self.paras = paras
        self.ports = ports

    def __str__(self) -> str:
        info = f'raw: {self.raw} name: {self.name}'
        info += f' paras: {self.paras} ports: {self.ports}'
        return info


class SVFileInfo(object):
    def __init__(
        self,
        path: str,
        inc: List[str],
        mod: List[ModuleInfo],
    ):
        self.path = path
        self.inc = inc
        self.mod = mod

    def __str__(self) -> str:
        return f'path: {self.path} inc: {self.inc} mod: {self.mod}'
