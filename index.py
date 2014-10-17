#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

import cgi
import datetime

from service import Service
from html_parts import *
from menu import *
from localize_string import Localize

## main

message = ""

## request params #########
form = cgi.FieldStorage()
req = {
    'lang':"ja", 'tab_id' : "-99"
}
for key in req.keys():
    if form.has_key(key):
        req[key] = form[key].value

loc = Localize(req['lang'])
if loc.message:
    message = loc.message

menu = Menu(req['tab_id'], loc)

### render html #####

### <html><head>--</head> ####
renderHead(loc.str('menu_index'), "", "")

print("<body>")

menu.render()

### form (hidden params) #####
params = { 
   'tab_id' : req['tab_id']
}
HtmlForm("form1", "index.py", "POST", params).render()

print("<div id='header'>")
print("<table style='margin-bottom: 0px;'><tr>")
print("<td style='border: 0;'><h3>"  + loc.str('index_title') + "</h3></td>")

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
    
print("<table>")
print("<tr><th width=200>" + loc.str("Service") + "</th><th width=200>" + loc.str("Application") + "</th><th width=200>" + loc.str("Host") + "</th></tr>" )
for i in range(0, len(menu.items)):
    item = menu.items[i]
    print("<tr>")
    print("<td><a href='" + item.service + "_ctl.py?lang=" + loc.language + "&host=" + item.host + "&tab_id=" + str(i) + "' title='" + item.service + ":" + item.host + "'>" + item.label + "</td><td>" + item.service + "</td><td>" + item.host + "</td>")
    print("</tr>" )
if len(menu.items) == 0:
    print("<tr><td colspan=3>" + loc.str('no_cp_msg') + "</td></tr>")
print("</table>")
print("<a href='webadmin_config.py?lang=" + loc.language + "&tab_id=-1' >" +  loc.str('menu_config') + "</a>")

print("</div>") #container
print("</div>") #outer

### footer ######
print("<div id='footer'>")
print("webadmin : " + loc.str('index_title'))
print("</div>")

#print("</form>")

print("</body>")
print("</html>")