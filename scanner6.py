# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/10/5
@Software: PyCharm
@disc:
======================================="""
from scapy.all import *
from scapy.layers.inet import *

if __name__ == '__main__':
    ganyu = '192.168.0.102'
    for i in range(1, 65535):
        ganyuport = i
        ganyusport = RandShort()  # 由于在和目标端口建立连接的时候，自己也需要使用一个源端口，RandShort用于随机产生一个端口号
        pkt = IP(dst=ganyu) / TCP(sport=ganyusport, dport=ganyuport, flags='S')
        ans = sr1(pkt, timeout=1)  # 指定等待应答数据包的时间，不使用的话可能需要要等待很久
        if str(type(ans)) == "<class 'NoneType'>":
            print('%s' % ganyu, ':%s is closed' % ganyuport)
        elif ans.haslayer(TCP):
            if ans.getlayer(TCP).flags == 'SA':  # SYN+ACK
                seq1 = ans.ack
                ack1 = ans.seq + 1
                pkt_rst = IP(dst=ganyu) / TCP(sport=ganyusport, dport=ganyuport, seq=seq1, ack=ack1, flags='A')  # ACK
                send(pkt_rst)
                print('%s' % ganyu, ':%s is open' % ganyuport)
            elif ans.getlayer(TCP).flags == 'R':  # RST
                print('%s' % ganyu, ':%s is closed' % ganyuport)
