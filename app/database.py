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
#        cursor.reset()

        query = ("SELECT DISTINCT domain FROM dnsmon.updates")
        cursor.execute(query)

        for (domain,) in cursor.fetchall():
            query = ("SELECT id, active, int_suspend, email from ispmgr.webdomain WHERE name_idn = '{}'".format(domain))

            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                continue
            (id, active, int_suspend, email) = result
            webdomain = WebDomain(id=id, name_idn=domain, active=active, suspended=int_suspend, email=email)
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
        cursor = cnx.cursor()

        query = ("SELECT name_idn from ispmgr.webdomain_alias WHERE webdomain = '{}'".format(webdomain.id))
        cursor.execute(query)

        for (record,) in cursor.fetchall():
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
