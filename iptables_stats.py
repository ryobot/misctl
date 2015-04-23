#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ssh import Ssh

class iptables_rule(object):
    num = ""
    pkts = 0
    bytes = 0
    target = ""
    prot = ""
    opt = ""
    ifin = ""
    ifout = ""
    source = ""
    destination = ""
    misc = ""
    dport = ""
    sport = ""
    state = ""

class iptables_chain(object):
    policy = ""
    rules = []
    
class iptables_table(object):
    chains = {}
    
class interface(object):
    name = ""
    hwaddr = ""
    subnet = ""
    mask = ""

### class Stats ###############
class IptablesStats():
    tables = {}
    ssh = None
    forward_chain = None
    interfaces = []

    def __init__(self, host, stat_str):
        self.ssh = Ssh(host)
        self.tables = self.getTables(stat_str)
        self.getInterfaces()
        self.forward_chain = self.getChain("FORWARD")

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

    def octet2int(self, ip):
        intIp = []
        for oct in ip.split('.'):
            intIp.append(int(oct))
        return intIp

    def mask2Bits(self, mask):
        intMask = self.octet2int(mask)
        bits = 0
        for i in range(0, len(intMask)):
            binary = bin(intMask[i])
            bits += len(binary.strip('0b'))
        return bits
    
    def bits2Mask(self, bits):
        b = bits
        mask = ""
        for i in range(0, 4):
            if b >= 8:
                val = 255
            else:
                x = 128
                val = 0
                for j in range(0, b):
                    val += x
                    x /= 2
            mask += str(val)
            if i < 3:
                mask += "."
            b -= 8
        return mask
    
    def getInterfaces(self):
        com = "route"
        self.interfaces = []
        (ret, content) = self.ssh.commandAsRoot(com)
        if ret == 0:
            lines = content.splitlines()
            for line in lines:
                columns = line.split()
                if columns[0] in ['Kernel', 'Destination', 'link-local', 'default']:
                    continue
                if len(columns) == 8 and columns[1] == "*":
                    iface = interface()
                    iface.subnet = columns[0]
                    iface.mask = self.mask2Bits(columns[2])
                    iface.name = columns[7]
                    self.interfaces.append(iface)

    def getChain(self, chain):
        com = "iptables -vnx --line-numbers -L " + chain
        chain = iptables_chain()
        (ret, content) = self.ssh.commandAsRoot(com)
        if ret == 0:
            lines = content.splitlines()
            for line in lines:
                columns = line.strip().split()
                if len(columns) == 0:
                    continue
                # label
                if columns[0] == "num":
                    continue
                if columns[0] == "Chain":
                    chain.policy = columns[3].strip("()")
                    chain.rules = []
                    continue
                # the line must be a rule:
                if len(columns) >= 6:
                    rule = iptables_rule()
                    rule.num = columns[0]
                    rule.pkts = columns[1]
                    rule.bytes = columns[2]
                    rule.target = columns[3]
                    rule.prot = columns[4]
                    rule.opt = columns[5]
                    rule.ifin = columns[6]
                    rule.ifout = columns[7]
                    rule.source = columns[8]
                    rule.destination = columns[9]
                    if len(columns) >= 11:
                        for i in range(10, len(columns)):
                            if rule.misc:
                                rule.misc += " "
                            rule.misc += columns[i]
                            miscItem = columns[i].split(":")
                            if len(miscItem) == 2:
                                if miscItem[0] == "dpt":
                                    rule.dport = miscItem[1]
                                if miscItem[0] == "spt":
                                    rule.sport = miscItem[1]
                            if i > 10 and columns[i-1] == "state":
                                rule.state = columns[i]
                    chain.rules.append(rule)
        return chain
        