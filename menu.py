#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

from ssh import Ssh

class CtlItem():
    service = ""
    host = ""
    label = ""

class Menu():
    items = None
    selected = -1
    lang = None
    config_path = "/home/webadmin/misctl.conf"
    ssh = Ssh()
    
    def __init__(self, select, loc):
        self.load()
        for item in self.items:
            item.label = loc.str('menu_' + item.service);
        self.selected = int(select)
        self.lang = loc.language
    
    def load(self):
        com = "cat " + self.config_path
        (ret,content) = self.ssh.localCommand(com)
        if ret == 0:
            self.items = self.getCtls(content)

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
                print("<li><a href='" + item.service + "_ctl.py?lang=" + self.lang + "&host=" + item.host + "&tab_id=" + str(i) + "'>" +  item.label + "</a></li>")
        print("</ul></div>")
        