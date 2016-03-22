#!/usr/bin/python2
# -*- coding: utf-8 -*-
__author__ = 'rl'
import sys
import cPickle as pickle
import os, fnmatch
import commands
#parameters file and directory for cpickle file
picklefile = 'datarelay.pic'
pickledir = '/sensmon/cpickle'
#arguments for execution for each medium
relayslist = (0,1,2,3,4,5)
#gpio commands and rain status
cmd_gpio1 = '/usr/bin/gpio -g read 2'
cmd_gpio2 = '/usr/bin/gpio -g read 3'
cmd_rain_status = '[[ ! -f /run/lock/rain.flg ]];echo $?'
#check if datarelay.pic file exists and get_data is avaliable and proper amount of arguments are given
total = len(sys.argv)
cmdargs = str(sys.argv)
#test if errors not occured if yes nothing will be displayed

try: 
    
    if total >2 or total == 1:
        #print ("Error the total numbers no arg passed to the script: %d " % (int(total) -1))
        argpass = []
        pass 
    elif (int(sys.argv[1])) in relayslist:
        argpass = int(sys.argv[1])
    else:
        argpass = []
except ValueError:  
    argpass = []
    pass
#function for checking if relays gpio status and rain lock file exist 
def checkrelays(arg=argpass):

    try: 
        if arg == 0:
            return commands.getoutput(cmd_gpio1)
        elif arg == 1:
            return commands.getoutput(cmd_gpio2)
        elif arg == 2:
            try:
                openpicklefileread = open(pickledir + '/' + picklefile, 'rb')
                get_data = pickle.load(openpicklefileread)
                openpicklefileread.close()
                p1 = get_data[0]
                return p1
            except IOError: 
                pass
            except NameError:
                pass
            
        elif arg == 3:
            try:
                openpicklefileread = open(pickledir + '/' + picklefile, 'rb')
                get_data = pickle.load(openpicklefileread)
                openpicklefileread.close()
                p2 = get_data[1]
                return p2
            except IOError: 
                pass
            except NameError:
                pass
        elif arg == 4:
            try:
                openpicklefileread = open(pickledir + '/' + picklefile, 'rb')
                get_data = pickle.load(openpicklefileread)
                openpicklefileread.close()
                p3 = get_data[2]
                return p3
            except IOError: 
                pass
            except NameError:
                pass
        elif arg == 5:
            return commands.getoutput(cmd_rain_status)
        elif arg not in relayslist:
            pass
    except IndexError:
        pass
    except NameError:
        pass
#function for get outside argument and run when script is run from shell
if __name__ == "__main__":
    try:
        if checkrelays(argpass) == None:
            pass
        else:
            print checkrelays(argpass)
    except IndexError:
        pass
   