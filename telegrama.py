#!/usr/bin/python3

import db,core
import asyncio
import sys, getopt
from core import TelegramaManager
def main(argv):
    usersfile = ''
    channelsfile = ''
    help_info = """\
Telegrama v0.1
Usage: telegrama.py -u <USERS_FILE> -c <CHANNELS_FILE>
"""
    try:
        opts, args = getopt.getopt(argv,"hu:c:",["users-file=","channels-file="])
    except getopt.GetoptError:
        print (help_info)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (help_info)
            sys.exit()
        elif opt in ("-u", "--users-file"):
            usersfile = arg
        elif opt in ("-c", "--channels-file"):
            channelsfile = arg
    if(usersfile == '' or channelsfile == ''):
        print (help_info)
        sys.exit()
    tm = TelegramaManager(usersfile,channelsfile)
    tm.generate_channels()
    tm.generate_users()

if __name__ == "__main__":
   main(sys.argv[1:])