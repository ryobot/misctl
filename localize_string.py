#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import codecs

languages = {
    'en': 'English',
    'ja': '日本語'
}

class Localize():
    localize_strs = None
    language = None
    message = None
    
    def __init__(self, lang):
        self.language = lang;
        f = codecs.open("localize.json", "r", "utf-8")
        if f:
            self.localize_strs = json.load(f)
            f.close()
        else:
            self.message = "cannot open localize json file"
    
    def str(self, key):
        if self.localize_strs and self.localize_strs.has_key(key):
            return self.localize_strs[key][self.language].encode('utf-8')
        return '[Undefined String]'
    
    def str_name(self, key, name, host=""):
        if self.localize_strs and self.localize_strs.has_key(key):
            ret_str = self.localize_strs[key][self.language].encode('utf-8').replace('NAME', name)
            if host:
                ret_str = ret_str.replace('HOST', host)
            return ret_str
        return '[Undefined String]'
    
    def renderOptions(self):
        for key, value in languages.items():
            selected = ""
            if self.language == key:
                selected = " selected"
            print("<option value='" + key + "'" + selected + ">" + value + "</option>")

        