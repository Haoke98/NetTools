# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/10/5
@Software: PyCharm
@disc:
======================================="""
from scapy.all import *
from scapy.layers.l2 import ARP, Ether

if __name__ == '__main__':
    ganyu = '192.168.0.102'
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ganyu)
    ans, unans = srp(pkt, timeout=1)
    for s, r in ans:
        print('success')
        print(r.sprintf('%Ether.src% - %ARP.psrc%'))
