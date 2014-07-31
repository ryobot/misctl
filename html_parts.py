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
        print("<title>" + self.title + "</title>")
        if self.css:
            print("<link rel='STYLESHEET' href='" + self.css + "' type='text/css'>")
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
        