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

    def __init__(self):
       self. state = self.getStatus()
        
    def getStatus(self):
        com = "service haproxy status"
        (ret, content) = self.ssh.command(com)
        if ret == 0:
            return "running"
        if ret == 3:
            return "stopped"
        return "unknown"
        
    def start(self):
        com = "service haproxy start"
        (ret, content) = self.ssh.commandAsRoot(com)
        if ret:
            self.state = getStatus()
            return "cannot start haproxy"
        self.state = "running"
        return ""
        
    def stop(self):
        com = "service haproxy stop"
        (ret, content) = self.ssh.commandAsRoot(com)
        if ret:
            self.state = getStatus()
            return "cannot stop haproxy"
        self.state = "stopped"
        return ""
        
    def reload(self):
        com = "service haproxy reload"
        (ret, content) = self.ssh.commandAsRoot(com)
        if ret:
            self.state = getStatus()
            return "cannot reload haproxy"
        self.state = "running"
        return ""
