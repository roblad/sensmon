#!/usr/bin/python2
# -*- coding: utf-8 -*-

debug = True  # tryb developerski
version = '0.41-dev'
global woda_last
import time
import os
import logging
from datetime import date

# https://github.com/leporo/tornado-redis
import tornadoredis
import paho.mqtt.publish as mqtt

import simplejson as json
# http://pymotw.com/2/multiprocessing
import multiprocessing

import tornado.ioloop
import tornado.web
import tornado.template
import tornado.websocket
import tornado.gen
import tornado.httpserver
import tornado.escape
import tornado.autoreload
from tornado.options import define, options

# sesnode engine
import sensnode.store
import sensnode.decoder
import sensnode.connect
import sensnode.common
import sensnode.logs as logs
from sensnode.config import config
from sensnode.weather import getWeather
#from sensnode.weather import getAQI - removed not neded
#added for additional functions
import sys
import cPickle as pickle
import redis
from sensnode.getrelays import checkrelays
#import sensnode.parse 




# inicjalizacja menadżera konfiguracji
ci = config(init=True)

# ------------------------webapp settings--------------------#
define("webapp_port",default=config().get("app", ['webapp', 'port']),
		help="Run on the given port", type=int)
define("webapp_host",default=sensnode.common.get_ip_address(config().get("app", ['webapp', 'iface'])),
        help="Run on the given hostname")
# leveldb
define("leveldb_enable",default=config().get("app", ['leveldb', 'enable']),
		help="LevelDB enabled")
define("leveldb_dbname",default=config().get("app", ['leveldb', 'dbname']),
		help="LevelDB database name")
define("leveldb_path",default=config().get("app", ['leveldb', 'path']),
		help="LevelDB path do database")
define("leveldb_forgot",default=config().get("app", ['leveldb', 'forgot']),
        help="Forgot nodes data")
# MQTT
define("mqtt_enable",default=config().get("app", ['mqtt', 'enable']),
		help="MQTT enabled")
define("mqtt_broker",default=config().get("app", ['mqtt', 'broker']),
		help="MQTT broker IP")
define("mqtt_port",default=config().get("app", ['mqtt', 'port']),
		help="MQTT broker port")
# ----------------------end webapp settings------------------#

# klient Redis
c = tornadoredis.Client()
c.connect()
clients = []

history = sensnode.store.history(options.leveldb_path, options.leveldb_dbname)



# --------------------------webapp code-----------------------#


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user")


# wylogowywanie
class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        # self.redirect("/")
        self.redirect(self.get_argument("next", "/"))


# logowanie
class LoginHandler(BaseHandler):

    def get(self):
        self.render("login.tpl", resp=None)

    def post(self):
        username = self.get_argument('name', '')
        password = self.get_argument('pass', '')
        print username, password

        settings_pass = config().get("app", ['webapp', 'password'])

        # logowanie - FIXME
        if not password:
            login_response = {
                'msg': 'Wpisz haslo.'
            }
            self.render("login.tpl", resp=login_response)
        elif not username:
            login_response = {
                'msg': 'Wpisz login.'
            }
            self.render("login.tpl", resp=login_response)
        elif username == 'admin' and password == settings_pass:
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect(self.get_argument("next", "/"))
        else:
            login_response = {
                'msg': 'Zły login i hasło!'
            }
            self.render("login.tpl", resp=login_response)


# zakładka Home
class HomeHandler(BaseHandler):

    def get(self):
        self.render("home.tpl")


# panel administatora
class AdminHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("admin.tpl")


# zakładka Wykresy
class GraphsHandler(BaseHandler):

    def get(self, node, sensor, timerange):
        self.render("graphs.tpl")


# zakładka Dashboard
class DashHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        c = tornadoredis.Client()
        res = yield tornado.gen.Task(c.get, 'initv')
        self.render("dash.tpl")


# zakładka Sterowanie
class ControlHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def get(self):
        c = tornadoredis.Client()
        res = yield tornado.gen.Task(c.hvals, 'status')
        self.render("control.tpl",
                    init=[json.loads(x) for x in res])


# zakłatka Logi
class LogsHandler(BaseHandler):

    def get(self):
        self.render("logs.tpl")


# zakłatka Intro
class IntroHandler(BaseHandler):

    def get(self):
        weather = getWeather(city='Stanislawow Pierwszy')
        #aqi = getAQI()
        #self.render("intro.tpl", w=weather,aqi=aqi)
        self.render("intro.tpl", w=weather)


# zakładka System
class InfoHandler(BaseHandler):

    def get(self):
        self.render("info.tpl",
                    arch=sensnode.common.this_mach(),
                    system=sensnode.common.this_system(),
                    lavg=sensnode.common.loadavg(),
                    uptime=sensnode.common.uptime(),
                    cpu_temp=sensnode.common.cpu_temp(),
                    process=sensnode.common.process(),
                    disksize=sensnode.common.disksize(),
                    machine=sensnode.common.machine_detect()[0],
                    usbrelay_status=sensnode.common.usbrelay(),
                    wheather_status=sensnode.common.wheather_control()
                    )


# RESTful
# history/<node>/<sensor>/<timerange>
class GetHistoryData(BaseHandler):

    def get(self, node, sensor, timerange):
        self.set_header("Content-Type", "application/json")
        response = []

        try:
            response = { 'data' :  history.get_toJSON(node, sensor, timerange) }
            self.write(response)
            self.finish()
        except KeyError, e:
            self.set_status(404)
            self.finish("%s nie znaleziono" % e)
        

class GetInitData(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.set_header("Content-Type", "application/json")
        _cl = tornadoredis.Client()
        _initv = yield tornado.gen.Task(_cl.get, 'initv')
        data_json = tornado.escape.json_encode(_initv)
        self.write(data_json)
        self.finish()


# Websocket
class Websocket(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super(Websocket, self).__init__(*args, **kwargs)
        self.listen()

    @tornado.web.asynchronous
    @tornado.gen.engine
    def listen(self):
        self.client = tornadoredis.Client()
        self.client.connect()
        yield tornado.gen.Task(self.client.subscribe, 'nodes')
        self.client.listen(self.sendmsg)

    def allow_draft76(self):
        # dla WebOS & iOS
        return True

    def open(self):
        print "WebSocket opened"

    """Wyślij wiadomość do klienta"""
    def sendmsg(self, msg):
        if hasattr(msg, "body"):
            self.write_message(str(msg.body))

    """Odbierz wiadomość od klienta"""
    def on_message(self, msg):
        rdb = sensnode.store.redisdb()
        # zapisz status w bazie redis
        rdb.setStatus(msg)
        # wrzuć w kolejkę
        q = self.application.settings.get('queue')
        q.put(msg)
        self.write_message('{"control":"You send: %s"}' % (
            json.loads(str(msg))))

    def on_close(self):
        if self.client.subscribed:
            print "WebSocket closed"
            self.client.unsubscribe('nodes')
            self.client.disconnect()


def publish(jsondata):
    """
    >> data = {'vrms': 220.39, 'timestamp': 1428338500, 'name': 'powernode', 'power': 246}
    >> publish(data, hostname="localhost" port="1883")
    /powernode/vrms 220.39
    /powernode/power 246
    /powernode/timestamp 1428338500
    """
    name = jsondata['name']
    for k, v in jsondata.iteritems():
        mqtt.single("/sensmon/%s/%s" % (name, k), v, hostname=options.mqtt_broker, port=options.mqtt_port)


    





def setValue(val):
    global globalVal
    valueChanged = val != val
    if valueChanged:
        print "pre zmienilo sie"
    globalVal = val
    if valueChanged:
        print "post zmienilo sie"

# funkcja główna
def main():
    taskQ = multiprocessing.Queue()
    resultQ = multiprocessing.Queue()

    connect = sensnode.connect.Connect(taskQ, resultQ, debug=debug)
    connect.daemon = True
    connect.start()

    redisdb = sensnode.store.redisdb(debug=debug)
    decoder = sensnode.decoder.Decoder(debug=debug)

    logger = logging.getLogger()

    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/admin", AdminHandler),
        #(r"/control", ControlHandler),
        (r"/", DashHandler),
        (r"/graphs/(?P<node>[^\/]+)/?(?P<sensor>[^\/]+)?/?(?P<timerange>[^\/]+)?", GraphsHandler),
        (r"/info", InfoHandler),
        (r"/intro", IntroHandler),
        (r"/logs", LogsHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/initv", GetInitData),
        (r"/history/(?P<node>[^\/]+)/?(?P<sensor>[^\/]+)?/?(?P<timerange>[^\/]+)?", GetHistoryData),
        (r"/websocket", Websocket),
        (r'/favicon.ico', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "static")})],
        queue=taskQ,
        template_path=os.path.join(os.path.dirname(__file__), "views"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        login_url="/login",
        debug=True)

    httpServer = tornado.httpserver.HTTPServer(application)
    httpServer.listen(options.webapp_port)
    print "sensmon %s started at %s port" % (version, options.webapp_port)
    print "Przejdz na stronę http://%s:%s" % (options.webapp_host, options.webapp_port)
    @tornado.gen.engine
    
    
    def checkResults():

        if not resultQ.empty():
            # suwówka
            result = resultQ.get()
            # dane zdekodowane
            decoded = decoder.decode(result)
            # dane zdekodowane + odczyty

            try: 
                node_name = decoded['name']
            except TypeError:
                return
            update = decoder.update(decoded)
            
#----------------------------------tu  pisac swoje razem z importem na poczatku ---------------------             
            #removed ater change of usbrelay check throug python script 22.03.16
            #dir_current = os.getcwd()
            ######if not node_name.empty():
            #print "Current directory for store data file result is: /mnt/data/ "
            #used for dump data from leveldb
            #if str(decoded) != 'None' and (decoded['name']) == 'woda':
                #filer = "/mnt/data/"+(decoded['name']+"_data_node.log"
                #with open('filer', 'r+') as f:
                #file = open("/mnt/data/"+(decoded['name'])+"_data_node.log", "w")
                #print history.pritndb((decoded['name']))
                #file.write(dane)
                #file.write("\n")
                #file.close()
                #file2 = open("/mnt/data/"+(decoded['name'])+"_data_node_decoded.log", "a+")
                #file2.write (str(decoded))
                #file2.write("\n")
                #file2.close()
#----------------------------------tu  pisac swoje razem z importem na poczatku ---------------------                  
            if debug:
                print ("RAW: %s" % (result))
                print ("JSON %s" % (decoded))
                #print ("UPD %s" % (update))
                    
                    
                    
            # leveldb włączone?
            if options.leveldb_enable:
                if decoded['name'] not in options.leveldb_forgot:
                    key = ('%s-%d' %  (decoded['name'], decoded['timestamp'])).encode('ascii')
                    value = ('%s' % decoded).encode('ascii')
                    history.put(key, value)
                    
                    if debug:
                        logger.debug("LevelDB: %s %s" % (key, decoded))
                        #print ("LevelDB: %s %s" % (key, decoded))
                        
                        

            # dane tymczasowe - initv
            redisdb.pubsub(update)
            for c in clients:
                c.write_message(update)
            

            # MQTT włączone?
            if options.mqtt_enable:
                publish(decoded)

#----------------------------------tu  pisac swoje dodatkowe funkcjonalnosci start ---------------------  
            try:
                woda_last = round((history.get_toJSON_last( 'woda', 'pulse','day')[0]),2)
                woda_first = round((history.get_toJSON_last( 'woda', 'pulse','day')[-1]),2)
                cena_woda_last = round((history.get_toJSON_last( 'woda', 'wop','day')[0]),2)
                cena_woda_first = round((history.get_toJSON_last( 'woda', 'wop','day')[-1]),2)
                gaz_last = round((history.get_toJSON_last( 'gaz', 'pulse','day')[0]),2)
                gaz_first = round((history.get_toJSON_last( 'gaz', 'pulse','day')[-1]),2)
                cena_gaz_last = round((history.get_toJSON_last( 'gaz', 'zuzycieoplata','day')[0]),2)
                cena_gaz_first = round((history.get_toJSON_last( 'gaz', 'zuzycieoplata','day')[-1]),2)
                furtka_state = int(checkrelays(0))
                brama_state = int(checkrelays(1))
                podlewanie_blokada = int(checkrelays(5))
                p1 = history.get_toJSON_last( 'piec', 'trela1','1h')[0]
                p2 = history.get_toJSON_last( 'piec', 'trela2','1h')[0]
                p3 = history.get_toJSON_last( 'piec', 'trela3','1h')[0]
                pickledir = os.path.abspath((os.path.dirname(__file__)) + '/cpickle')
                picklefile = 'datarelay.pic'
                #sensnode.parse.test_values('piec','trela1')
                #sensnode.parse.test_values('piec','trela2')
                #sensnode.parse.test_values('piec','trela3') 
                #sensnode.parse.test_values('woda','pulse') 
                store = (p1,
                         p2,
                         p3,
                         woda_last,
                         round((woda_last - woda_first),2),
                         round((cena_woda_last - cena_woda_first),2),
                         round((gaz_last - gaz_first),2),
                         round((cena_gaz_last - cena_gaz_first),2),
                         furtka_state, 
                         brama_state,
                         podlewanie_blokada)
                openpicklefilewrite = open(pickledir + '/' + picklefile, 'wb')
                pickle.dump(store, openpicklefilewrite,-1 )
                openpicklefilewrite.close()
                if os.path.isfile('/tmp/relaystart.flg'):
                    picklefilepodlewanie = 'datapodlewanie.pic'
                    openpicklefilepodlewanie = open(pickledir + '/' + picklefilepodlewanie, 'wb')
                    woda_last_podl=woda_last
                    pickle.dump(woda_last, openpicklefilepodlewanie,-1 )
                    openpicklefilepodlewanie.close()
                    os.remove('/tmp/relaystart.flg')

                if debug:
                    print pickledir 
                    print "trela1 :" , p1
                    print "trela2 :" , p2
                    print "trela3 :" , p3
                    print "Woda ostatnia wartość: " , woda_last
                    print "ostatnia wartosc dziennego zuzycia wody: %s litrów" % int((woda_last - woda_first) * 1000)
                    print "opłata dziennego zuzycia wody: %s zł" % (cena_woda_last - cena_woda_first)
                    print "ostatnia wartosc dziennego zuzycia gazu: %s m3" % (gaz_last - gaz_first)
                    print "opłata dziennego zuzycia gazu: %s zł" % (cena_gaz_last - cena_gaz_first)
                    try:
                        picklefilepodlewanie = 'datapodlewanie.pic'
                        openpicklefilepodlewanie = open(pickledir + '/' + picklefilepodlewanie, 'rb')
                        get_datapdl = pickle.load(openpicklefilepodlewanie)
                        openpicklefilepodlewanie.close()
                        print "wartosc wody pobrana do obliczania podlewania: %s m3" % get_datapdl
                    except UnboundLocalError:
                        print "wartosc wody pobrana do obliczania podlewania: %s m3" % 0
            except   ValueError:
                pass
            except IndexError:
                pass
                
#-------------------tu  pisac swoje koniec --------------------- 
    

    mainLoop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(mainLoop)
    scheduler = tornado.ioloop.PeriodicCallback(
        checkResults, 300, io_loop=mainLoop)


    
    scheduler.start()
    mainLoop.start()  

if __name__ == "__main__":
    main()
