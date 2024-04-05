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
from config_parser import ConfigParser
import global_para
from config_type import SoCConfig
from svfile_parser import SVFileParser


class SoCGen(object):
    def __init__(self, soc_cfg: SoCConfig):
        self.prj_path = ''
        self.soc_cfg = soc_cfg

    def gen_prj(self):
        meta_cfg = self.soc_cfg.meta_cfg
        prj_name = f'{meta_cfg.user}-{meta_cfg.process}'
        prj_name += f'-{meta_cfg.date}-{meta_cfg.name}'
        print(prj_name)
        self.prj_path = f'{global_para.ROOT_DIR}/{meta_cfg.gen_dir}'
        self.prj_path += f'/{prj_name}'
        print(self.prj_path)

        # if os.path.exists(self.prj_path):
            # os.system(f'rm -rf {self.prj_path}')

        # os.system(f'mkdir -p {self.prj_path}')

    def gen_core(self):
        core_cfg = self.soc_cfg.core_cfg
        os.system(f'mkdir -p {self.prj_path}/{core_cfg.path}')

    def gen_ram(self):
        ram_cfg = self.soc_cfg.ram_cfg
        os.system(f'mkdir -p {self.prj_path}/{ram_cfg.path}')

    def gen_filelist(self):
        fl_cfg = self.soc_cfg.fl_cfg
        os.system(f'mkdir -p {self.prj_path}/{fl_cfg.path}')

    def gen_top(self):
        top_cfg = self.soc_cfg.top_cfg
        os.system(f'mkdir -p {self.prj_path}/{top_cfg.path}')

    def gen_tb(self):
        tb_cfg = self.soc_cfg.tb_cfg
        os.system(f'mkdir -p {self.prj_path}/{tb_cfg.path}')

    def gen_sim(self):
        sim_cfg = self.soc_cfg.sim_cfg
        os.system(f'mkdir -p {self.prj_path}/{sim_cfg.path}')

    def gen_ip(self):
        ip_cfg = self.soc_cfg.ip_cfg
        os.system(f'mkdir -p {self.prj_path}/{ip_cfg.path}')
        os.chdir(f'{self.prj_path}/{ip_cfg.path}')
        for v in ip_cfg.perip:
            # os.system(f'git clone https://github.com/oscc-ip/{v}')
            pass

        os.chdir(global_para.SRC_DIR)
        svfile_parser = SVFileParser()
        for v in ip_cfg.perip:
            abs_path = f'{self.prj_path}/{ip_cfg.path}/{v}'
            print(f'abs_path: {abs_path}')
            svfile_parser.update_files(abs_path)

    def gen_sub_block(self):
        self.gen_core()
        self.gen_ram()
        self.gen_filelist()
        self.gen_top()
        self.gen_tb()
        self.gen_sim()
        self.gen_ip()


# read config file
# gen soc project
# gen sub module(core, rcu, bus, ...ip)
def main():
    cfg_parser = ConfigParser()
    cfg_parser.check()
    soc_gen = SoCGen(cfg_parser.soc_cfg)
    soc_gen.gen_prj()
    soc_gen.gen_sub_block()


main()
