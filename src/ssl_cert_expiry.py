'''

    Utility to find ssl certificate expiry date for any domain

    Author  : Viki (a) Vignesh Natarajan
    Contact : vikiworks.io

'''

import socket
import ssl
import datetime


def get_ssl_cert_info(domain_name):
    # timeout in seconds
    connection_timeout = 10.0

    #create context
    ctx = ssl.create_default_context()
    ctx.check_hostname = False

    conn = ctx.wrap_socket( socket.socket(socket.AF_INET), server_hostname=domain_name,)

    # 5 second timeout
    conn.settimeout(10.0)

    conn.connect((domain_name, 443))

    ssl_cert_info = conn.getpeercert()

    return ssl_cert_info

def get_ssl_expiry_date(domain_name):
    # ssl date and time format
    date_time_format = r'%b %d %H:%M:%S %Y %Z'

    ssl_cert_info = get_ssl_cert_info(domain_name)
    ssl_expiry_date = datetime.datetime.strptime(ssl_cert_info['notAfter'], date_time_format)
    # Python datetime object
    return ssl_expiry_date

if __name__ == "__main__":
    url_list = [
        "vikilabs.org",
        "asdfasdfas.io"
    ]

    print "\nDomain Expire Info: \n"
    for url in url_list:
        current_date = datetime.datetime.now()

        try:
            expiry_date = get_ssl_expiry_date(url)
            expiry_date_str = expiry_date.strftime("%Y-%m-%d")
            ndays = (expiry_date-current_date).days

            print ("\t[ DOMAIN : {} \t\t] [ EXPIRY_DATE : {} \t] [ NO DAYS TO EXPIRE : {} \t\t]".format(url, expiry_date_str, ndays))
        except Exception as e:
            print ("\t[ DOMAIN : {} \t\t] [ ERROR \t\t\t\t\t\t] [ ERROR \t\t\t\t\t\t]".format(url))
            #print (e)

    print "\n"
