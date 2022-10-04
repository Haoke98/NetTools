from scapy.all import sniff
from scapy.layers.inet import TCP, IP


def packet_callback(packet):
    if packet[IP]:
        print(f"{packet.src} --> {packet.dst}, {packet[IP].src} --> {packet[IP].dst}")
        if packet[TCP]:
            # print(f"TCP {packet[TCP]['src_address']}({packet.src}) --> {packet[TCP].dst_address}({packet.dst})")
            myPacket = str(packet[TCP].payload)
            if 'user' in myPacket.lower() or 'pass' in myPacket.lower():
                print(f"[*] Destination: {packet[IP].dst}, TCP.payload: {str(packet[TCP].payload)}")
        # print(f"{packet['protocol']} {packet[TCP].src_address}({packet.src}) --> {packet[TCP].dst_address}({packet.dst})")
    else:
        print(f"{packet.src} --> {packet.dst}")




def main():
    # sniff(filter='tcp port 110 or tcp port 25 or tcp port 143', prn=packet_callback, store=0)
    sniff(prn=packet_callback, store=0)


if __name__ == '__main__':
    main()
