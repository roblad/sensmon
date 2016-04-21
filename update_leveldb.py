#!/usr/bin/python2
# -*- coding: utf-8 -*-
import json
import plyvel as leveldb
import os
import sys
import time
db = leveldb.DB("_db", create_if_missing=True)		
wb = db.write_batch()
with open("delete.log") as f:
    wb = db.write_batch(transaction=True)
    for line in f:
        line = line.rstrip('\n')
        value = line.rstrip('\n')
        start_index = (line.find('timestamp'))+12
        stop_index = start_index + 10
        key = "outdoor-%s"%line[start_index:stop_index]
        wb.put(key, value)
        time.sleep(0.005)#type (line)
        #data = json.loads(line.rstrip('\n'))
        #type(data)
        print "insert key: %s "%key + " value: " + value
        if "timestamp" in key:
            break

wb.write()
db.closed
db.close()
db.closed
#snd node
wb = db.write_batch(transaction=True)
with open("gaz_data_node_decoded2.log") as f:
    for line in f:
        line = line.rstrip('\n')
        value = line.rstrip('\n')
        start_index = (line.find('timestamp'))+12
        stop_index = start_index + 10
        key = "gaz-%s"%line[start_index:stop_index]
        wb.put(key, value)
        #type (line)
        #data = json.loads(line.rstrip('\n'))
        #type(data)
        print "insert key: %s "%key + " value: " + value
        if "timestamp" in key:
            break

wb.write()

#delete
#!/usr/bin/python2
# -*- coding: utf-8 -*-
import json
import plyvel as leveldb
import os
import sys

db = leveldb.DB("_db", create_if_missing=True)
wb = db.write_batch(transaction=True)
with open("woda.log") as f:
    for line in f:
        line = line.rstrip('\n')
        value = line.rstrip('\n')
        #start_index = (line.find('timestamp'))+12
        #stop_index = start_index + 10
        #key = "piec-%s"%line[start_index:stop_index]
        key = line
        wb.delete(key)
        print "delete key: ",(key)
        #if "timestamp" in key:
            #break



wb.write()
db.closed
db.close()
db.closed


#dump
#!/usr/bin/python2
# -*- coding: utf-8 -*-
import json
import plyvel as leveldb
import os
import sys

imput ='woda'

db = leveldb.DB("_db", create_if_missing=True)
file = open("/sensmon/"+imput+".log", "w")
test = db.iterator(prefix=imput)
for key, value in test:
    file.write (key)
    file.write (" ")
    file.write (value)
    file.write("\n")

file.close()

#dupa = [value for key, value in test ]
#print dupa ,"\n"

db.closed
db.close()
db.closed

