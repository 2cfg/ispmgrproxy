#!/usr/bin/env python3
import ansible_runner
import os
import sys
import app.database as db
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

    if os.path.exists("/tmp/make_config.lock"):
        print("Process already running. Exit..")
        exit()

    lock_file = open("/tmp/make_config.lock", "a+")
    lock_file.close()

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
       
        # скопировать SSL-сертификат, при наличии
        if webdomain.secure == 'on':
            rc = run_playbook('configure_ssl_cert.yml', webdomain.get_ansible_extra_vars())
   
        # создать конфиг
        rc = run_playbook('configure_webdomain.yml', webdomain.get_ansible_extra_vars())

        if rc != 0:
            continue

        # обновить в БД инфомрацию о том, что операция выполнена
        db.remove_from_queue(webdomain)

    # remove lock file
    os.remove("/tmp/make_config.lock")

# TODO: Openresty stub status and triggers to zabbix