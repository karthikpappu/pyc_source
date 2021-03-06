# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/predict-ws.py
# Compiled at: 2018-04-06 11:24:35
# Size of source mod 2**32: 4250 bytes
import os, cherrypy
from jinja2 import Environment
from jinja2 import FileSystemLoader
import json, shutil
from predict import Predict
import util.utils as utils
PARTNER_ID = 'UPF'
PARTNER_WEB = 'http://phi.upf.edu'
ADMIN_NAME = 'Manuel Pastor'
ADMIN_EMAIL = 'manuel.pastor@upf.edu'
BASE_DIR = '/var/tmp/'

class FlamePredict(object):

    @cherrypy.expose
    def index(self):
        rdir = utils.root_path()
        endpoint = [x for x in os.listdir(rdir)]
        env = Environment(loader=(FileSystemLoader('templates')))
        tmpl = env.get_template('index.html')
        return tmpl.render(model_list=endpoint)

    @cherrypy.expose
    def upload(self):
        filename = os.path.basename(cherrypy.request.headers['x-filename'])
        temp_dir = os.path.basename(cherrypy.request.headers['temp-dir'])
        path = BASE_DIR + temp_dir
        os.mkdir(path)
        destination = os.path.join(path, filename)
        with open(destination, 'wb') as (f):
            shutil.copyfileobj(cherrypy.request.body, f)


@cherrypy.expose
class FlamePredictWS(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, ifile, model, version, temp_dir):
        ifile = BASE_DIR + temp_dir + '/' + ifile
        try:
            predict = Predict(ifile, model, version)
            success, results = predict.run()
        except:
            raise cherrypy.HTTPError(500)

        return results


@cherrypy.expose
class FlameInfoWS(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        data = {'provider':PARTNER_ID,  'homepage':PARTNER_WEB, 
         'admin':ADMIN_NAME, 
         'admin_email':ADMIN_EMAIL}
        return json.dumps(data)


@cherrypy.expose
class FlameDirWS(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        rdir = utils.root_path()
        endpoint = [x for x in os.listdir(rdir)]
        return json.dumps(endpoint)


if __name__ == '__main__':
    conf = {'/':{'tools.sessions.on':False, 
      'tools.staticdir.root':os.path.abspath(os.getcwd())}, 
     '/info':{'request.dispatch':cherrypy.dispatch.MethodDispatcher(), 
      'tools.response_headers.on':True, 
      'tools.response_headers.headers':[
       ('Content-Type', 'text/plain')]}, 
     '/dir':{'request.dispatch':cherrypy.dispatch.MethodDispatcher(), 
      'tools.response_headers.on':True, 
      'tools.response_headers.headers':[
       ('Content-Type', 'text/plain')]}, 
     '/predict':{'request.dispatch':cherrypy.dispatch.MethodDispatcher(), 
      'tools.response_headers.on':True, 
      'tools.response_headers.headers':[
       ('Content-Type', 'text/plain')]}, 
     '/static':{'tools.staticdir.on':True, 
      'tools.staticdir.dir':'./public'}, 
     'global':{'server.socket_host':'0.0.0.0', 
      'server.socket_port':8080, 
      'server.thread_pool':8}}
    webapp = FlamePredict()
    webapp.info = FlameInfoWS()
    webapp.dir = FlameDirWS()
    webapp.predict = FlamePredictWS()
    cherrypy.quickstart(webapp, '/', conf)