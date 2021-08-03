#!/usr/bin/env python3
from app.webdomain import WebDomain
from pathlib import Path
import app.config as config

class ConfigParser(object):
    def __init__(self, webdomain):
        self.name_idn = webdomain.name_idn
        self.records = []
        self.ngx_vhost_config = ''
        self.ssl_vhost_fullchain = ''
        self.ssl_vhost_privkey = ''
        self.secure = 'off'
        self.active = False
        self.ssl_type = ''
        self.ssl_valid_after = ''
        self.ssl_cert = ''
        self.redirect_http = ''
        self.new_records = webdomain.records
        self.ngx_vhost_config_exist = False
        self.ssl_vhost_fullchain_exist = False
        self.ssl_vhost_privkey_exist = False
        self.required_new_ssl_cert = False
        self.options_parsed = False
        self.webdomain = webdomain

        self.check_ngx_config_exist()
        self.check_ssl_config_exist()
        self.parse_options()
        self.check_required_new_ssl_cert()

    def check_ngx_config_exist(self):
        self.ngx_vhost_config = "{}/{}.conf".format(config.NGX_CONFIG_LOCATION, self.name_idn)
        self.ngx_vhost_config_exist = Path(self.ngx_vhost_config).exists()
 
    def check_ssl_config_exist(self):
        self.ssl_vhost_fullchain = "{}/{}.fullchain.crt".format(config.SSL_CERT_LOCATION, self.name_idn)
        self.ssl_vhost_fullchain_exist = Path(self.ssl_vhost_fullchain).exists()

        self.ssl_vhost_privkey = "{}/{}.private.key".format(config.SSL_CERT_LOCATION, self.name_idn)
        self.ssl_vhost_privkey_exist =  Path(self.ssl_vhost_privkey).exists()


    def parse_options(self):
        if self.ngx_vhost_config_exist:
            try:
                with open(self.ngx_vhost_config) as f:
                    first_line = f.readline()

                    options = first_line.split('$')[1:]

                    self.secure = options[0].split(':')[1]
                    self.active = options[1].split(':')[1]
                    self.ssl_type = options[2].split(':')[1]
                    self.ssl_valid_after = options[3].split(':')[1]
                    self.ssl_cert = options[4].split(':')[1]
                    self.redirect_http = options[5].split(':')[1]
                    self.records = options[6].split(':')[1].split()

                    self.options_parsed = True
            except:
                print("Can't parse options from file {}".format(self.ngx_vhost_config))


    def check_required_new_ssl_cert(self):
        if self.webdomain.secure == 'off':
            self.required_new_ssl_cert = False
            return

        if not self.ssl_vhost_fullchain_exist:
            self.required_new_ssl_cert = True
            return

        if not self.ssl_vhost_privkey_exist:
            self.required_new_ssl_cert = True
            return
        

        for record in self.new_records:
            if str(record) not in self.records:
                self.required_new_ssl_cert = True
                break