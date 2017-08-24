# -*- coding: utf8 -*-
import sys, getopt, logging


def get_config():
    short_opts = "hL:S:"
    config = dict(listen="", server="")
    try:
        optlist, args = getopt.getopt(sys.argv[1:], shortopts=short_opts)
    except getopt.GetoptError as error:
        logging.error(error)
        print_usage()
        sys.exit(1)
    for o, v in optlist:
        if o == "-h":
            print_usage()
            sys.exit(0)
        elif o == "-L":
            config["listen"] = v
        elif o == "-S":
            config["server"] = v
    for i in config:
        if config[i] == "":
            logging.error("Please specify dial value")
            print_usage()
            sys.exit(1)
    return config


def print_usage():
    usage = """
    -L  <interface>              The card you want to listen dial
    -S  <interface>              The card you want to make a dial
    -h                           Print this help
    """
    print(usage)
