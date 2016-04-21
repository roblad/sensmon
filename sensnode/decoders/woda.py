#!/usr/bin/python2
# -*- coding: utf-8 -*-
import time
import datetime
import inspect
import simplejson as json
import sys
import os
import cPickle as pickle



def switchoffrelays(arg):
    import commands
    import sys
    import os
    import time
    cmd_relay_off1_arch = 'sudo echo 01010|sudo netcat -c localhost 2000 2>/dev/null;sleep 1'
    cmd_relay_off2_arch = 'sudo echo 01020|sudo netcat -c localhost 2000 2>/dev/null;sleep 1'
    cmd_relay_off3_arch = 'sudo echo 01030|sudo netcat -c localhost 2000 2>/dev/null;sleep 1'
    cmd_relay_off1_deb = 'sudo echo 01010|sudo netcat -C localhost 2000 2>/dev/null;sleep 1'
    cmd_relay_off2_deb = 'sudo echo 01020|sudo netcat -C localhost 2000 2>/dev/null;sleep 1'
    cmd_relay_off3_deb = 'sudo echo 01030|sudo netcat -C localhost 2000 2>/dev/null;sleep 1'
    cmd_remove_flag = 'sudo rm -f /tmp/podlewanie.flg 2>/dev/null'
    try:
        if ((int (time.time()) - int (os.stat('/tmp/podlewanie.flg').st_mtime)) > arg) and ((int(os.path.isfile('/tmp/podlewanie.flg'))) == 1): 
            os.system(cmd_relay_off1_arch)
            os.system(cmd_relay_off2_arch)
            os.system(cmd_relay_off3_arch)
            os.system(cmd_relay_off1_deb)
            os.system(cmd_relay_off2_deb)
            os.system(cmd_relay_off3_deb)
            os.system(cmd_remove_flag)
            print "wylaczono podlewanie czas podlewania przekroczyl %s minut" % arg
        
        
    except OSError:
        print "Aktualnie sie nie podlewa"
        pass



def woda(data):
    """Pomiar:
    - swiatła,
    - wlgotności
    - temperatury
    - ciśnienia
    - stanu baterii
    - napięcia beterii

    >> a = "OK 2 0 0 70 1 242 0 201 38 0 15 17"
    >> raw = a.split(" ")
    >> weathernode(raw, "weathernode")
    '{"name": "weathernode", "temp": "242", "lobat": "0", "humi": "326", "timestamp": 1364553092, "light": "0", "press": "9929", "batvol": "4367"}'
    """
#----------------------------------added for pickle and podlewaczka relays---------------------  
    pickledir = os.path.abspath((os.path.dirname(__file__)) + '/../../cpickle')
    picklefile = 'datarelay.pic'
    openpicklefileread = open(pickledir + '/' + picklefile, 'rb')
    get_data = pickle.load(openpicklefileread)
    openpicklefileread.close()
    picklefilepodlewanie = 'datapodlewanie.pic'
    openpicklefilepodlewanie = open(pickledir + '/' + picklefilepodlewanie, 'rb')
    get_datapdl = pickle.load(openpicklefilepodlewanie)
    openpicklefilepodlewanie.close()
    p1 = get_data[0]
    p2 = get_data[1]
    p3 = get_data[2]
    w1 = get_data[4]
    w2 = get_data[5]
    w3 = get_data[10]
    a = float(data[2]) #deszcz
    b = float(data[3]) #temperatura
    c = float(data[4]) 
    d = float(data[5])#bateria
    e = float(data[6]) #pomiar woda
    switchoffrelays(1800)
    if p1 == 1 or p2 == 1 or p3 == 1 and ((int (time.time()) - int (os.stat('/tmp/podlewanie.flg').st_mtime)) > 10):
        w4 = round((e - get_datapdl),2)
        print "aktualnie sie podlewa stan - front: %s bok: %s taras: %s" % (p1,p2,p3)
    else:
        w4 = 0
    #else:
    #f = float(sensmon.woda_last) #pomiar woda
    #f = int(data[7])
    #g = int(data[8])
    #h = int(data[9])
    #i = int(data[10])
    #j = int(data[11])
    #k = int(data[12])

    #nodeid = str(data[1])

    name = inspect.stack()[0][3] # z nazwy funcji
    timestamp = int(time.mktime(datetime.datetime.now().timetuple())) # czas unixa
    template = ({
        'name':name,
        'batvol': d,
        'deszcz': int(a * 0.01),
        'zzztemp': b,
        'pulse': e,
        'wop': round ((e * 4.53),2),
        'wor': int((float (w1))*100),
        'wos': round(w2,2),
        'ewob': w3,
        'wpod': round(w4,2),
        'wpodz': round((w4 * 4.53),4),
        'timestamp':timestamp

        
         })
        
    """
    print "p1", p1
    print "p1", p2
    print "p1", p3
    print "w4", w4
    print "w4 przetw" ,(round(((e - float(get_datapdl))),4))
    print "wpod" , (round(w4,2))
    print "wpodz", (round(w4 * 4.53),4)
    """
    return  dict((k,v) for (k,v) in template.iteritems())
