#!/usr/bin/python
# -*- coding: UTF-8 -*-

import commands

class Ssh():
    host = ""
    copy_id_script = "~/ex_copy_id"
    
    def __init__(self, host="localhost"):
        self.host = host
        
    def checkConnection(self):
        com = "ssh -o BatchMode=yes root@" + self.host + " ls"
        ret_ch = commands.getstatusoutput(com)
        return (ret_ch[0], ret_ch[1])
    
    def doAuth(self, password):
        com = self.copy_id_script + " " + self.host + " " + password
        ret_ch = commands.getstatusoutput(com)
        return (ret_ch[0], ret_ch[1])
        
    def commandAsRoot(self,com):
        comAsRoot = 'ssh -o BatchMode=yes root@' + self.host + ' "' + com + '"'
        #comAsRoot = 'ssh -o BatchMode=yes root@localhost "' + com + '"'
        ret_ch = commands.getstatusoutput(comAsRoot)
        return (ret_ch[0], ret_ch[1])

    def localCommand(self,com):
        ret_ch = commands.getstatusoutput(com)
        return (ret_ch[0], ret_ch[1])
