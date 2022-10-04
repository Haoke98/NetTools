#! pthon3
# This is a sample Python script.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press Shift+F10 to execute it or replace it with your code.
import ipaddress
import os
import socket
import sys
import threading
import time

# 扫描的子网络
from netHeaderDecodeHelper import IP2, ICMP2

SUBNET = "192.168.0.0/24"

# 自定义字符串， 将在ICMP响应中进行核对
MAGIC_MESSAGE = "PYTHON-RULES!"


# 批量发送UDP数据包
def udp_sender(subnet, magicMsg):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(subnet).hosts():
            sender.sendto(bytes(magicMsg, 'utf-8'), (str(ip), 65212))
            # print(f"侦察机已出发，目标：{ip}")


class Scanner:
    def __init__(self, host):
        self.host = host
        if os.name == "nt":
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP
        self.sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.sniffer.bind((host, 0))  # Listen to our machine
        self.sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        if os.name == "nt":
            # 在windows平台上，我们需要设置IOCTL以启用混杂模式。
            self.sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self):
        print(f"开始嗅探主机[{self.host}]了.....")
        hosts_up = set([f'{str(self.host)} *'])
        try:
            while True:
                # read a packet
                raw_buffer, (ip, n) = self.sniffer.recvfrom(65565)
                # create an IP header from the first 20 bytes
                ip_header = IP2(raw_buffer[0:20])
                if ip_header.protocol == "ICMP":
                    # calculate where our ICMP packet starts
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    # create ICMP structure
                    icmp_header = ICMP2(buf)
                    # check for TYPE 3 and CODE
                    if icmp_header.code == 3 and icmp_header.code == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(SUBNET):
                            # make sure it has our magic message:
                            if raw_buffer[len(raw_buffer) - len(MAGIC_MESSAGE):] == bytes(MAGIC_MESSAGE, 'utf-8'):
                                tgt = str(ip_header.src_address)
                                if tgt != self.host and tgt not in hosts_up:
                                    hosts_up.add(str(ip_header.src_address))
                                    print(f"Hosts up: {tgt}, TTL:{ip_header.ttl}")
                    # print(f"[{ip}] {ip_header.src_address} --> {ip_header.dst_address} , Version:{ip_header.ver}, "
                    #       f"Header Length:{ip_header.ihl}, , "
                    #       f"ICMP -> Type:{icmp_header.type}, Code:{icmp_header.code}")
        except KeyboardInterrupt:
            if os.name == "nt":
                self.sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            sys.exit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    s = Scanner("192.168.0.102")
    ts = threading.Thread(target=Scanner.sniff, args=(s,))
    ts.start()
    t = threading.Thread(target=udp_sender, args=(SUBNET, MAGIC_MESSAGE))
    t.start()
