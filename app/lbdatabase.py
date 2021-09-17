import app.config as config
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
from app.webdomain import WebDomain, WebDomainRecord


def get_webdomains_to_update():
    domains = []

    try:
        cnx = connection.MySQLConnection(**config.lb_database)
        cursor = cnx.cursor(buffered=True)
        ssl_cert = 'NULL'

        query = ("SELECT DISTINCT name_idn FROM lb.updates_web")
        cursor.execute(query)
        
        for (domain,) in cursor.fetchall():

            if '*' in str(domain):
                continue
            
            query = ("SELECT updated_at FROM lb.updates_web WHERE name_idn = '{}' ORDER BY updated_at DESC LIMIT 1;".format(domain))
            cursor.execute(query)
            (updated_at, ) = cursor.fetchone()

            query = ("SELECT lb_ipaddr, real_ipaddr, user_id, botguard_check, l7filter, active, secure, redirect_http from lb.webdomain_options WHERE name_idn = '{}'".format(domain))

            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                webdomain = type('WebDomain', (object,), {"name_idn":domain, "updated_at": updated_at, "removed": True})
                domains.append(webdomain)
                continue

            (lb_ipaddr, real_ipaddr, user_id, botguard_check, l7filter, active, secure, redirect_http,) = result

            if not botguard_check:
                botguard_check = 'off'

            if l7filter == "on":
                l7filter = True
            else:
                l7filter = False

            webdomain = WebDomain(id=id, ip_addr=lb_ipaddr, name_idn=domain, active=active, updated_at=updated_at,
                                 secure=secure, ssl_cert=ssl_cert, owner=user_id, real_ipaddr=real_ipaddr,
                                 redirect_http=redirect_http, botguard_check=botguard_check, l7filter=l7filter)

            domains.append(webdomain)

        cursor.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

    return domains

def fill_webdomain_records(webdomain):

    try:
        cnx = connection.MySQLConnection(**config.lb_database)
        cursor = cnx.cursor(buffered=True)

        query = ("SELECT alias from lb.webdomain_alias WHERE name_idn = '{}'".format(webdomain.name_idn))
        cursor.execute(query)

        for (record,) in cursor.fetchall():
            
            webdomain_record = WebDomainRecord(name_idn=record)
            webdomain.records.append(webdomain_record)


        cursor.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

def remove_from_queue(webdomain):

    result = False

    try:
        cnx = connection.MySQLConnection(**config.lb_database)
        cursor = cnx.cursor(buffered=True)

        query = ("DELETE FROM lb.updates_web WHERE name_idn = '{}' and updated_at <= {}".
          format(webdomain.name_idn, webdomain.updated_at))
        cursor.execute(query)

        cnx.commit()
        cursor.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:

        cnx.close()
        result = True

    return result
