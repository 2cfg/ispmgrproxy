#!/usr/bin/env python3
import ansible_runner
import os
import sys
import app.database as db
from app.configparser import ConfigParser
from app.domainresolver import DomainResolver

def run_playbook(playbook, extra_vars):
    out, err, rc = ansible_runner.run_command(
        executable_cmd='ansible-playbook',
        cmdline_args=[playbook, extra_vars],
        host_cwd='/root/ansible-control',
        input_fd=sys.stdin,
        output_fd=sys.stdout,
        error_fd=sys.stderr,
    )
    print("out: {}".format(out))
    print("err: {}".format(err))
    print("rc: {}".format(rc))

if __name__ == '__main__':

    webdomains = db.get_webdomains_to_update()
    for webdomain in webdomains:
        db.fill_webdomain_records(webdomain)

        _config = ConfigParser(webdomain)

        # новый домен
        if not _config.ngx_vhost_config_exist: 
            # создать конфиг
            run_playbook('configure_webdomain.yml', webdomain.get_ansible_extra_vars(_config))

            _config = ConfigParser(webdomain)

        # проверить разрешение имён
        resolver = DomainResolver(webdomain.records)
        if not resolver.resolve_all():
            continue

        if _config.required_new_ssl_cert:
            # выпустить сертификат  
            run_playbook('configure_ssl_cert.yml', webdomain.get_ansible_extra_vars(_config))
            

        if _config.ssl_vhost_fullchain_exist and _config.ssl_vhost_privkey_exist:
            _config.ssl_enabled = True
            run_playbook('configure_webdomain.yml', webdomain.get_ansible_extra_vars(_config))

            # обновить в БД инфомрацию о том, что операция выполнена
