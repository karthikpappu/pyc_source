# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/sciroccoclient/exceptions.py
# Compiled at: 2016-11-22 16:46:46
# Size of source mod 2**32: 2830 bytes


class SciroccoError(Exception):

    def __init__(self, message):
        super(Exception, self).__init__(message)


class SciroccoRequestAdapterError(SciroccoError):
    __doc__ = ' Raised when theres some problem at request low level. Probably the request manager aka urllib3 changed its behaviour\n        or something else.\n    '

    def __init__(self, message):
        super(SciroccoRequestAdapterError, self).__init__(message)


class SciroccoInitParamsError(SciroccoError):
    __doc__ = '\n        Raised when theres a problem with initial parameters, token , server url .\n    '

    def __init__(self):
        message = 'You must init your connection to scirocco server with three positional arguments, host, node_id and auth_token.'
        super(SciroccoInitParamsError, self).__init__(message)


class SciroccoHTTPDAOError(SciroccoError):
    __doc__ = '\n        Raised when thers an unexpected result in DAO layer.\n    '

    def __init__(self, message):
        message = ''.join(['HTTPDAO received an unexpected status code ', str(message)])
        super(SciroccoHTTPDAOError, self).__init__(message)


class SciroccoInvalidMessageScheduleTimeError(SciroccoError):

    def __init__(self):
        message = 'The message schedule time param must be an datetime instance.'
        super(SciroccoInvalidMessageScheduleTimeError, self).__init__(message)


class SciroccoInvalidMessageError(SciroccoError):

    def __init__(self):
        message = 'The message param must be an instance of SciroccoMessage.'
        super(SciroccoInvalidMessageError, self).__init__(message)


class SciroccoInvalidMessageDataError(SciroccoError):
    __doc__ = '\n        Raised when try tu push and emtpy message.\n    '

    def __init__(self):
        message = 'The message data cannot be empty.'
        super(SciroccoInvalidMessageDataError, self).__init__(message)


class SciroccoInvalidMessageDestinationError(SciroccoError):

    def __init__(self):
        message = 'The message destination data cannot be empty.'
        super(SciroccoInvalidMessageDestinationError, self).__init__(message)


class SciroccoInvalidMessageStatusError(SciroccoError):

    def __init__(self):
        message = "The message status must be 'pending' or 'scheduled' ."
        super(SciroccoInvalidMessageStatusError, self).__init__(message)


class SciroccoInvalidOnReceiveCallBackError(SciroccoError):
    __doc__ = '\n    The callbackfunction provided by user its not valid\n    '

    def __init__(self, message):
        super(SciroccoInvalidOnReceiveCallBackError, self).__init__(message)


class SciroccoInterruptOnReceiveCallbackError(SciroccoError):
    __doc__ = '\n    Raised by user custom callback. Its intended to stop the consumer thread gracefully.\n    '

    def __init__(self, message):
        super(SciroccoInterruptOnReceiveCallbackError, self).__init__(message)