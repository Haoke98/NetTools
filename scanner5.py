# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/10/5
@Software: PyCharm
@disc:
======================================="""
import ipaddress

from scapy.all import *
from scapy.layers.inet import IP, UDP

if __name__ == '__main__':
    for host in ipaddress.ip_network("192.168.0.0/24").hosts():
        ganyu = str(host)
        ganyuport = 3306
        packet = IP(dst=ganyu) / UDP(dport=ganyuport)
        ans = sr1(packet, timeout=1.0)
        if ans:
            if int(ans[IP].proto) == 1:
                print(ganyu + ' ' + 'is alive')
            else:
                print(ganyu + ' ' + 'is alive1')
        else:
            print(ganyu + ' ' + 'is alive2')
