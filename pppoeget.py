# -*- coding: utf8 -*-
import pcap,dpkt

def get_pap_information(data):
    pap_type=data[0]
    pap_username_len=bytearray(list(data[4]))[0]
    pap_username=data[5:5+pap_username_len]
    pap_password_len=bytearray(list(data[5+pap_username_len]))[0]
    pap_password=data[6+pap_username_len:6+pap_username_len+pap_password_len]
    return dict(type=pap_type,username=pap_username,password=pap_password)


def get_config(card="eth0"):
    pap=None
    sniffer=pcap.pcap(name=card,immediate=True)
    for ts,pkt in sniffer:
        eth=dpkt.ethernet.Ethernet(pkt)
        if isinstance(eth.data,dpkt.pppoe.PPPoE): #判断是否为PPPoE数据包
            pppoe=eth.data  #拆包
            if isinstance(pppoe.data,dpkt.pppoe.PPP): #判断是否为PPP包
                ppp=pppoe.data #拆包
                if ppp.pack_hdr()==b"\xc0\x23": #PPP PAP包的头
                    if ppp.data[0]==b"\x01": #类别为Authenticate-Request
                        pap=get_pap_information(ppp.data)
                        break
    return pap