# This is a sample Python script.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press Shift+F10 to execute it or replace it with your code.
import socket
import threading
import time

from netaddr import IPNetwork

# 扫描的子网络
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


    try:
        while True:
            # print("ICMP -> Type: %d Code: %d"%(icmp_header.type,icmp_header.code))
            pass
    except:
        pass
