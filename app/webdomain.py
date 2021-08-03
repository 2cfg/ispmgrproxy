#!/usr/bin/env python3
import json

class WebDomain(object):

    def __init__(self, id, ip_addr, name_idn, email, dirindex, updated_at, secure, ssl_cert, ssl_valid_after, ssl_type, owner, redirect_http, active=True):

        self.id = id
        self.ip_addr = ip_addr
        self.name_idn = name_idn
        self.active = active
        self.secure = secure
        self.ssl_valid_after = ssl_valid_after
        self.ssl_type = ssl_type
        self.ssl_cert = ssl_cert
        self.redirect_http = redirect_http
        self.owner = owner
        self.records = []
        self.email = email
        self.updated_at = updated_at
        self.dirindex = dirindex

    def get_ansible_extra_vars(self, _config):

        active_chunk = "active" if self.active == 'on' else "suspended"
        ssl_chunk = "_ssl" if self.secure == 'on' else ""
        redirect_chunk = "_redirect" if self.redirect_http == 'on' else ""
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
            # "owner_email": self.email,
            # "domain_active": self.active,
            # "secure": self.secure,
            # "ssl_type": self.ssl_type,
            # "ssl_cert": self.ssl_cert,
            # "ssl_valid_after": str(self.ssl_valid_after),
            # "redirect_http": self.redirect_http,
            # "owner": self.owner,
            # "subject_alt_name": ",".join(r for r in subj_alt_records)
        }

        # print(data)
        json_string = json.dumps(data)   
        extra_vars = "--extra-vars '{}'".format(json_string)
        # print(extra_vars)

        return extra_vars


class WebDomainRecord(object):

    def __init__(self, name_idn, record_type='A'):
        self.name_idn = name_idn
        self.record_type = record_type

    def __str__(self):
        return str(self.name_idn)

    def __repr__(self):
        return str(self.name_idn)
