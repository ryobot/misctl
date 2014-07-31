#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
from ssh import Ssh

### log models #############
class http_server_data(object):
    timestamp_last = "N/A"
    server = "server"
    conn_cnt = "0"
    retry_cnt = "0"
    last_conn_str = None
    acc_cnt = 0
    acc_per_sec = 0.0

class http_data(object):
    timestamp_first = "N/A"
    timestamp_last = "N/A"
    fe_conn_cnt = "0"
    be_conn_cnt = "0"
    acc_cnt = 0
    acc_per_sec = 0.0
    duration_millisec = 0
    server_data = {}

### class HttpLog ###############
class HaproxyHttpLog():
    log_path = "/var/log/haproxy.log"
    ssh = Ssh()

    def getLogLineCount(self):
        com = "wc -l " + self.log_path
        (ret,content) = self.ssh.command(com)
        count = 0
        if ret == 0 and content:
            count = int(content.splitlines()[0].strip().split()[0])
        return count

    def getMilisec(self,timestr):
        cols = timestr.split(':')
        sec = 0
        if len(cols) > 3:
            sec += int(cols[1])*60*60*1000
            sec += int(cols[2])*60*1000
            sec += int(cols[3].split('.')[0])*1000
            sec += int(cols[3].split('.')[1])
        return sec

    def getDuration(self, first, last):
        if first == last:
            return 0
        msec = self.getMilisec(last) - self.getMilisec(first)
        return msec
    
    def getHowLong(self, to, fm):
        msec = self.getDuration(to, fm)
        sec = msec/1000
        if sec < 60:
            return str(sec) + " sec. ago"
        min = sec/60
        if min < 60:
            return str(min) + " min. ago"
        hour = min/60
        return str(hour) + " hr ago"

    def getServerLastTimestamp(self, server):
        com = "grep " + server + " " + self.log_path + " | grep HTTP | tail -1"
        (ret,content) = self.ssh.command(com)
        timestamp = "N/A"
        if ret == 0 and content:
            columns = content.splitlines()[0].strip().split()
            if len(columns) > 6:
                timestamp = columns[6].strip("[]")
        return timestamp

    def getLog(self, startLogLine, servers):
        totalLines = self.getLogLineCount()
        if totalLines - int(startLogLine) > 10000:
            startLogLine = str(totalLines - 10000)
        if int(startLogLine) > 0:
            startLogLine = str(int(startLogLine) - 1)

        data = http_data()
        for s in servers:
            data.server_data[s] = http_server_data()
        com = "tail -n +" + startLogLine + " " + self.log_path
        (ret,content) = self.ssh.command(com)
        endLogLine = startLogLine
        if ret == 0 and content:
            lines = content.splitlines()
            last_conn_str = None

            # counting
            for line in lines:
                cols = line.strip().split()
                if len(cols) > 6 and data.timestamp_first == "N/A":
                    data.timestamp_first = cols[6].strip("[]")
                    continue
                data.acc_cnt += 1
                if len(cols) > 6:
                    data.timestamp_last = cols[6].strip("[]")
                if len(cols) > 8 and data.server_data.has_key(cols[8]):
                    data.server_data[cols[8]].acc_cnt += 1
                    data.server_data[cols[8]].timestamp_last = cols[6].strip("[]")
                    if len(cols) > 15:
                        data.server_data[cols[8]].last_conn_str = cols[15]
                if len(cols) > 15:
                    last_conn_str = cols[15]

            if data.timestamp_last == "N/A":
                now = datetime.datetime.now()
                data.timestamp_last = now.strftime("%d/%b/%Y:%H:%M:%S") + ".%03d" % (now.microsecond / 1000)

            # durations and throughput
            data.duration_millisec = self.getMilisec(data.timestamp_last) - self.getMilisec(data.timestamp_first)
            if data.duration_millisec > 0:
                data.acc_per_sec = float(data.acc_cnt) / float(data.duration_millisec) * 1000

            # last conn state
            if last_conn_str:
                conn = last_conn_str.split("/")
                if len(conn) > 1:
                    data.fe_conn_cnt = conn[1]
                if len(conn) > 2:
                    data.be_conn_cnt = conn[2]

            # per server data
            for s in servers:
                if data.duration_millisec > 0:
                    data.server_data[s].acc_per_sec = float(data.server_data[s].acc_cnt) / float(data.duration_millisec) * 1000
                if data.server_data[s].last_conn_str:
                    conn = data.server_data[s].last_conn_str.split("/")
                    if len(conn) > 3:
                        data.server_data[s].conn_cnt = conn[3]
                    if len(conn) > 4:
                        data.server_data[s].retry_cnt = conn[4]
                if data.server_data[s].timestamp_last == "N/A":
                    data.server_data[s].timestamp_last = self.getServerLastTimestamp(s)

            # update current log line
            endLogLine = int(startLogLine) + len(lines)

        return (str(endLogLine), data)

    def getLastLog(self):
        com = "tail -1 " + self.log_path
        (ret,content) = self.ssh.command(com)
        data = http_data()
        if ret == 0 and content:
            columns = content.splitlines()[0].strip().split()
            if len(columns) > 6:
                data.timestamp = columns[6].strip("[]")
            if len(columns) > 15:
                conn = columns[15].split("/")
                if len(conn) > 1:
                    data.fe_conn_cnt = conn[1]
                if len(conn) > 2:
                    data.be_conn_cnt = conn[2]
        return data
