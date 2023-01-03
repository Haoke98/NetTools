# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/12/30
@Software: PyCharm
@disc:
======================================="""
import re

from IPy import IP


# 解析10.245.1.1-10.245.1.10这种类型的ip段
def all_for_one(dates):
    ipx = dates.split('-')
    ip2num = lambda x: sum([256 ** i * int(j) for i, j in enumerate(x.split('.')[::-1])])
    num2ip = lambda x: '.'.join([str(x // (256 ** i) % 256) for i in range(3, -1, -1)])
    a = [num2ip(i) for i in range(ip2num(ipx[0]), ip2num(ipx[1]) + 1) if not ((i + 1) % 256 == 0 or (i) % 256 == 0)]
    return a


# 解析带掩码的ip段
def netmask_to_ip(dates):
    dic = []
    for date in dates:
        ip_name = date
        ret = re.search(r'((2[0-4]\d|25[0-5]|[01]{0,1}\d{0,1}\d)\.){3}(2[0-4]\d|25[0-5]|[01]{0,1}\d{0,1}\d)[-/]',
                        ip_name)  # 是区分IP段中是否含有-以及/
        if (ret != None):
            ret = re.search(r'((2[0-4]\d|25[0-5]|[01]{0,1}\d{0,1}\d)\.){3}(2[0-4]\d|25[0-5]|[01]{0,1}\d{0,1}\d)[/]',
                            ip_name)  # 是区分IP段中是否含有/
            if (ret != None):
                ip = IP(ip_name,
                        make_net=1)  # 注意此处必须添加参数 make_net=1，IPy模块的缺陷，主要是make_net默认为0，就是标准的iP最后一位是16,32，这种才行，设置为1，就可以自己定义了。
                for x in ip:
                    dic.append(str(x))
            else:
                ip_result = all_for_one(ip_name)  # 解析10.245.1.1-10.245.1.10这种类型的ip段
                return ip_result
    return list(set(dic))


if __name__ == "__main__":
    # net = ipaddress.ip_network("36.0.0.0/9")
    # hosts = net.hosts()
    # for ip in hosts:
    #     print(ip)
    # net_list = ['10.10.10.1/29']
    net_list = ['36.96.0.0/9']
    ip_list = netmask_to_ip(net_list)
    for i, ip in enumerate(ip_list):
        print(i, ip)
