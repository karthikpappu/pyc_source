# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/oie/KannelMonitor/setuphandlers.py
# Compiled at: 2010-09-10 03:00:38
from Acquisition import aq_base
from lbn.zenoss.packutils import addZenPackObjects
from Products.ZenEvents.EventClass import manage_addEventClass
from Products.ZenModel.RRDTemplate import manage_addRRDTemplate
from datasources import KannelDataSource
from config import DATAPOINTS, GRAPHPOINTS

def setDataPoints(graphdef, prefix, tags):
    pretty_tags = {}
    for tag in tags:
        if tag.find('_') != -1:
            pretty = tag.replace('_', ' ').capitalize()
        else:
            pretty = tag
        pretty_tags[pretty] = tag

    graphdef.manage_addDataPointGraphPoints(pretty_tags.keys())
    for dp in graphdef.graphPoints():
        id = dp.getId()
        if pretty_tags.has_key(id):
            dp.dpName = '%s_%s' % (prefix, pretty_tags[id])


def install(zport, zenpack):
    """
    Set the collector plugin
    """
    dmd = zport.dmd
    if not getattr(aq_base(dmd.Events.Status), 'Kannel', None):
        manage_addEventClass(dmd.Events.Status, 'Kannel')
    tpls = dmd.Devices.Server.rrdTemplates
    if not getattr(aq_base(tpls), 'KannelServer', None):
        manage_addRRDTemplate(tpls, 'KannelServer')
        tpl = tpls.KannelServer
        tpl.manage_changeProperties(description='Monitors Kannel SMPP Servers', targetPythonClass='Products.ZenModel.Device')
        tpl.manage_addRRDDataSource('kannel', 'KannelDataSource.KannelDataSource')
        dsk = tpl.datasources.kannel
        map(lambda x: dsk.manage_addRRDDataPoint(x), DATAPOINTS)
        for dp_name in ('recv', 'sent'):
            dp = dsk.datapoints._getOb(dp_name)
            if dp.rrdtype != 'DERIVE':
                dp.manage_changeProperties(rrdtype='DERIVE', rrdmin='0', rrdmax='10000000')

        gdq = dsk.manage_addGraphDefinition('Kannel SMSC Queue')
        setDataPoints(gdq, 'kannel', GRAPHPOINTS['smsc'])
        gds = dsk.manage_addGraphDefinition('Kannel Store Size')
        setDataPoints(gds, 'kannel', GRAPHPOINTS['store'])
    addZenPackObjects(zenpack, (zport.dmd.Events.Status.Kannel, tpls.KannelServer))
    return


def uninstall(zport):
    for (parent, id) in ((zport.dmd.Events.Status, 'Kannel'),
     (
      zport.dmd.Devices.Server.rrdTemplates, 'KannelServer')):
        if getattr(aq_base(parent), id, None):
            parent._delObject(id)

    return