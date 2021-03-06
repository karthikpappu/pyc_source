# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/modules/example_module.py
# Compiled at: 2016-12-29 01:51:56


class CMEModule:
    """
        Example
        Module by @yomama

    """
    name = 'example module'
    description = 'Something Something'

    def options(self, context, module_options):
        """Required. Module options get parsed here. Additionally, put the modules usage here as well"""
        pass

    def on_login(self, context, connection):
        """Concurrent. Required if on_admin_login is not present. This gets called on each authenticated connection"""
        pass

    def on_admin_login(self, context, connection):
        """Concurrent. Required if on_login is not present. This gets called on each authenticated connection with Administrative privileges"""
        pass

    def on_request(self, context, request):
        """Optional. If the payload needs to retrieve additonal files, add this function to the module"""
        pass

    def on_response(self, context, response):
        """Optional. If the payload sends back its output to our server, add this function to the module to handle its output"""
        pass