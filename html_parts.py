#!/usr/bin/python
# -*- coding: UTF-8 -*-

def renderHead(title, css, js):
    print("Content-Type: text/html;charset=utf-8\n")
    print("<html>")
    print("<head>")
    print("<title>" + title + " - webadmin</title>")
    # common css
    print("<link rel='STYLESHEET' href='webadmin.css' type='text/css'>")
    # additional css
    if css:
        print("<link rel='STYLESHEET' href='" + css + "' type='text/css'>")
    # common js
    print("<script language='javascript' src='common.js' type='text/javascript'></script>")
    # additional js
    if js:
        print("<script language='javascript' src='" + js + "' type='text/javascript'></script>")
    print("</head>")

class HtmlForm():
    action = None
    method = None
    id = None
    params = {}
    
    def __init__(self, id, action, method, params=None):
        self.id = id
        self.action = action
        self.method = method
        if params:
            self.addParams(params)

    def addParam(self, key, value):
        self.params[key] = value
        
    def addParams(self, params):
        for key, value in params.items():
            self.addParam(key, value)

    def render(self):
        print("<form id='" + self.id + "' action='" + self.action + "' method='" + self.method + "'>")
        for key, value in self.params.items():
            print("<input type='hidden' name='" + key + "' value='" + value + "' />")

# misc utils
def renderVSpace(pixel):
    print("<div style='height:" + str(pixel) + "px;'>&nbsp;</div>")

def renderAutoRefresh(intervals, req, loc):
    for interval in intervals:
        if int(req) == interval:
            print("<span>" + str(interval) + "</span>")
        else:
            print("<a href='javascript:setRefresh(" + str(interval) + ")'>" + str(interval) + "</a>")
    if int(req) == 0:
        print("<span>off</span>")
    else:
        print("<a href='javascript:setRefresh(0)'>off</a>")
    print("<a href='javascript:refresh()'>" + loc.str('refresh') + "</a>")

def renderService(service, loc, message):
    color = "green"
    if service.state != "running":
        color = "red"
    print("<table><tr><th width=150>" + loc.str('service_status') + "</th><td width=150><font color=" + color + ">" + service.state + "</font></td>")
    if service.state == "running":
        print("<td class='actions' style='text-align:left;'><a href='javascript:stop()'>" + loc.str('service_stop') + "</a><a href='javascript:reload()'>" + loc.str('service_reload') + "</a></td>")
    elif service.state == "stopped":
        print("<td class='actions' style='text-align:left;'><a href='javascript:start()'>" + loc.str('service_start') + "</a></td>")
    else:
        print("<td>" + loc.str('no_service_message') + "</td>")    
    if message:
        print "<td>" + message + "</td>"
    print("</tr></table>")

def renderToggleDivStart(name, label, form, default="close"):
    openfunc = 'javascript:toggleDisplay("' + name + '", "open")'
    closefunc = 'javascript:toggleDisplay("' + name + '", "close")'
    state = default
    if form.has_key(name + '_div'):
       state =  form[name + '_div'].value
    if state == "open":
        print("<div id='" + name + "_close' style='display:none;'><table class='toggle'><tr><td class='triangle'><div class='detail_button'><a href='" + openfunc + "'></a></div></td><td><a href='" + openfunc + "'>" + label + "</a></td></tr></table></div>")
        print("<div id='" + name + "_open'><table class='toggle'><tr><td class='triangle'><div class='detail_button_close'><a href='" + closefunc + "'></a></div></td><td><a href='" + closefunc + "'>" + label + "</a></td></tr></table>")
        print("<input type='hidden' name='" + name + "_div' value='open' />")
    else:
        print("<div id='" + name + "_close'><table class='toggle'><tr><td class='triangle'><div class='detail_button'><a href='" + openfunc + "'></a></div></td><td><a href='" + openfunc + "'>" + label + "</a></td></tr></table></div>")
        print("<div id='" + name + "_open' style='display:none;'><table class='toggle'><tr><td class='triangle'><div class='detail_button_close'><a href='" + closefunc + "'></a></div></td><td><a href='" + closefunc + "'>" + label + "</a></td></tr></table>")
        print("<input type='hidden' name='" + name + "_div' value='close' />")
        