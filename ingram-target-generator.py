# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/12/30
@Software: PyCharm
@disc:
======================================="""
import os.path

ALL = 255 * 255 * 255 * 255


def handle(line: str):
    start, end, net, count = line.split("\t")
    return start, end, net, int(count)


def main(in_file_name: str):
    out_file_name: str = os.path.join("ingram-targets", os.path.basename(in_file_name))
    with open(out_file_name, encoding="utf-8", mode='w') as fw:
        with open(in_file_name, encoding="utf-8", mode='r') as fr:
            i = 0
            total = 0
            while True:
                i += 1
                line = fr.readline()
                if line == '':
                    break
                start, end, net, count = handle(line)
                fw.write(f"{start}-{end}\n")
                total += count
                print(i, line.replace("\n", ''))
            percent = total / ALL * 100
            print(f"总共：{total} 个IP地址, 占总IP库的 %0.5f%% ( {total} / {ALL} )" % percent)


if __name__ == "__main__":
    main("ips/CN-20221230.txt")
