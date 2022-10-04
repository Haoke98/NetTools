import os
import socket
import sys

from netHeaderDecodeHelper import IP2


def sniff(host: str):
    if os.name == "nt":
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    if os.name == "nt":
        # 在windows平台上，我们需要设置IOCTL以启用混杂模式。
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    print(f"开始嗅探主机[{host}]了.....")
    devices = []
    try:
        while True:
            # read a packet
            raw_buffer, (ip, n) = sniffer.recvfrom(65565)
            # create an IP header from the first 20 bytes
            ip_header = IP2(raw_buffer[0:20])
            print("[%s]Protocol: %s %s --> %s" % (ip,ip_header.protocol, ip_header.src_address, ip_header.dst_address))
            if not devices.__contains__(ip):
                devices.append(ip)
                # print(ip)
            # time.sleep(0.5)
    except KeyboardInterrupt:
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()


if __name__ == '__main__':
    sniff("192.168.0.102")
