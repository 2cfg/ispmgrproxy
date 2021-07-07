#!/usr/bin/env python3
import json

class WebDomain(object):

    def __init__(self, id, name_idn, email, updated_at, active=True, suspended=False):

        self.id = id
        self.name_idn = name_idn
        self.active = active
        self.suspended = suspended
        self.records = []
        self.email = email
        self.updated_at = updated_at

    def get_ansible_extra_vars(self, _config):
        # check nginx conf exist
        # check ssl state
        # check cert files exist

        # TODO: Config for wildcard domains
        # TODO: Mysql Trigger on table webdomain active / suspended
        
        
        active_chunk = "active" if self.active else "suspended"
        ssl_chunk = "_ssl" if _config.ssl_enabled else ""
        template_chunk = "{}{}".format(active_chunk, ssl_chunk)
        server_template = "server_{}_template.conf.j2".format(template_chunk)

        subj_alt_records = []
        for record in self.records:
            subj_alt_str = "DNS:{}".format(record)
            subj_alt_records.append(subj_alt_str)

        data = {
            "web_domain": self.name_idn,
            "server_template": server_template,
            "server_names": " ".join(str(r) for r in self.records),
            "owner_email": self.email,
            "domain_active": self.active,
            "subject_alt_name": ",".join(r for r in subj_alt_records)
        }

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
