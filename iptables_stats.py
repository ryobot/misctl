#!/usr/bin/python
# -*- coding: UTF-8 -*-

class iptables_rule(object):
    num = ""
    target = ""
    prot = ""
    opt = ""
    source = ""
    destination = ""
    misc = ""

class iptables_chain(object):
    policy = ""
    rules = []
    
class iptables_table(object):
    chains = {}

### class Stats ###############
class IptablesStats():
    tables = {}

    def __init__(self,stat_str):
        self.tables = self.getTables(stat_str)

    def isTableHeader(self,key):
        if key == "table:" or key == "Table:" or key == "テーブル:":
            return True
        return False
    
    def getTables(self,stat_str):
        lines = stat_str.splitlines()
        tables = {}
        tablename = ""
        chainname = ""
        for line in lines:
            columns = line.strip().split()
            if len(columns) == 0:
                continue
            # label
            if columns[0] == "num":
                continue
            if self.isTableHeader(columns[0]):
                tablename = columns[1]
                tables[tablename] = iptables_table()
                tables[tablename].chains = {}
                continue
            if columns[0] == "Chain":
                chainname = columns[1]
                tables[tablename].chains[chainname] = iptables_chain()
                tables[tablename].chains[chainname].policy = columns[3].strip("()")
                tables[tablename].chains[chainname].rules = []
                continue
            # the line must be a rule:
            if len(columns) >= 6:
                rule = iptables_rule()
                rule.num = columns[0]
                rule.target = columns[1]
                rule.prot = columns[2]
                rule.opt = columns[3]
                rule.source = columns[4]
                rule.destination = columns[5]
                if len(columns) >= 7:
                    for i in range(6, len(columns)):
                        if rule.misc:
                            rule.misc += " "
                        rule.misc += columns[i]
                tables[tablename].chains[chainname].rules.append(rule)
        return tables

