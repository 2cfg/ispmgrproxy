#!/usr/bin/env python3


class WebDomain(object):

    def __init__(self, id, name_idn, active=True, suspended=False):

        self.id = id
        self.name_idn = name_idn
        self.active = active
        self.suspended = suspended
        self.records = []

    def get_ansible_extra_vars(self):
        
        records = ':'.join(str(r) for r in self.records)
        
        extra_vars = '--extra-vars "WEB_DOMAIN={} DOMAIN_RECORDS={}"'.format(self.name_idn, records)

        return extra_vars


class WebDomainRecord(object):

    def __init__(self, name_idn, record_type='A'):
        self.name_idn = name_idn
        self.record_type = record_type

    def __str__(self):
        return str(self.name_idn)

    def __repr__(self):
        return str(self.name_idn)