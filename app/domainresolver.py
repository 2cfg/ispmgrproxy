#!/usr/bin/env python3
import socket
import app.config as config


class DomainResolver(object):
    def __init__(self, records):
        self.records = records


    def _resolve(self, record):
        try:
            data = socket.gethostbyname(record)
            ip = str(data)
            return ip
        except Exception as e:
            print(str(e))
            return False

    
    def resolve_all(self):
        result = True
        if not self.records:
            return False

        for record in self.records:
            if '*' in str(record):
                continue

            data = self._resolve(str(record))

            for addr in config.lb_ipaddr_list:
                result = result and (str(data) == addr)

        return result