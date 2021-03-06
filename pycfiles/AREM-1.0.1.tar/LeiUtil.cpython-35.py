# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/LeiUtil.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 2437 bytes
__doc__ = '\nCreated on Apr 25, 2015\n\n@author: Mark V Systems Limited\n(c) Copyright 2015 Mark V Systems Limited, All rights reserved.\n\nImplementation of ISO 17442:2012(E) Appendix A\n\n'
try:
    import regex as re
except ImportError:
    import re

LEI_VALID = 0
LEI_INVALID_LEXICAL = 1
LEI_INVALID_CHECKSUM = 2
LEI_RESULTS = ('valid', 'invalid lexical', 'invalid checksum')
leiLexicalPattern = re.compile('^[0-9A-Z]{18}[0-9]{2}$')

def checkLei(lei):
    if not leiLexicalPattern.match(lei):
        return LEI_INVALID_LEXICAL
    if not int(''.join({'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', 'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15', 'G': '16', 'H': '17', 'I': '18', 'J': '19', 'K': '20', 'L': '21', 'M': '22', 'N': '23', 'O': '24', 'P': '25', 'Q': '26', 'R': '27', 'S': '28', 'T': '29', 'U': '30', 'V': '31', 'W': '32', 'X': '33', 'Y': '34', 'Z': '35'}[c] for c in lei)) % 97 == 1:
        return LEI_INVALID_CHECKSUM
    return LEI_VALID


if __name__ == '__main__':
    for lei, name in (('001GPB6A9XPE8XJICC14', 'Fidelity Advisor Series I'), ('004L5FPTUREIWK9T2N63', 'Hutchin Hill Capital, LP'),
                      ('00EHHQ2ZHDCFXJCPCL46', 'Vanguard Russell 1000 Growth Index Trust'),
                      ('00GBW0Z2GYIER7DHDS71', 'Aristeia Capital, L.L.C.'), ('1S619D6B3ZQIH6MS6B47', 'Barclays Vie SA'),
                      ('21380014JAZAUFJRHC43', 'BRE/OPERA HOLDINGS'), ('21380016W7GAG26FIJ74', 'SOCIETE FRANCAISE ET SUISSE'),
                      ('21380058ERUIT9H53T71', 'TOTAN ICAP CO., LTD'), ('213800A9GT65GAES2V60', 'BARCLAYS SECURITIES JAPAN LIMITED'),
                      ('213800DELL1MWFDHVN53', 'PIRELLI JAPAN'), ('213800A9GT65GAES2V60', 'BARCLAYS SECURITIES JAPAN LIMITED'),
                      ('214800A9GT65GAES2V60', 'Error 1'), ('213800A9GT65GAE%2V60', 'Error 2'),
                      ('213800A9GT65GAES2V62', 'Error 3'), ('1234', 'Error 4'), ('    \n5299003M8JKHEFX58Y02', 'Error 4')):
        print('LEI {} result {} name {}'.format(lei, LEI_RESULTS[checkLei(lei)], name))