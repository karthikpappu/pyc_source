# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/amundsen_common/log/http_header_caller_retrieval.py
# Compiled at: 2020-02-13 16:36:56
# Size of source mod 2**32: 402 bytes
from flask import current_app as flask_app
from flask import request
from amundsen_common.log.caller_retrieval import BaseCallerRetriever
CALLER_HEADER_KEY = 'CALLER_HEADER_KEY'

class HttpHeaderCallerRetrieval(BaseCallerRetriever):

    def get_caller(self) -> str:
        header_key = flask_app.config.get(CALLER_HEADER_KEY, 'user-agent')
        return request.headers.get(header_key, 'UNKNOWN')