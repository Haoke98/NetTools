import os
import socket
host = "192.168.0.100"
if __name__ == '__main__':

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
    while True:
        res = sniffer.recvfrom(65565)
        ip = res[1][0]
        if not devices.__contains__(ip):
            devices.append(ip)
            print(ip)
        # time.sleep(0.5)
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
