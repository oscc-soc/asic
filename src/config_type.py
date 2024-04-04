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


class MetaConfig(object):
    def __init__(self, name: str, user: str, process: str, date: str,
                 gen_dir: str, version: str, author: str):
        self.name = name
        self.user = user
        self.process = process
        self.date = date
        self.gen_dir = gen_dir
        self.version = version
        self.author = author

    def __str__(self) -> str:
        info = f'name: {self.name} user: {self.user} process: {self.process}'
        info += f' date: {self.date} gen_dir: {self.gen_dir} version: {self.version}'
        info += f' author: {self.author}'
        return info


class CoreConfig(object):
    def __init__(self, path: str, file: str, top: str):
        self.path = path
        self.file = file
        self.top = top

    def __str__(self) -> str:
        return f'path: {self.path} file: {self.file} top: {self.top}'


class RAMConfig(object):
    def __init__(self, path: str):
        self.path = path

    def __str__(self) -> str:
        return f'path: {self.path}'


class FilelistConfig(object):
    def __init__(self, path: str, bakcend: str, sim: str):
        self.path = path
        self.be = bakcend
        self.sim = sim

    def __str__(self) -> str:
        return f'path: {self.path} be: {self.be} sim: {self.sim}'


class TopConfig(object):
    def __init__(self, path: str):
        self.path = path

    def __str__(self) -> str:
        return f'path: {self.path}'


class TBConfig(object):
    def __init__(self, path: str):
        self.path = path

    def __str__(self) -> str:
        return f'path: {self.path}'


class SimConfig(object):
    def __init__(self, path: str):
        self.path = path

    def __str__(self) -> str:
        return f'path: {self.path}'


class RCUConfig(object):
    def __init__(self, path: str, pllnum: int, bypass: bool):
        self.path = path
        self.pllnum = pllnum
        self.bypass = bypass


class BusConfig(object):
    def __init__(self):
        pass


class IPPackage(object):
    def __init__(self, branch: str, commit: str, pinmux: bool):
        self.branch = branch
        self.commit = commit
        self.pinmux = pinmux

    def __str__(self) -> str:
        return f'branch: {self.branch} commit: {self.commit} pinmux: {self.pinmux}'


class IPConfig(object):
    def __init__(self, path: str, perip: List[str], ip: List[IPPackage]):
        self.path = path
        self.perip = perip
        self.ip = ip

    def __str__(self) -> str:
        return f'path: {self.path} perip: {self.perip} ip: {self.ip}'


class SoCConfig(object):
    def __init__(self, meta_cfg: MetaConfig, core_cfg: CoreConfig,
                 ram_cfg: RAMConfig, fl_cfg: FilelistConfig,
                 top_cfg: TopConfig, tb_cfg: TBConfig, sim_cfg: SimConfig,
                 ip_cfg: IPConfig):
        self.meta_cfg = meta_cfg
        self.core_cfg = core_cfg
        self.ram_cfg = ram_cfg
        self.fl_cfg = fl_cfg
        self.top_cfg = top_cfg
        self.tb_cfg = tb_cfg
        self.sim_cfg = sim_cfg
        # self.rcu_cfg = rcu_cfg
        # self.bus_cfg = bus_cfg
        self.ip_cfg = ip_cfg

    def __str__(self) -> str:
        info = f'meta_cfg: {self.meta_cfg} core_cfg: {self.core_cfg}'
        info += f' ram_cfg: {self.ram_cfg} fl_cfg: {self.fl_cfg}'
        info += f' top_cfg: {self.top_cfg} tb_cfg: {self.tb_cfg}'
        info += f' sim_cfg: {self.sim_cfg} ip_cfg {self.ip_cfg}'
        return info
