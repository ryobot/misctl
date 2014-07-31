#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ssh import Ssh

### class Stats ###############
class Stats():
    socket_path = "/var/lib/haproxy/stats"
    ssh = Ssh()

    def getStats(self):
        stats = {}
        com = "echo 'show stat' | socat stdio unix-connect:" + self.socket_path
        (ret,content) = self.ssh.commandAsRoot(com)
        if ret == 0 and content:
            lines = content.splitlines()
            params = lines[0].strip("# ").split(",")
            for i in range(1,len(lines)):
                cols = lines[i].split(",")
                values = {}
                for j in range (0,len(cols)):
                    if params[j]:
                        values[params[j]] = cols[j]
                name = cols[0] + "/" + cols[1]
                stats[name] = values
        return stats
    
    def socketCommand(self, com):
        com = "echo '" + com + "' | socat stdio unix-connect:" + self.socket_path
        (ret,content) = self.ssh.commandAsRoot(com)
        if ret == 0:
            if content:
                return content
            return "[comannd sent]"
        return "[socket command error]: " + content
    
