# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/threebean/devel/busmon/busmon/controllers/error.py
# Compiled at: 2012-10-04 13:49:55
__doc__ = 'Error controller'
from tg import request, expose
__all__ = [
 'ErrorController']

class ErrorController(object):
    """
    Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """

    @expose('busmon.templates.error')
    def document(self, *args, **kwargs):
        """Render the error document"""
        resp = request.environ.get('pylons.original_response')
        default_message = "<p>We're sorry but we weren't able to process  this request.</p>"
        values = dict(prefix=request.environ.get('SCRIPT_NAME', ''), code=request.params.get('code', resp.status_int), message=request.params.get('message', default_message))
        return values