import datetime
import pymysql
import time
import requests
import pyperclip
from time import sleep

host = '74.93.130.114'
port = 3306
username = "sql"
password = "@AAGoods2019"
db_reroute = "Reroute"
sql_login_reroute = host, port, username, password, db_reroute

# info to scrape store router
start_url = "https://aagoods.lkdev.com/ajax_checkbook_storerouting.php?scannedval="
end_url = "&frommachine=1"
user_name = "aagoods"
pass_word = "ilovemedia!"
url = (start_url, end_url, user_name, pass_word)


def find_asin(barcode, sql_login=sql_login_reroute):
    a = sql_login
    conn = pymysql.connect(host=a[0], port=a[1], user=a[2], passwd=a[3], db=a[4])
    sql = "SELECT * FROM UPC WHERE UPC = (%s)"
    cur = conn.cursor()
    cur.execute(sql, barcode)
    a = cur.fetchone()
    cur.close()
    conn.close()
    if a is None:
        asin = barcode
    else:
        asin = a[2]
    return asin


def add_asin(data, sql_login=sql_login_reroute):
    a = sql_login
    conn = pymysql.connect(host=a[0], port=a[1], user=a[2], passwd=a[3], db=a[4])
    sql = "INSERT INTO UPC (UPC, Reroute, Time_stamp) VALUES (%s, %s, %s)"
    sql_info = data
    cur = conn.cursor()
    cur.execute(sql, sql_info)
    conn.commit()
    cur.close()
    conn.close()
    a = 'Added'
    return a


def check_item(Asin, url_info=url):
    send_data = (url_info[0] + Asin + url_info[1])
    r = requests.get(send_data, auth=(url_info[2], url_info[3]))
    return r


def sort_data_from_web(data):
    data1 = data.json()
    routeinfo = data1['routeinfo']
    Result = routeinfo['routedisplaytext']
    return Result


def check_data_15(Asin, url_info=url):
    run_count: int = 0
    stat = True
    send_data = (url_info[0] + Asin + url_info[1])
    data = False
    while stat:
        if run_count == 15:
            stat = False

        else:
            sleep(1)
            r = requests.get(send_data, auth=(url_info[2], url_info[3]))
            if r.text == "[]":
                run_count = 1 + run_count
            else:
                data = r
                run_count = 15

    return data


def copy_to_clipboard(Asin):
    pyperclip.copy(Asin)


def timestamp():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

