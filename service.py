#!/usr/bin/python
# -*- coding: UTF-8 -*-

#import commands
#import cgi
import os
#import sys
#import datetime

from ssh import Ssh

### class service ######
class Service():
    state = None
    ssh = Ssh()
    name = None

    def __init__(self,name):
       self.name = name
       self. state = self.getStatus()
        
    def getStatus(self):
        com = "service " + self.name +" status"
        (ret, content) = self.ssh.command(com)
        if ret == 0:
            return "running"
        if ret == 3:
            return "stopped"
        return "unknown"
        
    def start(self):
        com = "service " + self.name +" start"
        (ret, content) = self.ssh.commandAsRoot(com)
        if ret:
            self.state = self.getStatus()
            return "cannot start " + self.name +":" + content
        self.state = "running"
        return ""
        
    def stop(self):
        com = "service " + self.name +" stop"
        (ret, content) = self.ssh.commandAsRoot(com)
        if ret:
            self.state = self.getStatus()
            return "cannot stop " + self.name +":" + content
        self.state = "stopped"
        return ""
        
    def reload(self):
        com = "service " + self.name +" reload"
        (ret, content) = self.ssh.commandAsRoot(com)
        if ret:
            self.state = self.getStatus()
            return "cannot reload " + self.name +":" + content
        self.state = "running"
        return ""
