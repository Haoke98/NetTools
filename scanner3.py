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
from scapy.layers.inet import ICMP, IP

SUBNET = "192.168.0.0/24"


class Scanner:
    hosts_up = []

    def check(self, targetIP: str):
        pkt = IP(dst=targetIP) / ICMP()
        ans, unans = sr(pkt, timeout=10)
        for s, r in ans:
            host = r.sprintf('%IP.src%')
            if not self.hosts_up.__contains__(host):
                self.hosts_up.append(host)
                print(f"{host} is Alive.")

    def scan(self, targetSubnet):
        for ip in ipaddress.IPv4Network(targetSubnet):
            # self.check(str(ip))
            th = threading.Thread(target=Scanner.check, args=(self, str(ip)))
            th.start()
        while True:
            print("AliveHosts:", self.hosts_up)
            time.sleep(5)


if __name__ == '__main__':
    s = Scanner()
    s.scan(SUBNET)
