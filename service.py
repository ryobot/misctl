#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

from ssh import Ssh

### class service ######
class Service():
    state = None
    ssh = None
    name = None
    content = None
    os_version = "el6"

    def __init__(self,name,host):
       self.name = name
       self.ssh = Ssh(host)
       self.os_version = self.getOSVersion()
       self.state = self.getStatus()
        
    def getOSVersion(self):
        com = "uname -r"
        (ret, val) = self.ssh.commandAsRoot(com)
        if val.find("el6") > -1:
            return "el6"
        elif val.find("el7") > -1:
            return "el7"
        else:
            return "unknown"
    
    def getStatus(self):
        if self.os_version == "el7":
            if self.name == "iptables":
                com = "iptables -V"
                (ret, self.content) = self.ssh.commandAsRoot(com)
                if ret == 0:
                    (ret, content) = self.ssh.commandAsRoot("iptables -L")
                    self.content = "table: filter\r" + content
                    (ret, content) = self.ssh.commandAsRoot("iptables -L -t nat")
                    self.content += "\rtable: nat\r" + content
                    (ret, content) = self.ssh.commandAsRoot("iptables -L -t mangle")
                    self.content += "\rtable: mangle\r" + content
                    return "running"
                if ret == 3:
                    return "stopped"
                return "unknown :" + str(ret)
            return "OS(el7) not supported."
        com = "service " + self.name +" status"
        (ret, self.content) = self.ssh.commandAsRoot(com)
        ret = ret >> 8;
        if ret == 0:
            return "running"
        if ret == 3:
            return "stopped"
        return "unknown :" + str(ret)
        
    def start(self):
        com = "service " + self.name +" start"
        (ret, self.content) = self.ssh.commandAsRoot(com)
        if ret:
            self.state = self.getStatus()
            return "cannot start " + self.name +":" + self.content
        self.state = "running"
        return ""
        
    def stop(self):
        com = "service " + self.name +" stop"
        (ret, self.content) = self.ssh.commandAsRoot(com)
        if ret:
            self.state = self.getStatus()
            return "cannot stop " + self.name +":" + self.content
        self.state = "stopped"
        return ""
        
    def reload(self):
        com = "service " + self.name +" reload"
        (ret, self.content) = self.ssh.commandAsRoot(com)
        if ret:
            self.state = self.getStatus()
            return "cannot reload " + self.name +":" + self.content
        self.state = "running"
        return ""
    
    def getMessage(self):
        return self.content
