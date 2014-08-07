#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Menu():
    items = None
    selected = None
    
    def __init__(self, select):
        self.items = {}
        self.items['iptables'] = "ファイアウォール"
        self.items['haproxy'] = "ロードバランサ"
        self.items['snort'] = "侵入検知"
        self.items['squid'] = "Webキャッシュ"
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
        