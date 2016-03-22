# -*- coding: utf-8
import os
import subprocess
import redis
import simplejson as jsons
#import sensmon
#import sensnode.store
import cPickle as pickle



  
def test_values(nodename,value): #test database temporary if values came
#print 'Decoding JSON has failed value set to:' ,woda_actual
# i.e. node name is woda and tested value is pulse



    try:
        test = jsons.loads((redis.Redis("localhost", 6379)).get("initv"))[nodename]['sensors'][value]['raw']
        #test = json[nodename]['sensors'][value]['raw'] # woda
        return test
    except KeyError:  # includes simplejson.decoder.JSONDecodeError
        test = None
        return test

def checkValue(val):
    global globalVal
    valueChanged = val != val
    print valueChanged
    print val
    
    if valueChanged:
        print "pre :" , p1
    globalVal = val
    print globalVal
    if valueChanged:
        print "post :" , p1
        
#test if values are avaliable
if test_values('woda','pulse') == "error" or test_values('piec','trela1') == "error" or test_values('piec','trela2') == "error" or test_values('piec','trela3') == "error" :
    p1 = test_values('piec','trela1')
    p2 = test_values('piec','trela2')
    p3 = test_values('piec','trela3') 
    w1 = test_values('woda','pulse') 
    print "trela1 :" , p1
    print "trela2 :" , p2
    print "trela3 :" , p3
    print "Podlewaczka : " , w1
else: #values avaliable
    p1 = test_values('piec','trela1')
    p2 = test_values('piec','trela2')
    p3 = test_values('piec','trela3') 
    w1 = test_values('woda','pulse')     
    print "Value podlewaczka : " , w1
    print "trela1 :" , p1
    print "trela2 :" , p2
    print "trela3 :" , p3
store = p1,p2,p3,w1

pickledir = os.path.abspath((os.path.dirname(__file__)) + '/../cpickle')
picklefile = 'datarelay.pic'
#openpicklefilewrite = open(pickledir + '/' + picklefile, 'w')
openpicklefileread = open(pickledir + '/' + picklefile, 'rb')
#print pickledir 
#pickle.dump(store, openpicklefilewrite )
#openpicklefilewrite.close()
#a, b, c, d =  pickle.load(openpicklefileread)
#openpicklefileread.close()
dupa =  pickle.load(openpicklefileread)
openpicklefileread.close()
#dupa = a, b, c, d
print dupa
print checkValue(p1)



###################### TEMP #########################################################

#rdb = redis.Redis("localhost", 6379) # connect to redis database
#raw = rdb.get("initv") # get tempdatabase values in redis database
#json = jsons.loads(raw) # data taken in JSON format

#os.system('mpc clear')
#os.system('ls')
#cmd = subprocess.Popen("ls",shell=True, stdout=subprocess.STDOUT)
#stations = cmd.stdout.readlines()[0][1::3]
#print stations

#inputfile = "/mnt/data/woda_podlewanie.log"
#dat_file = open(inputfile, 'rb')
#line_from_woda_used =  dat_file.readlines()    
#last_line = line_from_woda_used[-1].strip()
#woda_start_podlewaczka = os.environ.get('WODA_START',0)



#print "variable woda - count current value of used water: ", woda_used_by_podlewaczka
    #print "last line from last value of podlewaczka : ", last_line

#if not "WODA_START" in os.environ or woda_start_podlewaczka == "" or woda_start_podlewaczka <= last_line:
    #woda_used_by_podlewaczka = 0
    #woda_actual == 0
    
#woda_used_by_podlewaczka = round ((float ((float (woda_start_podlewaczka)) - float(last_line))),2)