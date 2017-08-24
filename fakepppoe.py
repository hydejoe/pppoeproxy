# -*- coding: utf8 -*-
import dpkt, pcap, socket,os

local_mac = b"\x78\xac\xc0\x92\x56\x36"
PPPoE_PADI = b"\x09"
PPPoE_PADO = b"\x07"
PPPoE_PADR = b"\x19"
PPPoE_PADS = b"\x65"
PPPoE_PADT = b"\xA7"
PPPoE_SESSION = b"\x00"
PPPoE_DISCOVERY = b"\x88\x63"
PPPoE=b"\x88\x64"
PPP_LCP=b"\xc0\x21"
PPP_PAP=b"\xc0\x23"
PACKAGE_PADO = b"\x11\x07\x00\x00\x00,\x01\x01\x00\x00\x01\x03\x00\x04\x8c%\x00\x00\x01\x02\x00\x1cCQ-BN-LJT-BAS-2.MAN.ME60-X16 "
Session_ID=b"\x0d\x18"
PACKAGE_PADS = b"\x11e"+Session_ID+"\x00\x0c\x01\x01\x00\x00\x01\x03\x00\x04\x01-\x00\x00"


def start(interface="wlan0"):
    sniffer = pcap.pcap(name=interface, immediate=True)
    sock = None
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    sock.bind((interface, 0))
    handle_PADI(sniffer=sniffer, sock=sock)


def handle_PADI(sniffer, sock):
    dst_mac = b"\xff\xff\xff\xff\xff\xff"
    magic_number=bytes(os.urandom(6))
    for ts, pkt in sniffer:
        eth = dpkt.ethernet.Ethernet(pkt)
        pkt_src_mac = eth.pack_hdr()[6:12]
        pkt_dst_mac = eth.pack_hdr()[:6]
        if pkt_src_mac == local_mac:  # 如果是本机发出的
            pass
        elif eth.pack_hdr()[-2:] == PPPoE_DISCOVERY:  # 用isinstance判断不了PPPoE Discovery包
            pppoe = dpkt.pppoe.PPPoE(eth.data)
            if pppoe.pack_hdr()[1] == PPPoE_PADI:
                print "get padi"
                dst_mac = pkt_src_mac
                sock.send(dst_mac + local_mac + PPPoE_DISCOVERY + PACKAGE_PADO)
            elif pppoe.pack_hdr()[1] == PPPoE_PADR:
                print "get padr"
                dst_mac = pkt_src_mac
                sock.send(dst_mac + local_mac + PPPoE_DISCOVERY + PACKAGE_PADS)
        elif eth.pack_hdr()[-2:] == PPPoE_SESSION:
            pppoe = dpkt.pppoe.PPPoE(eth.data)
            if pppoe.pack_hdr()[1] == PPPoE_SESSION:
                print "get ppp"
                ppp=dpkt.pppoe.PPP(pppoe.data)
                print ppp.pack_hdr().encode("hex")
                if ppp.pack_hdr() == PPP_LCP:
                    pass


if __name__ == '__main__':
    start("lo")
