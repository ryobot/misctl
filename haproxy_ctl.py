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

### form params ###
settingList = ["check", "disabled", "backup"]
                        
def printSelectSettings(selectedValue):
    for s in settingList:
        print("<option value='" + s + "'")
        if s == selectedValue:
            print(" selected")
        print(">" + s + "</option>")

## main
message = ""

## request params #########
form = cgi.FieldStorage()
req_refresh = "10"
req_editServer = "none"
req_save = False
req_service_action = "none"
req_addServer = "none"
req_delServer = "none"
req_weightServer = "none"
req_name = "new_server"
req_ip_port = "0.0.0.0:80"
req_cookie = "new_server"
req_settings = "check weight 10"
req_y_scroll = "0"
req_detail = "no"
req_command = "no"
req_socket_command = ""
if form.has_key("refresh"):
    req_refresh = form["refresh"].value
if form.has_key("editServer"):
    req_editServer = form["editServer"].value
if form.has_key("addServer"):
    req_addServer = form["addServer"].value
if form.has_key("delServer"):
    req_delServer = form["delServer"].value
if form.has_key("weightServer"):
    req_weightServer = form["weightServer"].value
if form.has_key("service_action"):
    req_service_action = form["service_action"].value
if form.has_key("name"):
    req_name = form["name"].value
if form.has_key("ip_port"):
    req_ip_port = form["ip_port"].value
if form.has_key("cookie"):
    req_cookie = form["cookie"].value
if form.has_key("settings"):
    req_settings = form["settings"].value
if form.has_key("y_scroll"):
    req_y_scroll = form["y_scroll"].value
if form.has_key("detail"):
    req_detail = form["detail"].value
if form.has_key("command"):
    req_command = form["command"].value
if form.has_key("socket_command"):
    req_socket_command = form["socket_command"].value
if form.has_key("save") and form["save"].value == "yes":
    req_save = True

### get config / service ####
config = HaproxyConfig()
service = Service("haproxy")
if req_service_action == "stop":
    message += service.stop()
if req_service_action == "start":
    message += service.start()
    config.setLoaded(True)
    req_refresh = "10"
if req_service_action == "reload":
    message += service.reload()
    config.setLoaded(True)
    req_refresh = "10"

### edit server ###
if req_editServer != "none" and req_save:
    for sec in config.data.sections:
        if sec.name == "backend":
            for p in sec.params:
                if p[0] == "server" and p[1] == req_editServer:
                    p[1] = req_name
                    p[2] = req_ip_port
                    pos = 3
                    for i in range(3,len(p)):
                        if pos >= len(p):
                            break
                        if p[pos] != "cookie" and p[pos-1] != "cookie":
                            p.pop(pos)
                        else:
                            if p[pos-1] == "cookie":
                                p[pos] = req_cookie
                            pos += 1
                    cols = req_settings.strip().split()
                    for col in cols:
                        p.append(col)
                    config.data.edit = True
    message += config.save()
    req_editServer = "none"

### add server ####
if req_addServer != "none":
    for sec in config.data.sections:
        if sec.name == "backend":
            add = []
            add.append("server")
            add.append(req_addServer)
            add.append(req_ip_port)
            add.append("cookie")
            add.append(req_cookie)
            cols = req_settings.strip().split()
            for col in cols:
                add.append(col)
            sec.params.append(add)
            config.data.edit = True
    if req_save:
        message += config.save()
        req_addServer = "none"

### delete server ####
if req_delServer != "none":
    for sec in config.data.sections:
        if sec.name == "backend":
            for i in range(0, len(sec.params)):
                if sec.params[i][0] == "server" and sec.params[i][1] == req_delServer:
                    sec.params.pop(i)
                    config.data.edit = True
                    break
    message += config.save()
    req_delServer = "none"

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
if req_socket_command:
    socket_output = st.socketCommand(req_socket_command)
stats = st.getStats()

print("Content-Type: text/html;charset=utf-8\n")
print("<html>")
print("<head>")
print("<title>haproxy control</title><link rel='STYLESHEET' href='webadmin.css' type='text/css'>")
print("<script language='javascript' src='haproxy.js' type='text/javascript'></script>")
print("</head>")
print("<body onLoad='setRefreshTimerAndScroll(" + req_refresh + "," + req_y_scroll + ")'>")

### param form ######
print("<form id='form1' action='haproxy_ctl.py' method='POST'>")
print("<input type='hidden' name='refresh' value='" + req_refresh + "' />")
print("<input type='hidden' name='editServer' value='none' />")
print("<input type='hidden' name='service_action' value='none' />")
print("<input type='hidden' name='addServer' value='none' />")
print("<input type='hidden' name='delServer' value='none' />")
print("<input type='hidden' name='weightServer' value='none' />")
print("<input type='hidden' name='y_scroll' value=0 />")
print("<input type='hidden' name='socket_command' value='' />")
print("<input type='hidden' name='detail' value='" + req_detail + "' />")
print("<input type='hidden' name='command' value='" + req_command + "' />")
print("</form>")

print("<div id='header'>")
print("<table><tr>")
print("<td><h2>haproxy コントロール・パネル</h2></td>")
print("<td><div id='refresh'>refresh : </td>")
print("<td class='actions' style='text-align:left; margin-top:20px;'>")
print("<div style='height:7px'>&nbsp;</div>")
if int(req_refresh) == 5:
    print("<span>5</span>")
else:
    print("<a href='javascript:setRefresh(5)'>5</a>")
if int(req_refresh) == 10:
    print("<span>10</span>")
else:
    print("<a href='javascript:setRefresh(10)'>10</a>")
if int(req_refresh) == 30:
    print("<span>30</span>")
else:
    print("<a href='javascript:setRefresh(30)'>30</a>")
if int(req_refresh) == 0:
    print("<span>off</span>")
else:
    print("<a href='javascript:setRefresh(0)'>off</a>")
print("<a href='javascript:refresh()'>refresh</a>")
print("</td>")

# time stamp
now = datetime.datetime.now()
timestamp = now.strftime("%d/%b/%Y:%H:%M:%S") + ".%03d" % (now.microsecond / 1000)
print("<td>last update:<br>" + timestamp + "</td>")

print("</tr></table>")
print("</div>")

# service
print("<div id='container'>")
if message:
    print message
print("<table><tr><th width=150>status</th><td width=150>" + service.state + "</td>")
if service.state == "running":
    print("<td class='actions' style='text-align:left;'><a href='javascript:stop()'>stop</a><a href='javascript:reload()'>reload</a></td>")
elif service.state == "stopped":
    print("<td class='actions' style='text-align:left;'><a href='javascript:start()'>start</a></td>")
else:
    print("<td>Check haproxy configuration and installation.</td>")    
if not config.isLoaded():
    print "<td>Configuration has been edited. Please reload to activate current configurations.</td>"
print("</tr></table>")
    
# frontedns
for sec in config.data.sections:
    if sec.name == "frontend":
        stat = stats[sec.attributes[0] + "/FRONTEND"]
        print("<h3>frontend : ")
        for a in sec.attributes:
            print(" " + a)
        print("</h3>")
        print("<table>")
        for p in sec.params:
            print("<tr><th width=150>" + p[0] + "</th>")
            print("<td>")
            for i in range(1,len(p)):
                print(p[i] + " ")
            print("</td></tr>")
        print("<tr><th>rate/sec.(max)</th>")
        print("<td>" + stat["req_rate"] + " (" + stat["req_rate_max"] + ")</td></tr>")
        print("<tr><th>sessions(max)</th>")
        print("<td>" + stat["scur"] + " (" + stat["smax"] + ")</td></tr>")
        print("</table>")
print("</div>")

# backends
print("<div id='container'>")
for sec in config.data.sections:
    if sec.name == "backend":
        print("<h3>backend : ")
        backend_name = sec.attributes[0]
        frontend_name = ""
        
        stat = stats[backend_name + "/BACKEND"]
        for a in sec.attributes:
            print(" " + a)
        print("</h3>")
        print("<table>")
        # params
        for p in sec.params:
            if p[0] == "server":
                continue
            print("<tr><th width=150>" + p[0] + "</th>")
            print("<td>")
            for i in range(1,len(p)):
                print(p[i] + " ")
            print("</td></tr>")
        print("<tr><th>weight(total)</th>")
        print("<td>" + stat["weight"] + "</td></tr>")
        print("<tr><th>queue(max)</th>")
        print("<td>" + stat["qcur"] + " (" + stat["qmax"] +  ")</td></tr>")
        print("</table>")

        # servers
        print("<table class='server'>")
        print("<tr>")
        print("<th>server</th>")
        print("<th>ip:port</th>")
        print("<th>cookie</th>")
        print("<th colspan=2>settings</th>")
        print("<th>status</th>")
        print("<th colspan=2>weight</th>")
        print("<th>rate/sec.(max)</th>")
        print("<th>sessions(max)</th>")
        print("<th>last access</th>")
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
            if name == req_editServer:
                print("<form id='form2' action='haproxy_ctl.py' method='POST'>")
                print("<input type='hidden' name='save' value='yes' />")
                print("<input type='hidden' name='refresh' value='10' />")
                print("<input type='hidden' name='editServer' value='" + req_editServer + "' />")
                if isUp:
                    print("<td><input name='name' size=8 value='" + name + "' disabled /></td>")
                    print("<td><input name='ip_port' value='" + ip_port + "' disabled /></td>")
                    print("<td><input name='cookie' size=8 value='" + cookie + "' disabled /></td>")
                else:
                    print("<td><input name='name' size=8 value='" + name + "'/></td>")
                    print("<td><input name='ip_port' value='" + ip_port + "'/></td>")
                    print("<td><input name='cookie' size=8 value='" + cookie + "'/></td>")
                print("<td><input name='settings' value='" + settings + "'/></td>")
                print("<td class='actions'><a href='javascript:saveServer()'>save</a><a href='javascript:setRefresh(10)'>cancel</a></td>")
                print("</form>")
            elif name == req_addServer:
                print("<form id='form2' action='haproxy_ctl.py' method='POST'>")
                print("<input type='hidden' name='save' value='yes' />")
                print("<input type='hidden' name='refresh' value='10' />")
                print("<td><input name='addServer' size=8 value='" + name + "'/></td>")
                print("<td><input name='ip_port' value='" + ip_port + "'/></td>")
                print("<td><input name='cookie' size=8 value='" + cookie + "'/></td>")
                print("<td><input name='settings' value='" + settings + "'/></td>")
                print("<td class='actions'><a href='javascript:saveServer()'>save</a><a href='javascript:setRefresh(10)'>cancel</a></td>")
                print("</form>")
            else:
                print("<td>" + name + "</td>")
                print("<td>" + ip_port + "</td>")
                print("<td>" + cookie +"</td>")
                print("<td>" + settings +  "</td>")
                print("<td class='actions'><a href='javascript:editServer(" + '"' + name + '"' + ")'>config</a>")
                if isUp:
                    print("<span class='disabled'>delete</span></td>")
                else:
                    print("<a href='javascript:deleteServer(" + '"' + name + '"' + ")'>delete</a></td>")
                    
            # display stats:
            if stat:
                if isUp:
                    print("<td class='actions'>" + stat["status"] +  " <a href='javascript:downServer(" + '"' + backend_name + "/" + name + '"' + ")'>down</a></td>")
                else:
                    print("<td class='actions'>" + stat["status"] +  " <a href='javascript:upServer(" + '"' + backend_name + "/" + name + '"' + ")'>up</a></td>")
                if name == req_weightServer:
                    print("<form id='form2' action='haproxy_ctl.py' method='POST'>")
                    print("<input type='hidden' name='refresh' value='10' />")
                    print("<input type='hidden' name='socket_command' value='' />")
                    print("<td><input type=text name='weightValue' size=3 value=" + stat["weight"] +  " /></td>")
                    print("<td class='actions'><a href='javascript:doEditWeight(" + '"' + backend_name + "/" + name + '"' + ")'>submit</a></td>")
                    print("</form>")
                else:
                    print("<td>" + stat["weight"] +  "</td>")
                    print("<td class='actions'><a href='javascript:editWeight(" + '"' + name + '"' + ")'>set</a></td>")
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

        print("<tr><td class='actions' colspan=2 style='border:0px; text-align:left;'><a href='javascript:addServer()'>add server</a></td><td colspan=7 style='border:0px'>&nbsp;</td></tr>")
        print("</table>")

### socket command ######
if req_command == "no":
    print("<table><tr><td style='text-align:right; width:20px;'><div class='detail_button'><a href='javascript:toggleCommand()'></a></div></td><td>socket command</td></tr></table>")
else:
    print("<table><tr><td style='text-align:right; width:20px;'><div class='detail_button_close'><a href='javascript:toggleCommand()'></a></div></td><td>socket command</td></tr></table>")
    print("<table><tr><td>")
    print("<form id='form3' action='haproxy_ctl.py' method='POST'>")
    print("<input type='hidden' name='refresh' value='0' />")
    print("<input type='hidden' name='y_scroll' value=0 />")
    print("<input type='hidden' name='command' value='yes' />")
    print("<input type='text' name='socket_command' value='" + req_socket_command + "'/>")
    print("</td><td class='actions' style='vertical-align:middle;'>")
    print("<a href='javascript:socketCommand()'>submit</a>")
    print("</td></tr><tr><td colspan=2>")
    print("<textarea readonly rows=10>" + socket_output + "</textarea>")
    print("</form>")
    print("</td></tr></table>")

### stats table ######
if req_detail == "no":
    print("<table><tr><td style='text-align:right; width:20px;'><div class='detail_button'><a href='javascript:toggleDetail()'></a></div></td><td>stats detail</td></tr></table>")
else:
    print("<table><tr><td style='text-align:right; width:20px;'><div class='detail_button_close'><a href='javascript:toggleDetail()'></a></div></td><td>stats detail</td></tr></table>")
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

print("<div id='footer'>")
print("haproxy_ctl : HA Proxy Control Panel")
print("</div>")

print("</body>")
print("</html>")