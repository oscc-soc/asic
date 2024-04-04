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
from typing import Dict, Any
import tomli
import global_para
from config_type import MetaConfig, CoreConfig, RAMConfig
from config_type import FilelistConfig, TopConfig, TBConfig
from config_type import SimConfig, IPConfig
from config_type import SoCConfig


class ConfigParser(object):
    def __init__(self):
        self.soc_cfg = None

    def init(self):
        def_cfg_file = f'{global_para.SRC_DIR}/def_config.toml'
        if os.path.isfile(def_cfg_file):
            with open(def_cfg_file, 'rb') as fp:
                toml_cfg = tomli.load(fp)
                self.inst(toml_cfg)
        else:
            print('error: no def config toml file')

    def inst(self, cfg: Dict[str, Any]):
        tmp_cfg = cfg['meta']
        # print(cfg['meta'])
        meta_cfg = MetaConfig(tmp_cfg['name'], tmp_cfg['user'],
                              tmp_cfg['process'], tmp_cfg['date'],
                              tmp_cfg['gen_dir'], tmp_cfg['version'],
                              tmp_cfg['author'])

        tmp_cfg = cfg['core']
        core_cfg = CoreConfig(tmp_cfg['path'], tmp_cfg['file'], tmp_cfg['top'])

        tmp_cfg = cfg['ram']
        ram_cfg = RAMConfig(tmp_cfg['path'])

        tmp_cfg = cfg['filelist']
        fl_cfg = FilelistConfig(tmp_cfg['path'], tmp_cfg['be'], tmp_cfg['sim'])

        tmp_cfg = cfg['top']
        top_cfg = TopConfig(tmp_cfg['path'])

        tmp_cfg = cfg['tb']
        tb_cfg = TBConfig(tmp_cfg['path'])

        tmp_cfg = cfg['sim']
        sim_cfg = SimConfig(tmp_cfg['path'])

        tmp_cfg = cfg['ip']
        ip_cfg = IPConfig(tmp_cfg['path'], tmp_cfg['perip'], [])

        self.soc_cfg = SoCConfig(meta_cfg, core_cfg, ram_cfg, fl_cfg, top_cfg,
                                 tb_cfg, sim_cfg, ip_cfg)

    def check(self):
        self.init()


if __name__ == '__main__':
    cfg_parser = ConfigParser()
    cfg_parser.check()
