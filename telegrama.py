#!/usr/bin/python3

import db,core
import asyncio
import sys, getopt
from core import TelegramaManager
def main(argv):
    usersfile = ''
    channelsfile = ''
    targetgroup = 'hoctest1'
    help_info = """\
Telegrama v0.1
Usage: telegrama.py -u <USERS_FILE> -c <CHANNELS_FILE> -g <TARGET_GROUP>
"""
    try:
        opts, args = getopt.getopt(argv,"hu:c:g:",["users-file=","channels-file=","target-group="])
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
    tm = TelegramaManager(usersfile,channelsfile,targetgroup)
    tm.generate_channels()
    tm.generate_users()
    loop = asyncio.get_event_loop()
 #   loop.run_until_complete(tm.telegrama.explore_channels_and_groups())
    loop.run_until_complete(tm.telegrama.add_all_to_group(targetgroup))
    loop.close()

if __name__ == "__main__":
   main(sys.argv[1:])