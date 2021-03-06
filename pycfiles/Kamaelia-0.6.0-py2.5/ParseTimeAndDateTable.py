# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Device/DVB/Parse/ParseTimeAndDateTable.py
# Compiled at: 2008-10-19 12:19:52
"""===========================================
Parsing Time And Date Tables in DVB streams
===========================================

ParseTimeAndDateTable parses a reconstructed PSI table from a DVB MPEG
Transport Stream, and outputs the current time and date in UTC (GMT).

The purpose of the TDT and details of the fields within in are defined in the
DVB SI specification:

- ETSI EN 300 468 
  "Digital Video Broadcasting (DVB); Specification for Service Information (SI)
  in DVB systems"
  ETSI / EBU (DVB group)

The Time Offset Table (TOT) additionally contains information on the current
(and next) timezone offset that applies, as well as duplicating the datetime
information. See ParseTimeOffsetTable component.

Example Usage
-------------

A simple pipeline to receive, parse and display the Time and Date Table::

    FREQUENCY = 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    TDT_PID = 0x14
    
    Pipeline( DVB_Multiplex(FREQUENCY, [TDT_PID], feparams),
              DVB_Demuxer({ TDT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseTimeAndDateTable(),
              PrettifyTimeAndDateTable(),
              ConsoleEchoer(),
            ).run()

The output will look like this::

    [2006, 12, 21, 15, 1, 3]
    [2006, 12, 21, 15, 1, 4]
    [2006, 12, 21, 15, 1, 5]
    [2006, 12, 21, 15, 1, 6]

    .....

Behaviour
---------

Send reconstructed PSI table 'sections' to the "inbox" inbox. When all sections
of the table have arrived, ParseServiceDescriptionTable will parse the table and
send it out of its "outbox" outbox.

The table is output every time it is received. In practice a multiplex is likely
to transmit about 1 instance of this table per second, giving a reasonably
accurate measure of the current time.

The value output is a simple list/tuple describing the current UTC (GMT) date
and time, in the form (year,month,day,hour,minute,second).

For example: 21st December 2006 15:01:03 GMT is represented as::

    [2006, 12, 21, 15, 1, 3]

If this data is sent on through a PrettifyTimeAndDateTable component, then the
equivalent output is a string of the following form::

    TDT received:
       UTC Date now (y,m,d) : 2006 12 21
       UTC Time now (h,m,s) : 15:01:03

If a shutdownMicroprocess or producerFinished message is received on the
"control" inbox, then it will immediately be sent on out of the "signal" outbox
and the component will then immediately terminate.

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Support.DVB.Descriptors import parseDescriptor
from Kamaelia.Support.DVB.CRC import dvbcrc
from Kamaelia.Support.DVB.DateTime import parseMJD, unBCD
TDT_PID = 20

class ParseTimeAndDateTable(component):
    """    ParseTimeAndDateTable() -> new ParseTimeAndDateTable component.

    Send reconstructed PSI table sections to the "inbox" inbox. When a complete
    table is assembled and parsed, the result is sent out of the "outbox" outbox
    in the form [year,month,day,hour,minute,second]. The times are UTC (GMT).
    """
    Inboxes = {'inbox': 'DVB PSI Packets from a single PID containing a TDT table', 'control': 'Shutdown signalling'}
    Outboxes = {'outbox': 'Current date and time (UTC)', 'signal': 'Shutdown signalling'}

    def __init__(self):
        super(ParseTimeAndDateTable, self).__init__()

    def shutdown(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            self.send(msg, 'signal')
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True

        return False

    def main(self):
        while not self.shutdown():
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                e = [ ord(data[i]) for i in range(0, 3) ]
                table_id = e[0]
                if table_id != 112:
                    continue
                syntax = e[1] & 128
                if syntax:
                    continue
                section_length = (e[1] << 8) + e[2] & 4095
                e = [ ord(data[i]) for i in range(0, 8) ]
                utc = list(parseMJD((e[3] << 8) + e[4]))
                utc.extend([unBCD(e[5]), unBCD(e[6]), unBCD(e[7])])
                self.send(utc, 'outbox')

            self.pause()
            yield 1


__kamaelia_components__ = (
 ParseTimeAndDateTable,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
    from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables
    from Kamaelia.Device.DVB.Parse.PrettifyTables import PrettifyTimeAndDateTable
    import dvb3.frontend
    feparams = {'inversion': dvb3.frontend.INVERSION_AUTO, 
       'constellation': dvb3.frontend.QAM_16, 
       'code_rate_HP': dvb3.frontend.FEC_3_4, 
       'code_rate_LP': dvb3.frontend.FEC_3_4}
    Pipeline(DVB_Multiplex(505833330.0 / 1000000.0, [8192], feparams), DVB_Demuxer({TDT_PID: ['outbox']}), ReassemblePSITables(), ParseTimeAndDateTable(), PrettifyTimeAndDateTable(), ConsoleEchoer()).run()