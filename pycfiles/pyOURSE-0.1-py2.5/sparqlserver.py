# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mahound/projects/ourse/ourse/sparqlserver.py
# Compiled at: 2008-04-04 14:25:58
from cgi import parse_qs

class SPARQLEndPoint:

    def __init__(self, regExp):
        self.__regExp = regExp

    def getRegExp(self):
        return self.__regExp

    def requestHandler(self, ourseInstance, bindings, environ):
        parameters = parse_qs(environ.get('QUERY_STRING', ''))
        qtext = parameters.get('query', None)
        format = parameters.get('format', None)
        if not qtext:
            return ('text/plain', 'No query specified...')
        if not format:
            format = 'json'
        else:
            format = format[0]
        if format not in ('xml', 'json'):
            return (
             'text/plain', 'Format %s is not known...' % format)
        return self.sparqlRequestHandler(ourseInstance, qtext[0], format)

    def sparqlRequestHandler(self, ourseInstance, qtext, format):
        g = ourseInstance.getConjunctiveGraph()
        try:
            r = g.query(qtext)
            result = r.serialize(format=format)
            result = result.encode('utf-8')
            if format == 'json':
                mimeType = 'application/json'
            elif format == 'xml':
                mimeType = 'text/xml'
            return (format, result)
        except Exception, e:
            return (
             'text/plain', str(qtext) + '\n\n' + str(e))