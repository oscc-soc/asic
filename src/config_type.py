#!/bin/python

# Copyright (c) 2023 Beijing Institute of Open Source Chip
# ci is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#             http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from typing import List, Tuple


class CoreConfig(object):
    def __init__(self, path: str, file: str, top: str):
        self.path = path
        self.file = file
        self.top = top


class RAMConfig(object):
    def __init__(self, path: str):
        self.path = path


class FilelistConfig(object):
    def __init__(self, path: str, bakcend: str, sim: str):
        self.path = path
        self.backend = bakcend
        self.sim = sim


class TopConfig(object):
    def __init__(self, path: str):
        self.path = path


class TBConfig(object):
    def __init__(self, path: str):
        self.path = path


class SimConfig(object):
    def __init__(self, path: str):
        self.path = path


class RCUConfig(object):
    def __init__(self, path: str, pllnum: int, bypass: bool):
        self.path = path
        self.pllnum = pllnum
        self.bypass = bypass


class BusConfig(object):
    def __init__(self):
        pass


class IPPackage(object):
    def __init__(self, repo: str, branch: str, commit: str, pinmux: bool):
        self.repo = repo
        self.branch = branch
        self.commit = commit
        self.pinmux = pinmux


class IPConfig(object):
    def __init__(self, path: str, ip: List[IPPackage]):
        self.path = path
        self.ip = ip
