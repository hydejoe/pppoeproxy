# -*- coding: utf8 -*-
import pppoeget,shell,template
import subprocess

def run():
    config=shell.get_config()
    try:
        ret=subprocess.check_call(["pppoe-server","-I",config["listen"]])
        pap=pppoeget.get_config(config["listen"])
        template.write_conf(config["server"],pap["username"],pap["password"])
        ret=subprocess.check_call("/usr/sbin/pppoe-start")
        ret=subprocess.check_call(["systemctl","restart","dnsmasq"])
    finally:
        ret=subprocess.check_call(["killall","pppoe-server"])

if __name__ == '__main__':
    run()