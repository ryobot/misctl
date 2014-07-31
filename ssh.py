#!/usr/bin/python
# -*- coding: UTF-8 -*-

import commands

class Ssh():
    
    def commandAsRoot(self,com):
        comAsRoot = 'ssh root@localhost "' + com + '"'
        ret_ch = commands.getstatusoutput(comAsRoot)
        return (ret_ch[0], ret_ch[1])

    def command(self,com):
        ret_ch = commands.getstatusoutput(com)
        return (ret_ch[0], ret_ch[1])
