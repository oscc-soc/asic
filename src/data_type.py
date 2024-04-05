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
from dataclasses import dataclass, field


@unique
class PortType(IntEnum):
    STD = 0
    IF = 1


@unique
class PortDir(IntEnum):
    IN = 0
    OUT = 1
    INOUT = 2


@dataclass
class SVParam(object):
    dt: str
    name: str
    defval: str


@dataclass
class SVPort(object):
    pt: PortType
    dire: PortDir
    width: str
    name: str


@dataclass
class SVInst(object):
    mid: str
    aid: str


@dataclass
class SVModule(object):
    raw: str = field(repr=False)
    name: str
    params: List[SVParam]
    ports: List[SVPort]
    insts: List[SVInst]


@dataclass
class SVFile(object):
    path: str
    inc: List[str]
    mod: List[SVModule]
