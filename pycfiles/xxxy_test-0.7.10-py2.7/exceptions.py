# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/exceptions.py
# Compiled at: 2018-12-27 05:19:41
from click import ClickException

class RussellException(ClickException):

    def __init__(self, message=None, code=None):
        super(RussellException, self).__init__(message)


class AuthenticationException(ClickException):

    def __init__(self, message='Authentication failed. Retry by invoking russell login.'):
        super(AuthenticationException, self).__init__(message=message)


class NotFoundException(ClickException):

    def __init__(self, message='The resource you are looking for is not found. Check if the id/path is correct.'):
        super(NotFoundException, self).__init__(message=message)


class BadRequestException(ClickException):

    def __init__(self, message='One or more request parameter is incorrect.'):
        super(BadRequestException, self).__init__(message=message)


class NoRequestException(ClickException):

    def __init__(self, message='Request parameter is not found'):
        super(NoRequestException, self).__init__(message=message)


class OverLimitException(ClickException):

    def __init__(self, message='You are over the allowed limits for this operation. Consider upgrading your account.'):
        super(OverLimitException, self).__init__(message=message)


class InvalidResponseException(ClickException):

    def __init__(self, message='Authentication failed. Retry by invoking russell login.'):
        super(InvalidResponseException, self).__init__(message=message)


class ExistedException(ClickException):

    def __init__(self, message='Directory/File Existed. Retry by changing name.'):
        super(ExistedException, self).__init__(message=message)


class OverPermissionException(ClickException):

    def __init__(self, message="You are over the allowed permission for this operation. Maybe you should not visit other's private resource."):
        super(OverPermissionException, self).__init__(message=message)


class VersionTooOldException(ClickException):

    def __init__(self, message='Your local version is too old. Please try to clone the latest verion project.'):
        super(VersionTooOldException, self).__init__(message=message)


class NoBalanceException(ClickException):

    def __init__(self, message='You have no enough balance to run this task. Consider recharge your account or upgrading your account.'):
        super(NoBalanceException, self).__init__(message=message)


class DuplicateException(ClickException):

    def __init__(self, message='The name does exited on remote. Please change the name and retry'):
        super(DuplicateException, self).__init__(message=message)


class TaskSubmitException(ClickException):

    def __init__(self, message='Task is submitted failed. Please retry after a while or contact the development team via contact@russellcloud.cn'):
        super(TaskSubmitException, self).__init__(message=message)


class ServiceBusyException(ClickException):

    def __init__(self, message='Service is busy right now. Please retry after a while or contact the development team via contact@russellcloud.cn'):
        super(ServiceBusyException, self).__init__(message=message)


class ResourceUnavailableException(ClickException):

    def __init__(self, message='The resource is unavailable right now. Please retry after a while or contact the development team via contact@russellcloud.cn'):
        super(ResourceUnavailableException, self).__init__(message=message)


class OverSizeException(ClickException):

    def __init__(self, message='Upload file size exceeds limit. Data upload max size is 20GB and project upload max size is 100MB.'):
        super(OverSizeException, self).__init__(message=message)


class ResumeInvalidException(ClickException):

    def __init__(self, message="Resume upload failed. Server can't find temp file."):
        super(ResumeInvalidException, self).__init__(message=message)