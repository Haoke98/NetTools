# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/12/25
@Software: PyCharm
@disc:
======================================="""
import datetime
import ipaddress
import sqlite3
from concurrent.futures import ThreadPoolExecutor

import requests

TOTAL = 255 * 255 * 255 * 255
COMPLETED = 0
STARTED_AT = datetime.datetime.now()


def get_progress():
    dlt = datetime.datetime.now() - STARTED_AT
    return f"进度：%0.4f%% ( {COMPLETED} / {TOTAL} ), 已运行：{dlt}, " % (COMPLETED / TOTAL * 100)


def get_ip_info(ip):
    resp = requests.get(f"https://api-v3.speedtest.cn/ip?ip={ip}")
    respJson: dict = resp.json()['data']
    country = respJson['country']
    countryCode = respJson['countryCode']
    province = respJson['province']
    city = respJson['city']
    district = respJson['district']
    isp = respJson['isp']
    operator = respJson['operator']
    lon = ""
    lat = ""
    if respJson.keys().__contains__("lon"):
        lon = respJson['lon']
        lat = respJson['lat']
    return country, countryCode, province, city, district, isp, operator, lon, lat


def insert(ip):
    global COMPLETED
    ip_str = ip[0].compressed
    con = sqlite3.connect("ips.db")
    updatedAt = datetime.datetime.now()
    values = (ip_str, updatedAt) + get_ip_info(ip_str)
    con.execute(
        'INSERT INTO ips(ip,updatedAt,country,countryCode,province,city,district,isp,operator,lon,lat) values(?,?,?,?,?,?,?,?,?,?,?)',
        values)
    con.commit()
    con.close()
    COMPLETED += 1
    print(get_progress(), values)


def update(ip):
    global COMPLETED
    ip_str = ip[0].compressed
    con = sqlite3.connect("ips.db")
    updatedAt = datetime.datetime.now()
    values = (updatedAt,) + get_ip_info(ip_str)
    con.execute(
        '''UPDATE ips SET updatedAt=?,country=?,countryCode=?,province=?,city=?,district=?,isp=?,operator=?,lon=?,lat=? WHERE ip= ?''',
        values + (ip_str,))
    con.commit()
    con.close()
    COMPLETED += 1
    print(get_progress(), values)


# weeks=1)):


def all():
    global COMPLETED
    con = sqlite3.connect("ips.db")
    try:
        con.execute(
            "CREATE TABLE ips(ip varchar(15) primary key, updatedAt timestamp , country varchar(255),countryCode varchar(255), province varchar(255),city varchar(255),district varchar(255),isp varchar(255),operator varchar(255),lon varchar(255),lat varchar(255))")
    except Exception as e:
        print(f"CREATE TABLE failed:[{e}]")
    pool = ThreadPoolExecutor(max_workers=5)
    net = ipaddress.ip_network("0.0.0.0/0")
    hosts = net.hosts()
    for ip in hosts:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM ips WHERE ip='{str(ip)}'")
        res = cur.fetchall()
        cur.close()
        if len(res) == 0:
            pool.submit(insert, (ip,))
        else:
            obj = res[0]
            ip = obj[0]
            if "." in obj[1]:
                updatedAt = datetime.datetime.strptime(obj[1].split(".")[0], "%Y-%m-%d %H:%M:%S")
            else:
                updatedAt = datetime.datetime.strptime(obj[1], "%Y-%m-%d %H:%M:%S")
            dlt = datetime.datetime.now() - updatedAt
            if dlt > datetime.timedelta(weeks=1):
                pool.submit(update, (ip,))
            else:
                COMPLETED += 1
                print(get_progress(), ip, updatedAt, dlt)
    pool.shutdown(wait=True)


if __name__ == '__main__':
    all()
