# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/website/manage.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 1272 bytes
"""Utility module for administrative tasks.

A python script version of Django's command-line utility for
administrative tasks (``django-admin``). Additionally, puts the project
package on ``sys.path`` and defines the ``DJANGO_SETTINGS_MODULE``
variable to point to the jwql ``settings.py`` file.

Generated by ``django-admin startproject`` using Django 2.0.1.

Use
---

    To run the web app server:
    ::

        python manage.py runserver

    To start the interactive shellL:
    ::

        python manage.py shell

    To run tests for all installed apps:
    ::

        python manage.py test

References
----------
For more information please see:
    ``https://docs.djangoproject.com/en/2.0/ref/django-admin/``
"""
import os, sys
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jwql_proj.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?") from exc

    execute_from_command_line(sys.argv)