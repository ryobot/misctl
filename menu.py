#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

from ssh import Ssh

class CtlItem():
    service = ""
    host = ""
    label = ""
    auth_check = "Not Ckecked"

class Menu():
    items = None
    selected = -1
    lang = None
    config_path = "/home/webadmin/misctl.conf"
    ssh = Ssh()
    config_label = ""
    
    def __init__(self, select, loc):
        self.load()
        labels = []
        for item in self.items:
            item.label = loc.str('menu_' + item.service)
            cnt = 2
            while item.label in labels:
                item.label = loc.str('menu_' + item.service) + str(cnt)
                cnt += 1
            labels.append(item.label)
        self.config_label = loc.str('menu_config')
        self.selected = int(select)
        self.lang = loc.language
    
    def load(self):
        com = "cat " + self.config_path
        (ret,content) = self.ssh.localCommand(com)
        if ret == 0:
            self.items = self.getCtls(content)

    def save(self):
        com = "echo '## CTL [service] [host]' > " + self.config_path
        self.ssh.localCommand(com)
        for item in self.items:
            str = "CTL " + item.service + " " + item.host
            com = "echo '" + str +"' >> " + self.config_path 
            self.ssh.localCommand(com)

    def getCtls(self, conf):
        lines = conf.splitlines()
        ctlItems = []
        for line in lines:
            columns = line.strip().split()
            if len(columns) > 0 and columns[0][0] == '#':
                continue
            if len(columns) == 0:
                continue
            if columns[0] == "CTL":
                item = CtlItem()
                item.service = columns[1]
                item.host = columns[2]
                ctlItems.append(item)
        return ctlItems
    
    def render(self):
        print("<div id='menu_header'>webadmin</div>")
        print("<div id='menu'><ul class='tabmenu'>")
        for i in range(0, len(self.items)):
            item = self.items[i]
            if i == self.selected:
                print("<li class='act'>" +  item.label + "</li>")
            else:
                print("<li><a href='" + item.service + "_ctl.py?lang=" + self.lang + "&host=" + item.host + "&tab_id=" + str(i) + "' title='" + item.service + ":" + item.host + "'>" +  item.label + "</a></li>")
        # config tab:
        if self.selected == -1:
            print("<li class='act'>" +  self.config_label + "</li>")
        else:
            print("<li><a href='webadmin_config.py?lang=" + self.lang + "&tab_id=-1' >" +  self.config_label + "</a></li>")
        print("</ul></div>")

    def sshAuthCheck(self):
        for item in self.items:
            (ret, msg) = Ssh(item.host).checkConnection()
            if ret == 0:
                item.auth_check = "OK"
            else:
                if "No route" in msg:
                    item.auth_check = "No route to host"
                elif "Host key" in msg:
                    item.auth_check = "Not Authenticated"
                else:
                    item.auth_check = msg
                    