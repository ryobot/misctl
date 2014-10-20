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

    def __init__(self,name,host):
       self.name = name
       self.ssh = Ssh(host)
       self.state = self.getStatus()
        
    def getStatus(self):
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
