# This is a sample Python script.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press Shift+F10 to execute it or replace it with your code.
import os
import socket
import threading
import time

from netaddr import IPNetwork

# 扫描的子网络
from netHeaderDecodeHelper import IP

subnet = "192.168.0.0/24"

# 自定义字符串， 将在ICMP响应中进行核对
magicMsg = "PYTHON-RULES!"


# 批量发送UDP数据包
def udp_sender(subnet, magicMsg):
    time.sleep(5)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magicMsg, ("%s" % ip, 65212))
        except:
            pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    t = threading.Thread(target=udp_sender, args=(subnet, magicMsg))
    t.start()
    host = "192.168.0.102"
    if os.name == "nt":
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))  # Listen to our machine
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    if os.name == "nt":
        # 在windows平台上，我们需要设置IOCTL以启用混杂模式。
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    print(f"开始嗅探主机[{host}]了.....")
    devices = []
    try:
        while True:
            res = sniffer.recvfrom(65565)
            # print("res:", res)
            raw_buffer, (ip, n) = res
            ip_header = IP(raw_buffer[0:32])
            print("Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
            # print("ICMP -> Type: %d Code: %d"%(icmp_header.type,icmp_header.code))
            pass
    except KeyboardInterrupt:
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    # while True:
    #     if not devices.__contains__(ip):
    #         devices.append(ip)
    #         print(ip)
    #     # time.sleep(0.5)
