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

import sys
sys.path.append('iptables/')
from iptables_stats import IptablesStats
from ssh import Ssh

## main

message = ""

## request params #########
form = cgi.FieldStorage()
req = {
    'refresh':"0", 'service_action':"none" ,'y_scroll':"0", 'lang':"en", 'tab_id' : "-99", 'host':"localhost", 'command':"",
    'rule_id':"", 'target':"", 'prot':"", 'opt':"", 'ifin':"", 'ifout':"", 'source':"", 'sport':"", 'destination':"", 'dport':"", 'misc':"", 'state':""
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

if service.state == "running":
    ### modify rules ###
    if req['command']:
        ssh = Ssh(req['host'])
        if req['command'] == "replace":
            com = "iptables -R FORWARD " + req['rule_id'] + " -j " + req['target']
        if req['command'] == "insert":
            com = "iptables -I FORWARD " + req['rule_id'] + " -j " + req['target']
        if req['command'] == "add":
            com = "iptables -A FORWARD " + " -j " + req['target']
           
        if req['command'] == "delete":
            com = "iptables -D FORWARD " + req['rule_id']
        else:
            # protocol
            if req['prot'] != "" and req['prot'] != "all":
                com += " -p " + req['prot']
            # input interface
            if req['ifin'] != "" and req['ifin'] != "*":
                com += " -i " + req['ifin']
            # source
            if req['source'] != "" and req['source'] != "0.0.0.0/0":
                com += " -s " + req['source']
            # output interface
            if req['ifout'] != "" and req['ifout'] != "*":
                com += " -o " + req['ifout']
            # destination
            if req['destination'] != "" and req['destination'] != "0.0.0.0/0":
                com += " -d " + req['destination']
            # sport
            if req['sport'] != "":
                com += " --sport " + req['sport']
            # dport
            if req['dport'] != "":
                com += " --dport " + req['dport']
            # state
            if req['state'] != "":
                com += " -m state --state " + req['state']
            
        # do command
        (ret, msg) = ssh.commandAsRoot(com)
        if ret != 0:
            message += "iptables : " + msg
        else:
            # redirect GET:
            print ("Location: iptables_ctl.py?lang=" + req['lang'] + "&host=" + req['host'] + "&tab_id=" + req['tab_id'] + "\n\n")
            exit(0)
        
### render html #####

### <html><head>--</head> ####
renderHead(loc.str('menu_iptables'), "", "iptables/iptables.js")

print("<body onLoad='setRefreshTimerAndScroll(" + req["refresh"] + "," + req["y_scroll"] + ")'>")

Menu(req['tab_id'], loc).render()

### form (hidden params) #####
params = {
    'refresh':req["refresh"], 'y_scroll':'0', 'tab_id': req['tab_id'], 'service_action': 'none', 'host': req['host'], 'command': req['command'],
    'rule_id':req['rule_id'], 'target':req['target'], 'prot':req['prot'], 'opt':req['opt'], 'ifin':req['ifin'], 'ifout':req['ifout'], 'source':req['source'], 
    'sport':req['sport'], 'destination':req['destination'], 'dport':req['dport'], 'misc':req['misc'], 'state':req['state']
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

if service.state == "running":
    
    stats = IptablesStats(req['host'], service.getMessage())
    #print(stats.getMessage() + "<br>")

    # interfaces:
    print("Interfaces")
    print("<table>")
    for iface in stats.interfaces:
        print("<tr><td>" + iface.name + "</td><td>" + iface.subnet + "/" + str(iface.mask) + "</td><tr>")
        print("<script language='javascript'>addInterface('" + iface.name + "');</script>")
    print("</table>")

    # rules (FORWARD):
    print("FORWARD chain : policy " + stats.forward_chain.policy)
    print("<table>")

    print("<tr>")
    print("<th>#</th>")
    print("<th>target</th>")
    print("<th>prot</th>")
    print("<th>opt.</th>")
    print("<th>IF in</th>")
    print("<th>IF out</th>")
    print("<th>src</th>")
    print("<th>dest</th>")
    print("<th>conditions</th>")
    print("<th>&nbsp;</th>")
    print("</tr>")

    for rule in stats.forward_chain.rules:
        print("<tr><td>" + rule.num + "</td>")
        #print("<td>" + str(rule.pkts) + "</td>")
        #print("<td>" + str(rule.bytes) + "</td>")
        print("<td>" + rule.target + "</td>")
        print("<td>" + rule.prot + "</td>")
        print("<td>" + rule.opt + "</td>")
        print("<td>" + rule.ifin + "</td>")
        print("<td>" + rule.ifout + "</td>")
        print("<td>" + rule.source + "</td>")
        print("<td>" + rule.destination + "</td>")
        if rule.misc:
            print("<td>" + rule.misc + "</td>")
        else:
            print("<td>&nbsp;</td>")
        # ruleOperation(rule_id, target, prot, ifin, ifout, source, destination, misc)
        d = '", "'
        params = ', "' + rule.target + d + rule.prot + d + rule.opt + d + rule.ifin + d + rule.ifout + '"'
        params += ', "' + rule.source + d + rule.sport + d + rule.destination + d + rule.dport + d +rule.misc + d + rule.state + '"'
        print("<td><div class='opr_button'><a href='javascript:ruleOperation(" + rule.num + params + ")'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div></td>")
        print("</tr>")

    print("<tr><td colspan=9>&nbsp;</td>")
    print("<td><div class='plus_button'><a href='javascript:ruleAdd(" + str(len(stats.forward_chain.rules)) + ")'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div></td>")
    print("</tr>")
    print("</table>")

    for tablename, table in stats.tables.items():
        renderVSpace(10)
        toggleDefault = "close"
        #if tablename == "filter":
        #    toggleDefault = "open"
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