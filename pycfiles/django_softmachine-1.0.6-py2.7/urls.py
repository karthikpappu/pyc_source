# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/urls.py
# Compiled at: 2014-06-23 11:39:29
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from protoLib.utils.generic_views import DirectTemplateView
from protoLib.protoMenu import protoGetMenuData
from protoLib.protoGetPci import protoGetPCI, protoSaveProtoObj, protoGetFieldTree, getFieldIncrement
from protoLib.protoGetDetails import protoGetDetailsTree
from protoLib.protoLogin import protoGetUserRights, protoLogout, protoGetPasswordRecovery, resetpassword, changepassword
from protoLib.protoActionList import protoList
from protoLib.protoActionRep import sheetConfigRep, protoCsv
from protoLib.protoActionEdit import protoCreate, protoUpdate, protoDelete
from protoLib.protoActions import protoExecuteAction
from protoLib.utils.loadFile import loadFiles
urlpatterns = patterns('', url('^protoExt$', TemplateView.as_view(template_name='protoExt.html')), url('^protoExtReset$', DirectTemplateView.as_view(template_name='protoExt.html', extra_context={'isPasswordReseted': True})), url('protoList/$', protoList), url('sheetConfigRep/$', sheetConfigRep), url('protoCsv/$', protoCsv), url('protoDoActions/$', protoExecuteAction), url('protoAdd/$', protoCreate), url('protoUpd/$', protoUpdate), url('protoDel/$', protoDelete), url('protoGetMenuData/$', protoGetMenuData), url('protoGetPCI/$', protoGetPCI), url('protoSaveProtoObj/$', protoSaveProtoObj), url('protoGetFieldTree/$', protoGetFieldTree), url('protoGetDetailsTree/$', protoGetDetailsTree), url('protoGetUserRights/$', protoGetUserRights), url('protoGetPasswordRecovery/$', protoGetPasswordRecovery), url('resetpassword/$', resetpassword), url('submitChangePassword/$', changepassword), url('protoLogout/$', protoLogout), url('getFieldIncrement/$', getFieldIncrement), url('loadFile/$', loadFiles))