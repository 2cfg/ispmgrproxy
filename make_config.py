#!/usr/bin/env python3
import ansible_runner
import os
import sys
import app.database as db

if __name__ == '__main__':

    webdomains = db.get_webdomains_to_update()
    for webdomain in webdomains:
        db.fill_webdomain_records(webdomain)
        # print(webdomain.get_ansible_extra_vars())
        out, err, rc = ansible_runner.run_command(
           executable_cmd='ansible-playbook',
           cmdline_args=['configure_webdomain.yml', webdomain.get_ansible_extra_vars()], # for example, see playbook.yml
           host_cwd='/root/ansible-control',
           input_fd=sys.stdin,
           output_fd=sys.stdout,
           error_fd=sys.stderr,
        )
        print("out: {}".format(out))
        print("err: {}".format(err))
        print("rc: {}".format(rc))
