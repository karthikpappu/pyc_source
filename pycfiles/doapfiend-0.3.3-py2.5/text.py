# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/doapfiend/plugins/text.py
# Compiled at: 2008-06-09 19:05:55
"""

Plain text serializer
=====================

This plugin outputs DOAP in human-readable plain text

"""
__docformat__ = 'epytext'
import logging, textwrap
from cStringIO import StringIO
from rdflib import Namespace
from rdfalchemy import rdfSubject
from doapfiend.plugins.base import Plugin
from doapfiend.utils import COLOR
from doapfiend.doaplib import load_graph
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
LOG = logging.getLogger(__name__)

class OutputPlugin(Plugin):
    """Class for formatting DOAP output"""
    name = 'text'
    enabled = False
    enable_opt = None

    def __init__(self):
        """Setup Plain Text OutputPlugin class"""
        super(OutputPlugin, self).__init__()
        self.options = None
        return

    def add_options(self, parser, output, search):
        """Add plugin's options to doapfiend's opt parser"""
        output.add_option('--%s' % self.name, action='store_true', dest=self.enable_opt, help='Output DOAP as plain text (Default)')
        return (parser, output, search)

    def serialize(self, doap_xml, color=False):
        """
        Serialize RDF/XML DOAP as plain text

        @param doap_xml: DOAP in RDF/XML serialization
        @type doap_xml: string
        
        @rtype: unicode
        @return: DOAP in plain text
        """
        if hasattr(self.options, 'no_color'):
            color = not self.options.no_color
        if not color:
            for this in COLOR:
                COLOR[this] = '\x1b[0m'

        if hasattr(self.options, 'quiet'):
            brief = self.options.quiet
        else:
            brief = False
        printer = DoapPrinter(load_graph(doap_xml, get_list=True), brief, color)
        return printer.print_doap()


class DoapPrinter(object):
    """Prints DOAP in human readable text"""

    def __init__(self, doap, brief=False, color=False):
        """Initialize attributes"""
        self.brief = brief
        self.doap_list = doap
        self.doap = None
        self.text = StringIO()
        self.color = color
        return

    def write(self, text):
        """
        Write to DOAP output file object
        """
        self.text.write(text.encode('utf-8') + '\n')

    def print_doap(self):
        """
        Serialize DOAP in human readable text, optionally colorized

        @rtype: unicode
        @return: DOAP as plain text
        """
        for doap in self.doap_list:
            self.doap = doap
            self.print_misc()
            if self.brief:
                return
            self.print_people()
            self.print_repos()
            self.print_releases()

        doap = self.text.getvalue()
        self.text.close()
        return doap

    def print_misc(self):
        """Prints basic DOAP metadata"""
        fields = ('name', 'shortname', 'homepage', 'shortdesc', 'description', 'old_homepage',
                  'created', 'download_mirror')
        fields_verbose = ('license', 'programming_language', 'bug_database', 'screenshots',
                          'oper_sys', 'wiki', 'download_page', 'mailing_list')
        for fld in fields:
            self.print_field(fld)

        if not self.brief:
            for fld in fields_verbose:
                self.print_field(fld)

    def print_repos(self):
        """Prints DOAP repository metadata"""
        if hasattr(self.doap.cvs_repository, 'module') and self.doap.cvs_repository.module is not None:
            self.write(misc_field('CVS Module:', self.doap.cvs_repository.module))
            self.write(misc_field('CVS Anon:', self.doap.cvs_repository.anon_root))
            self.write(misc_field('CVS Browse:', self.doap.cvs_repository.cvs_browse.resUri))
        if hasattr(self.doap.svn_repository, 'location') and self.doap.svn_repository.location is not None:
            self.write(misc_field('SVN Location:', self.doap.svn_repository.location.resUri))
            if hasattr(self.doap.svn_repository, 'svn_browse') and self.doap.svn_repository.svn_browse is not None:
                self.write(misc_field('SVN Browse:', self.doap.svn_repository.svn_browse.resUri))
        return

    def print_releases(self):
        """Print DOAP package release metadata"""
        if hasattr(self.doap, 'releases') and len(self.doap.releases) != 0:
            self.write(COLOR['bold'] + 'Releases:' + COLOR['normal'])
            for release in self.doap.releases:
                if release.name:
                    self.write(COLOR['bold'] + COLOR['cyan'] + release.name + COLOR['normal'])
                if hasattr(release, 'created') and release.created is not None:
                    created = release.created
                else:
                    created = ''
                self.write(COLOR['cyan'] + '  ' + release.revision + ' ' + COLOR['normal'] + created)
                if hasattr(release, 'changelog'):
                    if release.changelog:
                        self.write(COLOR['yellow'] + release.changelog + COLOR['normal'])
                for frel in release.file_releases:
                    self.write('   %s' % frel.resUri)

        return

    def print_people(self):
        """Print all people involved in the project"""
        people = [
         'maintainer', 'developer', 'documenter', 'helper',
         'tester', 'translator']
        for job in people:
            if hasattr(self.doap, job):
                attribs = getattr(self.doap, job)
                if len(attribs) > 0:
                    peeps = []
                    for attr in attribs:
                        if attr[FOAF.mbox] is None:
                            person = '%s' % attr[FOAF.name]
                        else:
                            mbox = attr[FOAF.mbox].resUri
                            if mbox.startswith('mailto:'):
                                mbox = mbox[7:]
                                person = '%s <%s>' % (attr[FOAF.name], mbox)
                            else:
                                LOG.debug('mbox is invalid: %s' % mbox)
                                person = '%s' % attr[FOAF.name]
                        peeps.append(person)

                    label = job.capitalize() + 's:'
                    self.write(misc_field(label, (', ').join([ p for p in peeps ])))

        return

    def print_field(self, name):
        """
        Print a DOAP element

        @param name: A misc DOAP element
        @type name: string, list or RDFSubject

        @rtype: None
        @return: Nothing
        """
        if not hasattr(self.doap, name):
            return
        attr = getattr(self.doap, name)
        if attr is [] or attr is None:
            return
        label = '%s' % COLOR['bold'] + pretty_name(name) + COLOR['normal'] + ':'
        label = label.ljust(21)
        if isinstance(attr, list):
            text = ''
            for thing in getattr(self.doap, name):
                if isinstance(thing, rdfSubject):
                    text += thing.resUri + '\n'
                else:
                    thing = thing.strip()
                    text += thing + '\n'

        else:
            text = getattr(self.doap, name)
            if isinstance(text, rdfSubject):
                text = text.resUri
            else:
                text = text.strip()
        if text:
            if text.startswith('http://'):
                self.write('%s %s' % (label, text.strip()))
            else:
                self.write(textwrap.fill('%s %s' % (label, text), initial_indent='', subsequent_indent='              '))
        return


def pretty_name(field):
    """
    Convert DOAP element name to pretty printable label
    Shorten some labels for formatting purposes

    @param field: Text to be formatted
    @type field: C{string}

    @return: formatted string
    @rtype: string
    """
    if field == 'programming_language':
        field = 'Prog. Lang.'
    elif field == 'created':
        field = 'DOAP Created'
    else:
        field = field.capitalize()
        field = field.replace('_', ' ')
        field = field.replace('-', ' ')
    return field


def misc_field(label, text):
    """
    Print colorized and justified single label value pair

    @param label: A label
    @type label: string

    @param text: Text to print
    @type text: string

    @rtype: string
    @return: Colorized, left-justified text with label
    """
    label = label.ljust(13)
    label = COLOR['bold'] + label + COLOR['normal']
    return '%s %s' % (label, text)