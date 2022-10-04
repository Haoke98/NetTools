# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/10/5
@Software: PyCharm
@disc:
======================================="""
from scapy.all import *
from scapy.layers.inet import IP, TCP
if __name__ == '__main__':
    ganyu = '192.168.0.100'
    ganyuport = 3306
    pkt = IP(dst=ganyu) / TCP(dport=ganyuport, flags='S')
    ans, unans = sr(pkt, timeout=1)
    for s, r in ans: print(r.sprintf('%IP.src% is alive'))
    for s in unans: print('you ip is not alive')
