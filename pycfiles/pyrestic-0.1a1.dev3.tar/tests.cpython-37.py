# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/tests.py
# Compiled at: 2019-03-15 23:50:48
# Size of source mod 2**32: 2709 bytes
from pyrestful.rest import get, post, RestHandler, RestService
from tornado.testing import AsyncHTTPTestCase
import json

class Book:
    title = str


class Person:
    idperson = int
    name = str
    books = Book


class service(RestHandler):

    @get('/person', {'format': 'xml'}, _catch_fire=True)
    def get_person(self):
        book = Book()
        book.title = 'Life'
        person = Person()
        person.idperson = 1
        person.name = 'Rodrigo'
        person.books = book
        return person

    @get('/echo/{value}')
    def echo(self, value):
        return value

    @get('/data/{name}', {'format': 'json'})
    def get_json(self, name):
        return {'name': name}

    @post('/data', {'format': 'json'})
    def post_json(self, data):
        return data

    @get('/book/{isbn}', {'produces': 'application/json'})
    def get_book(self, isbn):
        return {'title':'The Quick Python Book', 
         'isbn':isbn}

    @post('/book', {'consumes': 'application/json'})
    def post_book(self, data):
        return 'Book Ok'


class TestService(AsyncHTTPTestCase):

    def get_app(self):
        return RestService([service])

    def test_get_string(self):
        response = self.fetch('/echo/TEST')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'TEST')

    def test_get_json(self):
        response = self.fetch('/data/tornado')
        response_json = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertDictEqual(response_json, {'name': 'tornado'})
        self.assertEqual(response_json['name'], 'tornado')

    def test_post_json(self):
        response = self.fetch('/data', method='POST', body=(json.dumps({'id': 123456})), headers={'content-type': 'application/json'})
        response_json = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertDictEqual(response_json, {'id': 123456})

    def test_get_book(self):
        response = self.fetch('/book/978-1617294037')
        response_json = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertIn('Python', response_json['title'])
        self.assertEqual(response_json['isbn'], '978-1617294037')

    def test_post_book(self):
        book = {'isbn':'978-1617294037', 
         'title':'The Quick Python Book'}
        response = self.fetch('/book', method='POST', body=(json.dumps(book)), headers={'content-type': 'application/json'})
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'Book Ok')

    def test_get_person(self):
        response = self.fetch('/person')
        person = response.body
        print(person)
        self.assertEqual(response.code, 200)