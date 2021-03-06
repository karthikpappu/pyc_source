# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/global.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 2251 bytes
import string
from pylinkirc import conf, utils, world
from pylinkirc.coremods import permissions
from pylinkirc.log import log
DEFAULT_FORMAT = '[$sender@$fullnetwork] $text'

def g(irc, source, args):
    """<message text>

    Sends out a Instance-wide notice.
    """
    permissions.check_permissions(irc, source, ['global.global'])
    message = ' '.join(args).strip()
    if not message:
        irc.error('Refusing to send an empty message.')
        return
    global_conf = conf.conf.get('global') or {}
    template = string.Template(global_conf.get('format', DEFAULT_FORMAT))
    exempt_channels = set(global_conf.get('exempt_channels', set()))
    netcount = 0
    chancount = 0
    for netname, ircd in world.networkobjects.items():
        if ircd.connected.is_set() and ircd.pseudoclient:
            netcount += 1
            for channel in ircd.pseudoclient.channels:
                local_exempt_channels = exempt_channels | set(ircd.serverdata.get('global_exempt_channels', set()))
                skip = False
                for exempt in local_exempt_channels:
                    if ircd.match_text(exempt, str(channel)):
                        log.debug('global: Skipping channel %s%s for exempt %r', netname, channel, exempt)
                        skip = True
                        break

                if skip:
                    pass
                else:
                    subst = {'sender':irc.get_friendly_name(source), 
                     'network':irc.name, 
                     'fullnetwork':irc.get_full_network_name(), 
                     'current_channel':channel, 
                     'current_network':netname, 
                     'current_fullnetwork':ircd.get_full_network_name(), 
                     'text':message}
                    ircd.msg(channel, (template.safe_substitute(subst)), loopback=False)
                    chancount += 1

    irc.reply('Done. Sent to %d channels across %d networks.' % (chancount, netcount))


utils.add_cmd(g, 'global', featured=True)