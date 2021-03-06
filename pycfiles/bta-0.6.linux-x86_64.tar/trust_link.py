# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/trust_link.py
# Compiled at: 2015-10-20 16:27:01
from bta.miner import Miner

@Miner.register
class TrustLink(Miner):
    _name_ = 'TrustLink'
    _desc_ = 'Find all trusted domain object'
    _uses_ = ['raw.datatable', 'special.categories']

    def run(self, options, doc):
        trusted = self.datatable.find({'objectCategory': self.categories.trusted_domain})
        ta = doc.create_table('Trusted domains:')
        ta.add(['Partner', 'Created', 'Changed', 'Direction', 'type', 'Attributes'])
        ta.add()
        for t in trusted:
            trustatt = t.get('trustAttributes')
            if trustatt is None:
                trustatt = {'flags': {'EMPTY': True}}
            ta.add([t.get('trustPartner'),
             t.get('whenCreated'),
             t.get('whenChanged'),
             t.get('trustDirection'),
             t.get('trustType'),
             (', ').join([ a for a, b in trustatt.get('flags').items() if b ])])

        ta.flush()
        ta.finished()
        return

    def assert_consistency(self):
        Miner.assert_consistency(self)
        self.assert_field_type(self.datatable, 'name', str, unicode)