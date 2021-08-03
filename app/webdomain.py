#!/usr/bin/env python3
import json

class WebDomain(object):

    def __init__(self, id, ip_addr, name_idn, updated_at, secure, ssl_cert, owner, redirect_http, active=True):

        self.id = id
        self.ip_addr = ip_addr
        self.name_idn = name_idn
        self.active = active
        self.secure = secure
        self.ssl_cert = ssl_cert
        self.owner = owner
        self.redirect_http = redirect_http
        self.records = []
        self.updated_at = updated_at

    def get_ansible_extra_vars(self):

        active_chunk = "active" if self.active == 'on' else "suspended"
        if self.secure == 'on':
            ssl_chunk = "_ssl" 
            redirect_chunk = "_redirect" if self.redirect_http == 'on' else ""
        else:
            ssl_chunk = ""
            redirect_chunk = ""
        
        template_chunk = "{}{}{}".format(active_chunk, ssl_chunk, redirect_chunk)
        server_template = "server_{}_template.conf.j2".format(template_chunk)

        subj_alt_records = []
        for record in self.records:
            subj_alt_str = "DNS:{}".format(record)
            subj_alt_records.append(subj_alt_str)

        data = {
            "web_domain": self.name_idn,
            "listen_server": self.ip_addr,
            "server_template": server_template,
            "server_names": " ".join(str(r) for r in self.records),
            "ssl_cert": self.ssl_cert,
            "owner": self.owner
        }

        json_string = json.dumps(data)   
        extra_vars = "--extra-vars '{}'".format(json_string)

        return extra_vars


class WebDomainRecord(object):

    def __init__(self, name_idn, record_type='A'):
        self.name_idn = name_idn
        self.record_type = record_type

    def __str__(self):
        return str(self.name_idn)

    def __repr__(self):
        return str(self.name_idn)
