#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from ssh import Ssh

### config models #############
class section(object):
    name = None
    attributes = []
    params = []
    def __init__(self):
        self.name = None
        self.attributes = []
        self.params = []

class haproxy_cfg(object):
    cfg_path = "/etc/haproxy/haproxy.cfg"
    edit = False
    sections = []

### class Config ###############
class Config():
    data = haproxy_cfg()
    cfg_tmp_path = "/home/haproxy_ctl/haproxy.cfg"
    loadflag_path = "/home/haproxy_ctl/haproxy_ctl_not_config_loaded"
    ssh = Ssh()

    def __init__(self):
        self.data = self.load()

    def setLoaded(self,loaded):
        if loaded and not self.isLoaded():
            com = "rm -f " + self.loadflag_path
            self.ssh.command(com)
        if not loaded and self.isLoaded():
            com = "touch " + self.loadflag_path
            self.ssh.command(com)
    
    def isLoaded(self):
        if os.path.exists(self.loadflag_path):
            return False
        return True
    
    def isSectionHeader(self,key):
        if key == "global" or key == "defaults" or key == "frontend" or key == "backend":
            return True
        return False
    
    def getSections(self,conf):
        lines = conf.splitlines()
        item_list = []
        sections = []
        sec = section()
        for line in lines:
            columns = line.strip().split()
            if len(columns) > 0 and columns[0][0] == '#':
                continue
            if len(columns) == 0:
                continue
            if self.isSectionHeader(columns[0]):
                if sec.name:
                    sections.append(sec)
                    sec = section()
                sec.name = columns[0]
                for i in range(1,len(columns)):
                    sec.attributes.append(columns[i])
                continue
            if sec.name:
                values = []
                for i in range(0,len(columns)):
                    values.append(columns[i])
                sec.params.append(values)
        if sec.name:
            sections.append(sec)
        return sections

    def load(self):
        cfg = haproxy_cfg()
        com = "cat " + cfg.cfg_path
        (ret,content) = self.ssh.command(com)
        if ret == 0:
            cfg.sections = self.getSections(content)
        return cfg
    
    def writeConf(self, line):
        com = "echo '" + line + "' >>" + self.cfg_tmp_path
        self.ssh.command(com)

    def save(self):
        if not self.data.edit:
            return "edit flag not set"
        com = "echo '# config written by haproxy_ctl' > " + self.cfg_tmp_path
        self.ssh.command(com)
        for s in self.data.sections:
            line = s.name
            for a in s.attributes:
                line += " " + a
            self.writeConf(line)
            for p in s.params:
                line = "   "
                for v in p:
                    line += " " + v
                self.writeConf(line)
        com = "cat " + self.cfg_tmp_path + " > " + self.data.cfg_path
        (ret,content) = self.ssh.commandAsRoot(com)
        if ret != 0:
            return content
        self.setLoaded(False)
        return ""
