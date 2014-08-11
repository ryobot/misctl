#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import codecs

class Localize():
    localize_strs = None
    language = None
    message = None
    
    def __init__(self, lang):
        self.language = lang;
        f = codecs.open("localize_" + self.language + ".json", "r", "utf-8")
        if f:
            self.localize_strs = json.load(f)
            f.close()
        else:
            self.message = "cannot open localize json file"
    
    def str(self, key):
        if self.localize_strs and self.localize_strs.has_key(key):
            return self.localize_strs[key].encode('utf-8')
        return '[Undefined String]'
        