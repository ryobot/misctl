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

## main

message = ""

## request params #########
form = cgi.FieldStorage()
req = {
    'refresh':"0", 'service_action':"none" ,'y_scroll':"0", 'lang':"en", 'tab_id' : "-99", 'host': "localhost"
}
for key in req.keys():
    if form.has_key(key):
        req[key] = form[key].value

loc = Localize(req['lang'])
if loc.message:
    message = loc.message

### service ####
service = Service("squid", req['host'])
if req["service_action"] == "stop":
    message += service.stop()
if req["service_action"] == "start":
    message += service.start()
if req["service_action"] == "reload":
    message += service.reload()

### render html #####

### <html><head>--</head> ####
renderHead(loc.str('menu_squid'), "", "")

print("<body onLoad='setRefreshTimerAndScroll(" + req["refresh"] + "," + req["y_scroll"] + ")'>")

Menu(req['tab_id'], loc).render()

### form (hidden params) #####
params = { 
    'refresh':req["refresh"], 'y_scroll':'0', 'tab_id': req['tab_id']
}
HtmlForm("form1", "squid_ctl.py", "POST", params).render()

print("<div id='header'>")
print("<table style='margin-bottom: 0px;'><tr>")
print("<td style='border: 0;'><h3>"  + loc.str('squid_title') + "(" + req['host'] + ")</h3></td>")

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
msg = ""
renderService(service, loc, msg)
    
print("</div>") #container
print("</div>") #outer

### footer ######
print("<div id='footer'>")
print("webadmin : " + loc.str('squid_title'))
print("</div>")

print("</form>")

print("</body>")
print("</html>")