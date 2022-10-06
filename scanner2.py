# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/10/5
@Software: PyCharm
@disc:
======================================="""
from concurrent.futures import ThreadPoolExecutor

import netaddr
from scapy.all import *
from scapy.layers.l2 import Ether, ARP


def ipv4Network(subnet: str):
    a, b = subnet.split("/")
    a1, a2, a3, a4 = str(a).split(".")
    b = int(b)
    if b == 24:
        print("NetMask:", "1" * b + "0" * (32 - b), " ===>> ", "255.255.255.0")
        for i in range(1, 255):
            yield f"{a1}.{a2}.{a3}.{i}"


class Scanner:
    hosts_up = []

    def __init__(self):
        self.sendedcount = 0
        self.silent = 0
        self.aliveCount = 0
        self.startedAt = None

    def get_mac(self, targetIP: str):
        pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op="who-has", pdst=targetIP)
        complete = self.aliveCount + self.silent
        progress = complete / self.sendedcount
        print(f"\rScanning now: %0.2f%% ({complete}/{self.sendedcount})" % (progress * 100), end='')
        ans, unans = srp(pkt, timeout=10, verbose=0)
        for s, r in ans:
            print(r.sprintf('\n%Ether.src% - %ARP.psrc%'))
            ip = r[ARP].psrc
            hw = r[Ether].src
            device = {'ip': ip, 'hardware': hw}
            if not self.hosts_up.__contains__(device):
                self.hosts_up.append(device)
            self.aliveCount += 1
            return
        self.silent += 1

    def scan(self):
        self.startedAt = time.time()
        threadPool = ThreadPoolExecutor(120)
        for targetIP in netaddr.IPNetwork("192.168.0.0/24"):
            self.sendedcount += 1
            threadPool.submit(Scanner.get_mac, self, str(targetIP))
            # th = threading.Thread(target=Scanner.get_mac, args=(self, str(targetIP)))
            # th.start()
        print("\n扫描准备工作已完成，部分侦察机早已出发")
        while True:
            complete = self.silent + self.aliveCount
            if complete > 0 and complete == self.sendedcount:
                print(f"\n扫描已完成！所用时间：{time.time() - self.startedAt}毫秒:")
                for i, device in enumerate(self.hosts_up):
                    print(f"{i + 1}.  {device.get('ip')} - {device.get('hardware')}")
                break


if __name__ == '__main__':
    s = Scanner()
    s.scan()
    # SUBNET = "192.168.0.0/24"
    # for ip in ipv4Network(subnet=SUBNET):
    #     print(ip)
