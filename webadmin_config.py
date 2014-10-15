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
    'lang':"en", 'tab_id' : "0", 'config_action': 'none', 'service_id': '-1', 'service': 'none', 'host': 'none', 'passwd': ''
}
for key in req.keys():
    if form.has_key(key):
        req[key] = form[key].value

loc = Localize(req['lang'])
if loc.message:
    message = loc.message

menu = Menu(req['tab_id'], loc)

## actions

if req['config_action'] == "delete_service":
    if int(req['service_id']) >= 0:
        menu.items.pop(int(req['service_id']));
        menu.save();
        menu = Menu(req['tab_id'], loc)
        
if req['config_action'] == "add_service":
    if req['service'] != "none" and req['host'] != "none" :
        item = CtlItem()
        item.service = req['service']
        item.host = req['host']
        menu.items.append(item);
        menu.save();
        menu = Menu(req['tab_id'], loc)

if req['config_action'] == "do_auth":
    if req['service_id'] != "none" and req['passwd'] != "":
        (ret, msg) = Ssh(menu.items[int(req['service_id'])].host).doAuth(req['passwd'])
        if ret:
            message += "SSH key not authenticated on remote host. " + msg

menu.sshAuthCheck()

### render html #####

### <html><head>--</head> ####
renderHead(loc.str('menu_config'), "", "webadmin_config.js")

print("<body>")

menu.render()

### form (hidden params) #####
params = { 
    'tab_id' : req['tab_id'], 'config_action': 'none', 'service_id': '-1', 'passwd': ''
}
HtmlForm("form1", "webadmin_config.py", "POST", params).render()

print("<div id='header'>")
print("<table style='margin-bottom: 0px;'><tr>")
print("<td style='border: 0;'><h3>"  + loc.str('config_title') + "</h3></td>")

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
print("<tr><th width=200>" + loc.str("Service") + "</th><th width=200>" + loc.str("Application") + "</th><th width=200>" + loc.str("Host") + "</th><th width=200>" + loc.str("ssh_login") + "</th><td>&nbsp;</td></tr>" )
for i in range(0, len(menu.items)):
    item = menu.items[i]
    print("<tr>")
    print("<td>" + item.label + "</td><td>" + item.service + "</td><td>" + item.host + "</td>")
    if item.auth_check == "Not Authenticated":
        print("<td class='actions'><b><font color=red>" + item.auth_check + "</font></b> <a href='javascript:doAuth(" + str(i) + ', "' + loc.str_name('ssh_auth_message', item.host) + '"' + ")'>" + loc.str('ssh_auth') + "</a></td>")
    else:
        if item.auth_check == "OK":
            print("<td><b><font color=green>" + item.auth_check + "</font></b></td>")
        else:
            print("<td><b><font color=gray>" + item.auth_check + "</font></b></td>")
    print("<td class='actions' style='text-align: left;'><a href='javascript:deleteService(" + str(i) + ', "' + loc.str_name('delete_service_message', item.service, item.host) + '"' + ")'>" + loc.str('btn_delete') + "</a></td>")
    print("</tr>" )
if len(menu.items) == 0:
    print("<tr><td colspan=5>" + loc.str('no_cp_msg') + "</td></tr>")
print("</table>")

print("<h1>" + loc.str('add_cp') + "</h1>")
print("<table class='notfull'>")
print("<tr><th width=200>" + loc.str("Service") + "</th><td width=200><select name='service'>")
print("<option value='iptables'>" + loc.str("menu_iptables") + "(iptables)</option>")
print("<option value='haproxy'>" + loc.str("menu_haproxy") + "(haproxy)</option>")
print("<option value='snort'>" + loc.str("menu_snort") + "(snort)</option>")
print("<option value='squid'>" + loc.str("menu_squid") + "(squid)</option>")
print("</select></td></tr>")
print("<tr><th>" + loc.str("Host") + "</th><td><input type='text' name='host' size=20></td></tr>")
print("<tr><td class='actions' style='border: 0px; text-align: left;'><a href='javascript:addService()'>" + loc.str('btn_add') + "</a></td></tr>")
print("</table>")

print("</div>") #container
print("</div>") #outer

### footer ######
print("<div id='footer'>")
print("webadmin : " + loc.str('config_title'))
print("</div>")

print("</form>")

print("</body>")
print("</html>")