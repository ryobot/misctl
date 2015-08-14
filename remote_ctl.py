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
from ssh import Ssh

## main

message = ""

## request params #########
form = cgi.FieldStorage()
req = {
    'refresh':"0", 'service_action':"none" ,'y_scroll':"0", 'lang':"en", 'tab_id' : "-99", 'host': "localhost", 'cmd': "ls"
}
for key in req.keys():
    if form.has_key(key):
        req[key] = form[key].value

loc = Localize(req['lang'])
if loc.message:
    message = loc.message

if req['cmd']:
    ssh = Ssh(req['host'])
    com = req['cmd']
    (ret,content) = ssh.commandAsRoot(com)
    if ret == 0 and content:
        message = ""
        lines = content.splitlines()
        for i in range(1,len(lines)):
            message += lines[i] + "<br>"
    else:
        if ret != 0:
            message = "[error] Command failed."
        else:
            message = "[no output]"

### render html #####

### <html><head>--</head> ####
renderHead(loc.str('menu_remote'), "", "remote.js")

print("<body onLoad='focusInput()'>")

Menu(req['tab_id'], loc).render()

### form (hidden params) #####
params = { 
    'refresh':req["refresh"], 'y_scroll':'0', 'tab_id': req['tab_id'], 'host': req['host']
}
HtmlForm("form1", "remote_ctl.py", "POST", params).render()

print("<div id='header'>")
print("<table style='margin-bottom: 0px;'><tr>")
print("<td style='border: 0;'><h3>"  + loc.str('remote_title') + "(" + req['host'] + ")</h3></td>")

### auto refresh #####
#print("<td style='border: 0;' style='text-align: right;'>" + loc.str('auto_refresh') + "</td>")
#print("<td class='actions' style='text-align:left; border: 0;'>")
#renderAutoRefresh([30,60], req["refresh"], loc)
#print("</td>")

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

print("<table><tr><td style='border-bottom: 0;'>")
print("<input type='text' id='cmd_input' size=100 onfocus='this.select()' style='width: 100%;' name='cmd' value='" + req["cmd"] + "'/>")
print("</td><td class='actions' style='vertical-align:middle; border-bottom: 0;'>")
print("<a href='javascript:remoteCommand()'>" + loc.str('submit') + "</a>")
print("</td></tr></table>")

print("<div id='output_area'>")
if message:
    print message
print("</div>")

print("</div>") #container
print("</div>") #outer

### footer ######
print("<div id='footer'>")
print("webadmin : " + loc.str('remote_title'))
print("</div>")

print("</form>")

print("</body>")
print("</html>")