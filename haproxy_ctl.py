#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

#import commands
import cgi
import datetime

from service import Service
from haproxy_config import HaproxyConfig
from haproxy_log import HaproxyHttpLog
from haproxy_stats import HaproxyStats
from html_parts import *
from menu import Menu
from localize_string import Localize

## main

message = ""

## request params #########
form = cgi.FieldStorage()
req = {
    'refresh':"10", 'editServer':"none", 'save':"no", 'service_action':"none", 'addServer':"none", 'delServer':"none",
    'weightServer':"none", 'name':"new_server", 'ip_port':"0.0.0.0:80", 'cookie':"new_server", 'settings':"check weight 10",
    'y_scroll':"0", 'socket_command':"", 'lang':"en"
}
for key in req.keys():
    if form.has_key(key):
        req[key] = form[key].value

loc = Localize(req['lang'])
if loc.message:
    message = loc.message

### get config / service ####
config = HaproxyConfig()
service = Service("haproxy")
if req["service_action"] == "stop":
    message += service.stop()
if req["service_action"] == "start":
    message += service.start()
    config.setLoaded(True)
    req["refresh"] = "10"
if req["service_action"] == "reload":
    message += service.reload()
    config.setLoaded(True)
    req["refresh"] = "10"

### edit server ###
if req["editServer"] != "none" and req["save"] == "yes":
    for sec in config.data.sections:
        if sec.name == "backend":
            for p in sec.params:
                if p[0] == "server" and p[1] == req["editServer"]:
                    p[1] = req["name"]
                    p[2] = req["ip_port"]
                    pos = 3
                    for i in range(3,len(p)):
                        if pos >= len(p):
                            break
                        if p[pos] != "cookie" and p[pos-1] != "cookie":
                            p.pop(pos)
                        else:
                            if p[pos-1] == "cookie":
                                p[pos] = req["cookie"]
                            pos += 1
                    cols = req["settings"].strip().split()
                    for col in cols:
                        p.append(col)
                    config.data.edit = True
    message += config.save()
    req["editServer"] = "none"

### add server ####
if req["addServer"] != "none":
    for sec in config.data.sections:
        if sec.name == "backend":
            add = []
            add.append("server")
            add.append(req["addServer"])
            add.append(req["ip_port"])
            add.append("cookie")
            add.append(req["cookie"])
            cols = req["settings"].strip().split()
            for col in cols:
                add.append(col)
            sec.params.append(add)
            config.data.edit = True
    if req["save"] == "yes":
        message += config.save()
        req["addServer"] = "none"

### delete server ####
if req["delServer"] != "none":
    for sec in config.data.sections:
        if sec.name == "backend":
            for i in range(0, len(sec.params)):
                if sec.params[i][0] == "server" and sec.params[i][1] == req["delServer"]:
                    sec.params.pop(i)
                    config.data.edit = True
                    break
    message += config.save()
    req["delServer"] = "none"

### set server list #####
servers = []
for sec in config.data.sections:
    if sec.name == "backend":
        backend_name = sec.attributes[0]
        for p in sec.params:
            if p[0] == "server":
                servers.append(backend_name + "/" + p[1])
                
### get new log #########
httpLog = HaproxyHttpLog()

### get stats ######
st = HaproxyStats()
socket_output = ""
if req["socket_command"]:
    socket_output = st.socketCommand(req["socket_command"])
stats = st.getStats()

### render html #####

### <head>--</head> ####
HtmlHead(loc.str('menu_haproxy'), "", "haproxy.js").render()

print("<body onLoad='setRefreshTimerAndScroll(" + req["refresh"] + "," + req["y_scroll"] + ")'>")

Menu("haproxy", loc).render()

### form (hidden params) #####
params = { 
    'refresh':req["refresh"], 'editServer':'none', 'service_action':'none', 'addServer':'none',
    'delServer':'none', 'weightServer':'none', 'y_scroll':'0', 'socket_command':'', 'save':'no'
}
HtmlForm("form1", "haproxy_ctl.py", "POST", params).render()

print("<div id='header'>")
print("<table style='margin-bottom: 0px;'><tr>")
print("<td style='border: 0;'><h3>"  + loc.str('haproxy_title') + "</h3></td>")
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
if not config.isLoaded():
    print "<td>" + loc.str('need_service_reload_message') + "</td>"
print("</tr></table>")
    
# frontedns
for sec in config.data.sections:
    if sec.name == "frontend":
        stat = stats[sec.attributes[0] + "/FRONTEND"]
        print("<table class='nomargin'><tr><td width=200 class='nobottom'>")
        print("<h3>" + loc.str('frontend') + " : ")
        for a in sec.attributes:
            print(" " + a)
        print("</h3></td><td class='nobottom'>")
        
        # toggle display:
        renderToggleDivStart("frontend_settings", loc.str('settings'), form)
        # contents --
        print("<table class='nomargin'>")
        for p in sec.params:
            print("<tr><th width=150>" + p[0] + "</th>")
            print("<td>")
            for i in range(1,len(p)):
                print(p[i] + " ")
            print("</td></tr>")
        print("</table>")
        print("</div>")
        # -- contents end
        
        print("</td></tr></table>")        
        print("<table>")
        print("<tr><th width=150>" + loc.str('rate_sec') + "(" + loc.str('max') + ")</th>")
        print("<td>" + stat["req_rate"] + " (" + stat["req_rate_max"] + ")</td></tr>")
        print("<tr><th>" + loc.str('sessions') + "(" + loc.str('max') + ")</th>")
        print("<td>" + stat["scur"] + " (" + stat["smax"] + ")</td></tr>")
        print("</table>")

#renderVSpace(10)
# backends
for sec in config.data.sections:
    if sec.name == "backend":
        print("<table class='nomargin'><tr><td width=200 class='nobottom'>")
        print("<h3>" + loc.str('backend') + " : ")
        backend_name = sec.attributes[0]
        frontend_name = ""
        
        stat = stats[backend_name + "/BACKEND"]
        for a in sec.attributes:
            print(" " + a)
        print("</h3></td><td class='nobottom'>")
        
        # toggle display:
        renderToggleDivStart("backend_settings", loc.str('settings'), form)
        # contents --
        print("<table class='nomargin'>")
        for p in sec.params:
            if p[0] == "server":
                continue
            print("<tr><th width=150>" + p[0] + "</th>")
            print("<td>")
            for i in range(1,len(p)):
                print(p[i] + " ")
            print("</td></tr>")
        print("</table>")
        print("</div>")
        # -- contents end
        
        print("</td></tr></table>")
        print("<table>")
        print("<tr><th width=150>" + loc.str('weight') + "(" + loc.str('total') + ")</th>")
        print("<td>" + stat["weight"] + "</td></tr>")
        print("<tr><th>" + loc.str('queue') + "(" + loc.str('max') + ")</th>")
        print("<td>" + stat["qcur"] + " (" + stat["qmax"] +  ")</td></tr>")
        print("</table>")

        # servers
        print("<table class='server'>")
        print("<tr>")
        print("<th>" + loc.str('server') + "</th>")
        print("<th>" + loc.str('ip_port') + "</th>")
        print("<th>" + loc.str('cookie') + "</th>")
        print("<th colspan=2>" + loc.str('config') + "</th>")
        print("<th>" + loc.str('status') + "</th>")
        print("<th colspan=2>" + loc.str('weight') + "</th>")
        print("<th>" + loc.str('rate_sec') + "(" + loc.str('max') + ")</th>")
        print("<th>" + loc.str('sessions') + "(" + loc.str('max') + ")</th>")
        print("<th>" + loc.str('last_access') + "</th>")
        print("</tr>")
        for p in sec.params:
            if p[0] != "server":
                continue
            
            # configs:
            name = p[1]
            ip_port = p[2]
            cookie = "--"
            settings = ""
            for i in range(3,len(p)):
                if p[i] == "cookie" and i+1 < len(p):
                    cookie = p[i+1]
                    continue
                if p[i-1] == "cookie":
                    continue
                if settings:
                    settings += " "
                settings += p[i]
                
            # stats:
            last_timestamp = "--"
            stat = None
            isUp = False
            if stats.has_key(backend_name + "/" + name):
                stat = stats[backend_name + "/" + name]
                if stat["rate"] == "0":
                    last_timestamp = httpLog.getServerLastTimestamp(backend_name + "/" + name)
                    if last_timestamp != "N/A":
                        last_timestamp = httpLog.getHowLong(last_timestamp, timestamp)
                else:
                    last_timestamp = "now"
                if "UP" in stat["status"]:
                    isUp = True

            # server start:
            print("<tr>")
            
            # display configs:
            if name == req["editServer"]:
                if isUp:
                    print("<td><input name='name' size=8 value='" + name + "' disabled /></td>")
                    print("<td><input name='ip_port' value='" + ip_port + "' disabled /></td>")
                    print("<td><input name='cookie' size=8 value='" + cookie + "' disabled /></td>")
                else:
                    print("<td><input name='name' size=8 value='" + name + "'/></td>")
                    print("<td><input name='ip_port' value='" + ip_port + "'/></td>")
                    print("<td><input name='cookie' size=8 value='" + cookie + "'/></td>")
                print("<td><input name='settings' value='" + settings + "'/></td>")
                print("<td class='actions'><a href='javascript:saveServer(" + '"' + req["editServer"] + '"' + ")'>" + loc.str('btn_save') + "</a><a href='javascript:setRefresh(10)'>" + loc.str('btn_cancel') + "</a></td>")
            elif name == req["addServer"]:
                print("<td><input name='name' size=8 value='" + name + "'/></td>")
                print("<td><input name='ip_port' value='" + ip_port + "'/></td>")
                print("<td><input name='cookie' size=8 value='" + cookie + "'/></td>")
                print("<td><input name='settings' value='" + settings + "'/></td>")
                print("<td class='actions'><a href='javascript:saveAddServer()'>" + loc.str('btn_save') + "</a><a href='javascript:setRefresh(10)'>" + loc.str('btn_cancel') + "</a></td>")
            else:
                print("<td>" + name + "</td>")
                print("<td>" + ip_port + "</td>")
                print("<td>" + cookie +"</td>")
                print("<td>" + settings +  "</td>")
                print("<td class='actions'><a href='javascript:editServer(" + '"' + name + '"' + ")'>" + loc.str('btn_edit') + "</a>")
                if isUp:
                    print("<span class='disabled'>" + loc.str('btn_delete') + "</span></td>")
                else:
                    msg = loc.str_name('delete_server_message', name)
                    print("<a href='javascript:deleteServer(" + '"' + name + '", "' + msg + '"' + ")'>" + loc.str('btn_delete') + "</a></td>")
                    
            # display stats:
            if stat:
                if isUp:
                    print("<td class='actions'>" + stat["status"] +  " <a href='javascript:downServer(" + '"' + backend_name + "/" + name + '"' + ")'>down</a></td>")
                else:
                    print("<td class='actions'>" + stat["status"] +  " <a href='javascript:upServer(" + '"' + backend_name + "/" + name + '"' + ")'>up</a></td>")
                if name == req["weightServer"]:
                    print("<td><input type=text name='weightValue' size=3 value=" + stat["weight"] +  " /></td>")
                    print("<td class='actions'><a href='javascript:doEditWeight(" + '"' + backend_name + "/" + name + '"' + ")'>" + loc.str('submit') + "</a></td>")
                    print("</form>")
                else:
                    print("<td>" + stat["weight"] +  "</td>")
                    print("<td class='actions'><a href='javascript:editWeight(" + '"' + name + '"' + ")'>" + loc.str('btn_change') + "</a></td>")
                print("<td>" + stat["rate"] +  " (" + stat["rate_max"] + ")</td>")
                print("<td>" + stat["scur"] + " (" + stat["smax"] + ")</td>")
                print("<td>" + last_timestamp +  "</td>")
            else:
                print("<td>--</td>")
                print("<td>--</td>")
                print("<td>--</td>")
                print("<td>--</td>")
                print("<td>--</td>")

            # server end:
            print("</tr>")
        
        if req['addServer'] == "none":
            print("<tr><td class='actions' colspan=2 style='border:0px; text-align:left;'><a href='javascript:addServer()'>" + loc.str('add_server') + "</a></td><td colspan=7 style='border:0px'>&nbsp;</td></tr>")
        print("</table>")

### socket command ######
# toggle display:
renderToggleDivStart("socket_command", loc.str('send_command'), form)
# contents --
print("<table><tr><td>")
print("<input type='text' name='socket_command_str' value='" + req["socket_command"] + "'/>")
print("</td><td class='actions' style='vertical-align:middle;'>")
print("<a href='javascript:socketCommand()'>" + loc.str('submit') + "</a>")
print("</td></tr><tr><td colspan=2>")
print("<textarea readonly rows=10>" + socket_output + "</textarea>")
print("</td></tr></table>")
print("</div>")
# -- contents end

### stats table ######
# toggle display:
renderToggleDivStart("stats_table", loc.str('stats_detail'), form)
# contents --
print("<table>")
print("<tr>")
print("<td>&nbsp;</td>")
for name in stats.keys():
    print("<th>" + name + "</th>")
print("</tr>")
first = sorted(stats.keys())[0]
for key in sorted(stats[first].keys()):
    print("<tr>")
    print("<th>" + key + "</th>")
    for name in stats.keys():
        print("<td>" + stats[name][key] + "</td>")
    print("</tr>")
print("</table>")
print("</div>")
# -- contents end

print("</div>") #container
print("</div>") #outer

### footer ######
print("<div id='footer'>")
print("webadmin : " + loc.str('haproxy_title'))
print("</div>")

print("</form>")

print("</body>")
print("</html>")