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
    'refresh':"0", 'service_action':"none" ,'y_scroll':"0", 'lang':"en"
}
for key in req.keys():
    if form.has_key(key):
        req[key] = form[key].value

loc = Localize(req['lang'])
if loc.message:
    message = loc.message

### get config / service ####
service = Service("iptables")
if req["service_action"] == "stop":
    message += service.stop()
if req["service_action"] == "start":
    message += service.start()
if req["service_action"] == "reload":
    message += service.reload()

### render html #####

### <head>--</head> ####
HtmlHead(loc.str('menu_iptables'), "", "").render()

print("<body onLoad='setRefreshTimerAndScroll(" + req["refresh"] + "," + req["y_scroll"] + ")'>")

Menu("iptables", loc).render()

### form (hidden params) #####
params = { 
    'refresh':req["refresh"], 'y_scroll':'0'
}
HtmlForm("form1", "iptables_ctl.py", "POST", params).render()

print("<div id='header'>")
print("<table style='margin-bottom: 0px;'><tr>")
print("<td style='border: 0;'><h3>"  + loc.str('iptables_title') + "</h3></td>")
print("<td style='border: 0;' style='text-align: right;'>" + loc.str('auto_refresh') + "</td>")
print("<td class='actions' style='text-align:left; border: 0;'>")

### auto refresh #####
if int(req["refresh"]) == 5:
    print("<span>5</span>")
else:
    print("<a href='javascript:setRefresh(5)'>5</a>")
if int(req["refresh"]) == 10:
    print("<span>10</span>")
else:
    print("<a href='javascript:setRefresh(10)'>10</a>")
if int(req["refresh"]) == 30:
    print("<span>30</span>")
else:
    print("<a href='javascript:setRefresh(30)'>30</a>")
if int(req["refresh"]) == 0:
    print("<span>off</span>")
else:
    print("<a href='javascript:setRefresh(0)'>off</a>")
print("<a href='javascript:refresh()'>refresh</a>")

print("</td>")

# time stamp
now = datetime.datetime.now()
timestamp = now.strftime("%d/%b/%Y:%H:%M:%S") + ".%03d" % (now.microsecond / 1000)
print("<td style='border: 0;'>" + loc.str('last_update') + timestamp + "</td>")

# language
print("<td style='border: 0;'><select name='lang' onchange='langSelect()'>")
loc.renderOptions()
print("</select></td>")

print("</tr></table>")
print("</div>")

print("<div id='outer'>")
print("<div id='container'>")

# service
if message:
    print message
print("<table><tr><th width=150>" + loc.str('service_status') + "</th><td width=150>" + service.state + "</td>")
if service.state == "running":
    print("<td class='actions' style='text-align:left;'><a href='javascript:stop()'>" + loc.str('service_stop') + "</a><a href='javascript:reload()'>" + loc.str('service_reload') + "</a></td>")
elif service.state == "stopped":
    print("<td class='actions' style='text-align:left;'><a href='javascript:start()'>" + loc.str('service_start') + "</a></td>")
else:
    print("<td>" + loc.str('no_service_message') + "</td>")    
print("</tr></table>")
    
print("</div>") #container
print("</div>") #outer

### footer ######
print("<div id='footer'>")
print("webadmin : " + loc.str('iptables_title'))
print("</div>")

print("</form>")

print("</body>")
print("</html>")