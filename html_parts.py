#!/usr/bin/python
# -*- coding: UTF-8 -*-

class HtmlHead():
    title = None
    css = None
    js = None
    
    def __init__(self, title, css, js):
        self.title = title
        self.css = css
        self.js = js
    
    def render(self):
        print("Content-Type: text/html;charset=utf-8\n")
        print("<html>")
        print("<head>")
        print("<title>" + self.title + " - webadmin</title>")
        print("<link rel='STYLESHEET' href='webadmin.css' type='text/css'>")
        if self.css:
            print("<link rel='STYLESHEET' href='" + self.css + "' type='text/css'>")
        print("<script language='javascript' src='common.js' type='text/javascript'></script>")
        if self.js:
            print("<script language='javascript' src='" + self.js + "' type='text/javascript'></script>")
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

def renderToggleDivStart(name, label, form):
    openfunc = 'javascript:toggleDisplay("' + name + '", "open")'
    closefunc = 'javascript:toggleDisplay("' + name + '", "close")'
    if form.has_key(name + '_div') and form[name + '_div'].value == "open":
        print("<div id='" + name + "_close' style='display:none;'><table class='toggle'><tr><td class='triangle'><div class='detail_button'><a href='" + openfunc + "'></a></div></td><td><a href='" + openfunc + "'>" + label + "</a></td></tr></table></div>")
        print("<div id='" + name + "_open'><table class='toggle'><tr><td class='triangle'><div class='detail_button_close'><a href='" + closefunc + "'></a></div></td><td><a href='" + closefunc + "'>" + label + "</a></td></tr></table>")
        print("<input type='hidden' name='" + name + "_div' value='open' />")
    else:
        print("<div id='" + name + "_close'><table class='toggle'><tr><td class='triangle'><div class='detail_button'><a href='" + openfunc + "'></a></div></td><td><a href='" + openfunc + "'>" + label + "</a></td></tr></table></div>")
        print("<div id='" + name + "_open' style='display:none;'><table class='toggle'><tr><td class='triangle'><div class='detail_button_close'><a href='" + closefunc + "'></a></div></td><td><a href='" + closefunc + "'>" + label + "</a></td></tr></table>")
        print("<input type='hidden' name='" + name + "_div' value='close' />")
        