#!/usr/bin/env python3
import json

class WebDomain(object):

    def __init__(self, id, name_idn, active=True, suspended=False):

        self.id = id
        self.name_idn = name_idn
        self.active = active
        self.suspended = suspended
        self.records = []

    def get_ansible_extra_vars(self):
        # TODO: Trigger on table webdomain
        if self.active:
            server_template = "server_active_template.conf.j2"
        else:
            server_template = "server_suspended_template.conf.j2"

        data = {
            "web_domain": self.name_idn,
            "server_template": server_template,
            "server_names": " ".join(str(r) for r in self.records)
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