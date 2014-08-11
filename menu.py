#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Menu():
    items = None
    selected = None
    
    def __init__(self, select, loc):
        self.items = {}
        self.items['iptables'] = loc.str('menu_iptables')
        self.items['haproxy'] = loc.str('menu_haproxy')
        self.items['snort'] = loc.str('menu_snort')
        self.items['squid'] = loc.str('menu_squid')
        self.selected = select
    
    def render(self):
        print("<div id='menu_header'>webadmin</div>")
        print("<div id='menu'><ul class='tabmenu'>")
        for key, value in self.items.items():
            if key == self.selected:
                print("<li class='act'>" +  value + "</li>")
            else:
                print("<li><a href='" + key + "_ctl.py'>" +  value + "</a></li>")
        print("</ul></div>")
        