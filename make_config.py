#!/usr/bin/env python3
import ansible_runner
import os
import sys
import app.database as db
from app.configparser import ConfigParser
# from app.domainresolver import DomainResolver
import json

def run_playbook(playbook, extra_vars):
    out, err, rc = ansible_runner.run_command(
        executable_cmd='ansible-playbook',
        cmdline_args=[playbook, extra_vars],
        host_cwd='/root/ansible-control',
        input_fd=sys.stdin,
        output_fd=sys.stdout,
        error_fd=sys.stderr,
    )
    
    return rc


if __name__ == '__main__':

    webdomains = db.get_webdomains_to_update()

    for webdomain in webdomains:

        # remove old configurations
        if hasattr(webdomain, "removed"):
            if webdomain.removed:
                extra_vars = "--extra-vars '{}'".format(json.dumps({"web_domain": webdomain.name_idn}))
                rc = run_playbook('remove_webdomain.yml', extra_vars)
                db.remove_from_queue(webdomain)
                continue

        db.fill_webdomain_records(webdomain)
        _config = ConfigParser(webdomain)

        # скопировать SSL-сертификат, при наличии
        rc = run_playbook('configure_ssl_cert.yml', webdomain.get_ansible_extra_vars(_config))
   
        # создать конфиг
        rc = run_playbook('configure_webdomain.yml', webdomain.get_ansible_extra_vars(_config))

        if rc != 0:
            continue

        #     _config = ConfigParser(webdomain)

        # # проверить разрешение имён
        # resolver = DomainResolver(webdomain.records)
        # if not resolver.resolve_all():
        #     continue

        # if _config.required_new_ssl_cert:
        #     # выпустить сертификат  
        #     rc = run_playbook('configure_ssl_cert.yml', webdomain.get_ansible_extra_vars(_config))

        #     if rc != 0:
        #         continue

        # _config = ConfigParser(webdomain)
            
        # if _config.ssl_vhost_fullchain_exist and _config.ssl_vhost_privkey_exist:
        #     _config.ssl_enabled = True
        #     rc = run_playbook('provision_ssl_cert.yml', webdomain.get_ansible_extra_vars(_config))

        #     if rc != 0:
        #         continue

        # _config = ConfigParser(webdomain)
            
        # if _config.ssl_vhost_fullchain_exist and _config.ssl_vhost_privkey_exist:
        #     _config.ssl_enabled = True
        #     rc = run_playbook('configure_webdomain.yml', webdomain.get_ansible_extra_vars(_config))

        #     if rc != 0:
        #         continue

        
        # _config = ConfigParser(webdomain)

        # if not _config.ngx_vhost_config_exist:
        #     print("ngx_vhost_config_exist")
        #     continue
        # if not _config.ssl_vhost_fullchain_exist:
        #     print("ssl_vhost_fullchain_exist")
        #     continue
        # if not _config.ssl_vhost_privkey_exist:
        #     print("ssl_vhost_privkey_exist")
        #     continue
        # if not _config.ssl_enabled:
        #     print("ssl_enabled")
        #     continue

        # обновить в БД инфомрацию о том, что операция выполнена
        db.remove_from_queue(webdomain)
        # print("remove_from_queue")
