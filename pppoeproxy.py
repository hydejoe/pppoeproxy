# -*- coding: utf8 -*-
import pppoeget, shell, template
import subprocess,os

def check():
    if os.getuid()!=0:
        print "Must run as root"
        raise Exception
    # For the first time
    if not os.path.exists("/etc/ppp/pppoe-server-options"):
        template.write_conf(template.pppoe_server_options,"/etc/ppp/pppoe-server-options")
    if not os.path.exists("/etc/ppp/pap-secrets"):
        template.update_conf("eth0","temp_username","temp_password")
        ret=subprocess.check_call(["chmod","go-rwx","/etc/ppp/pap-secrects"])

def run():
    config = shell.get_config()
    try:
        ret = subprocess.check_call(["pppoe-server", "-I", config["listen"]])
        pap = pppoeget.get_config(config["listen"])
        ret = subprocess.check_call(["killall", "pppoe-server"])
        template.update_conf(config["server"], pap["username"], pap["password"])
        ret = subprocess.check_call("/usr/sbin/pppoe-start")
    except:
        ret = subprocess.call(["killall", "pppoe-server"])


if __name__ == '__main__':
    run()
