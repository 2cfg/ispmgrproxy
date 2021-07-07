#!/usr/bin/env python3

config = {
  'user': 'user',
  'password': 'password',
  'host': 'host',
  'raise_on_warnings': True
}

NGX_CONFIG_LOCATION = "/etc/nginx/sites-enabled"
SSL_CERT_LOCATION = "/etc/nginx/sslcert"

# LB External IP-address list
lb_ipaddr_list = [
    '1.1.1.1',
]
