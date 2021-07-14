import app.config as config
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
from app.webdomain import WebDomain, WebDomainRecord

def get_webdomains_to_update():
    domains = []

    try:
        cnx = connection.MySQLConnection(**config.database)
        cursor = cnx.cursor(buffered=True)

        query = ("SELECT DISTINCT domain FROM dnsmon.updates_web")
        cursor.execute(query)

        for (domain,) in cursor.fetchall():

            if '*' in str(domain):
                continue
            
            query = ("SELECT updated_at FROM dnsmon.updates_web WHERE domain = '{}' ORDER BY updated_at DESC LIMIT 1;".format(domain))
            cursor.execute(query)
            (updated_at, ) = cursor.fetchone()

            query = ("SELECT id, active, int_suspend, email, dirindex from ispmgr.webdomain WHERE name_idn = '{}'".format(domain))

            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                continue
            (id, active, int_suspend, email, dirindex) = result

            query = ("select ip.name as ip_addr from ispmgr.ipaddr as ip join ispmgr.ipaddr_webdomain as ipw on ip.id = ipw.ipaddr where ipw.webdomain = {}").format(id)
            cursor.execute(query)
            (ip_addr, ) = cursor.fetchone()

            webdomain = WebDomain(id=id, ip_addr=ip_addr, name_idn=domain, active=active, dirindex=dirindex, updated_at=updated_at, suspended=int_suspend, email=email)
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
        cnx = connection.MySQLConnection(**config.database)
        cursor = cnx.cursor(buffered=True)

        query = ("SELECT name_idn from ispmgr.webdomain_alias WHERE webdomain = '{}'".format(webdomain.id))
        cursor.execute(query)

        for (record,) in cursor.fetchall():

            if '*' in str(record):
                continue
            
            webdomain_record = WebDomainRecord(name_idn=record)
            webdomain.records.append(webdomain_record)
            # print("Process web domain record: {}".format(webdomain_record.name_idn))

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
        cnx = connection.MySQLConnection(**config.database)
        cursor = cnx.cursor(buffered=True)

        query = ("DELETE FROM dnsmon.updates_web WHERE domain = '{}' and updated_at <= {}".
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
