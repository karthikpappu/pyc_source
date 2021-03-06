# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhardware\config\connected_instruments.py
# Compiled at: 2013-10-05 04:00:20
"""
This module helps discover the instruments connected and their models
"""
from pyhardware.config.pyinstruments_config import PyInstrumentsConfig

def get_model_name(address):
    """Physically queries the instrument model at the given address"""
    from visa import VisaIOError
    import visa
    model = 'no device'
    try:
        instr = visa.Instrument(str(address))
        timeout = instr.timeout
    except VisaIOError:
        print 'instrument at address ' + str(address) + " didn't reply in time..."
    else:
        try:
            try:
                instr.timeout = 0.1
                ret = instr.ask('*IDN?')
            except VisaIOError as TypeError:
                print 'instrument at address ' + address + " didn't reply in time..."
            else:
                model = ret.split(',')[1]

        finally:
            instr.timeout = timeout

    return model


EXISTING_ADRESSES = None

def existing_addresses(recheck=True):
    """
    returns a list of all valid addresses (using visa.get_instruments_list())
    """
    global EXISTING_ADRESSES
    if recheck or EXISTING_ADRESSES == None:
        import visa
        EXISTING_ADRESSES = visa.get_instruments_list()
    return EXISTING_ADRESSES


def get_surrounding_instruments():
    """returns a dictionnary with address:model_string as key,value pair"""
    dictionnary = dict()
    import visa
    adress = existing_addresses()
    for adr in adress:
        dictionnary[adr] = get_model_name(adr)

    return dictionnary


def add_all_new_instruments():
    """Looks at all surrounding instruments as listed by 
    visa.get_instrument_list() and queries the model
    """
    dictionnary = get_surrounding_instruments()
    pic = PyInstrumentsConfig()
    existing_addresses = [ instr['address'] for instr in pic.values() ]
    for address, model in dictionnary.iteritems():
        if address not in existing_addresses:
            if model == 'no device':
                model = None
            if len(address) < 10:
                tag = address
            else:
                tag = 'DEV'
            tag = pic.add_instrument(tag, address=address, model=model)

    return


def query_models():
    """Physically queries all instruments models"""
    pic = PyInstrumentsConfig()
    for item in pic.values():
        item['model'] = get_model_name(item['address'])

    pic.save()