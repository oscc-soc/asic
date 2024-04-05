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
from enum import IntEnum, unique


@unique
class PortDir(IntEnum):
    IN = 0
    OUT = 1
    INOUT = 2


class SVParam(object):
    def __init__(self, name: str, defval: str):
        self.name = name
        self.defval = defval

    def __str__(self) -> str:
        return f'name: {self.name} defval: {self.defval}'


class SVPort(object):
    def __init__(self, dire: PortDir, width: str, name: str):
        self.dire = dire
        self.width = width
        self.name = name

    def __str__(self) -> str:
        return f'dire: {self.dire} width: {self.width} name: {self.name}'


class SVModule(object):
    def __init__(self, name: str, params: List[SVParam], ports: List[SVPort]):
        self.name = name
        self.params = params
        self.ports = ports

    def __str__(self) -> str:
        info = f'name: {self.name} params: {self.params} ports: {self.ports}'
        return info


class SVFile(object):
    def __init__(
        self,
        path: str,
        inc: List[str],
        mod: List[SVModule],
    ):
        self.path = path
        self.inc = inc
        self.mod = mod

    def __str__(self) -> str:
        return f'path: {self.path} inc: {self.inc} mod: {self.mod}'
