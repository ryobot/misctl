#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

import cgi
import datetime

from service import Service
from html_parts import *
from menu import Menu
from localize_string import Localize

from iptables_stats import IptablesStats

## main

message = ""

## request params #########
form = cgi.FieldStorage()
req = {
    'refresh':"0", 'service_action':"none" ,'y_scroll':"0", 'lang':"en", 'tab_id' : "0", 'host':"loclahost"
}
for key in req.keys():
    if form.has_key(key):
        req[key] = form[key].value

loc = Localize(req['lang'])
if loc.message:
    message = loc.message

### service ####
service = Service("iptables", req['host'])
if req["service_action"] == "stop":
    message += service.stop()
if req["service_action"] == "start":
    message += service.start()
if req["service_action"] == "reload":
    message += service.reload()

### render html #####

### <html><head>--</head> ####
renderHead(loc.str('menu_iptables'), "", "")

print("<body onLoad='setRefreshTimerAndScroll(" + req["refresh"] + "," + req["y_scroll"] + ")'>")

Menu(req['tab_id'], loc).render()

### form (hidden params) #####
params = { 
    'refresh':req["refresh"], 'y_scroll':'0'
}
HtmlForm("form1", "iptables_ctl.py", "POST", params).render()

print("<div id='header'>")
print("<table style='margin-bottom: 0px;'><tr>")
print("<td style='border: 0;'><h3>"  + loc.str('iptables_title') + "(" + req['host'] + ")</h3></td>")

### auto refresh #####
print("<td style='border: 0;' style='text-align: right;'>" + loc.str('auto_refresh') + "</td>")
print("<td class='actions' style='text-align:left; border: 0;'>")
renderAutoRefresh([30,60], req["refresh"], loc)
print("</td>")

### time stamp #####
now = datetime.datetime.now()
timestamp = now.strftime("%d/%b/%Y:%H:%M:%S") + ".%03d" % (now.microsecond / 1000)
print("<td style='border: 0;'>" + loc.str('last_update') + timestamp + "</td>")

### language #####
print("<td style='border: 0;'><select name='lang' onchange='langSelect()'>")
loc.renderOptions()
print("</select></td>")

print("</tr></table>")
print("</div>")

### contents #####
print("<div id='outer'>")
print("<div id='container'>")

if message:
    print message

# service
renderService(service, loc, "")

stats = IptablesStats(service.getMessage())

if service.state == "running":
    for tablename, table in stats.tables.items():
        renderVSpace(10)
        toggleDefault = "close"
        if tablename == "filter":
            toggleDefault = "open"
        renderToggleDivStart("table_" + tablename, "Table: " + tablename, form, toggleDefault)
        for chainname, chain in table.chains.items():
            print("<table class='notstripe'><tr><td>Chain: " + chainname + " policy " + chain.policy + "</td></tr>")
            if chain.rules:
                print("<tr><td style='border-bottom: 0;'><table class='stripe'>")
                for rule in chain.rules:
                    print("<tr>")
                    print("<td>" + rule.num + "</td>")
                    print("<td>" + rule.target + "</td>")
                    print("<td>" + rule.prot + "</td>")
                    print("<td>" + rule.opt + "</td>")
                    print("<td>" + rule.source + "</td>")
                    print("<td>" + rule.destination + "</td>")
                    print("<td>" + rule.misc + "</td>")
                    print("</tr>")
                print("</table></td></tr>")
            print("</table>")
        print("</div>") #end of toggle div:

print("</div>") #container
print("</div>") #outer

### footer ######
print("<div id='footer'>")
print("webadmin : " + loc.str('iptables_title'))
print("</div>")

print("</form>")

print("</body>")
print("</html>")