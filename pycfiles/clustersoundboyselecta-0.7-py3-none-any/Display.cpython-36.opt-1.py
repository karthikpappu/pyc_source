# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/CLI/Display.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 10054 bytes
__doc__ = '\nCLI results display class\n'
from __future__ import print_function
import difflib, sys
from ClusterShell.NodeSet import NodeSet
VERB_QUIET = 0
VERB_STD = 1
VERB_VERB = 2
VERB_DEBUG = 3
THREE_CHOICES = ['never', 'always', 'auto']
WHENCOLOR_CHOICES = THREE_CHOICES
if sys.getdefaultencoding() == 'ascii':
    STRING_ENCODING = 'utf-8'
else:
    STRING_ENCODING = sys.getdefaultencoding()

def sys_stdin():
    return getattr(sys.stdin, 'buffer', sys.stdin)


def sys_stdout():
    return getattr(sys.stdout, 'buffer', sys.stdout)


def sys_stderr():
    return getattr(sys.stderr, 'buffer', sys.stderr)


class Display(object):
    """Display"""
    COLOR_RESULT_FMT = '\x1b[92m%s\x1b[0m'
    COLOR_STDOUT_FMT = '\x1b[94m%s\x1b[0m'
    COLOR_STDERR_FMT = '\x1b[91m%s\x1b[0m'
    COLOR_DIFFHDR_FMT = '\x1b[1m%s\x1b[0m'
    COLOR_DIFFHNK_FMT = '\x1b[96m%s\x1b[0m'
    COLOR_DIFFADD_FMT = '\x1b[92m%s\x1b[0m'
    COLOR_DIFFDEL_FMT = '\x1b[91m%s\x1b[0m'
    SEP = '---------------'

    class _KeySet(set):
        """Display._KeySet"""

        def __str__(self):
            return ','.join(self)

    def __init__(self, options, config=None, color=None):
        """Initialize a Display object from CLI.OptionParser options
        and optional CLI.ClushConfig.

        If `color' boolean flag is not specified, it is auto detected
        according to options.whencolor.
        """
        if options.diff:
            self._print_buffer = self._print_diff
        else:
            self._print_buffer = self._print_content
        self._display = self._print_buffer
        self._diffref = None
        self.gather = options.gatherall or options.gather or options.diff
        self.progress = getattr(options, 'progress', False)
        if options.diff:
            if options.line_mode:
                raise ValueError('diff not supported in line_mode')
        else:
            self.line_mode = options.line_mode
            self.label = options.label
            self.regroup = options.regroup
            self.groupsource = options.groupsource
            self.noprefix = options.groupbase
            self.maxrc = getattr(options, 'maxrc', False)
            if color is None:
                color = False
                if not options.whencolor or options.whencolor == 'auto':
                    color = sys.stdout.isatty()
                elif options.whencolor == 'always':
                    color = True
            self._color = color
            self.out = sys_stdout()
            self.err = sys_stderr()
            if self._color:
                self.color_stdout_fmt = self.COLOR_STDOUT_FMT
                self.color_stderr_fmt = self.COLOR_STDERR_FMT
                self.color_diffhdr_fmt = self.COLOR_DIFFHDR_FMT
                self.color_diffctx_fmt = self.COLOR_DIFFHNK_FMT
                self.color_diffadd_fmt = self.COLOR_DIFFADD_FMT
                self.color_diffdel_fmt = self.COLOR_DIFFDEL_FMT
            else:
                self.color_stdout_fmt = self.color_stderr_fmt = self.color_diffhdr_fmt = self.color_diffctx_fmt = self.color_diffadd_fmt = self.color_diffdel_fmt = '%s'
        if config:
            self.node_count = config.node_count
            self.verbosity = config.verbosity
        else:
            self.node_count = True
            self.verbosity = VERB_STD
        if hasattr(options, 'quiet'):
            if options.quiet:
                self.verbosity = VERB_QUIET
        if hasattr(options, 'verbose'):
            if options.verbose:
                self.verbosity = VERB_VERB
        if hasattr(options, 'debug'):
            if options.debug:
                self.verbosity = VERB_DEBUG

    def flush(self):
        """flush display object buffers"""
        self._diffref = None

    def _getlmode(self):
        """line_mode getter"""
        return self._display == self._print_lines

    def _setlmode(self, value):
        """line_mode setter"""
        if value:
            self._display = self._print_lines
        else:
            self._display = self._print_buffer

    line_mode = property(_getlmode, _setlmode)

    def _format_nodeset(self, nodeset):
        """Sub-routine to format nodeset string."""
        if self.regroup:
            return nodeset.regroup((self.groupsource), noprefix=(self.noprefix))
        else:
            return str(nodeset)

    def format_header(self, nodeset, indent=0):
        """Format nodeset-based header."""
        if not self.label:
            return ''
        else:
            indstr = ' ' * indent
            nodecntstr = ''
            if self.verbosity >= VERB_STD:
                if self.node_count:
                    if len(nodeset) > 1:
                        nodecntstr = ' (%d)' % len(nodeset)
            hdr = self.color_stdout_fmt % ('%s%s\n%s%s%s\n%s%s' % (
             indstr, self.SEP,
             indstr, self._format_nodeset(nodeset), nodecntstr,
             indstr, self.SEP))
            return hdr.encode(STRING_ENCODING) + '\n'

    def print_line(self, nodeset, line):
        """Display a line with optional label."""
        if self.label:
            prefix = self.color_stdout_fmt % ('%s: ' % nodeset)
            self.out.write(prefix.encode(STRING_ENCODING) + line + '\n')
        else:
            self.out.write(line + '\n')

    def print_line_error(self, nodeset, line):
        """Display an error line with optional label."""
        if self.label:
            prefix = self.color_stderr_fmt % ('%s: ' % nodeset)
            self.err.write(prefix.encode(STRING_ENCODING) + line + '\n')
        else:
            self.err.write(line + '\n')

    def print_gather(self, nodeset, obj):
        """Generic method for displaying nodeset/content according to current
        object settings."""
        return self._display(NodeSet(nodeset), obj)

    def print_gather_finalize(self, nodeset):
        """Finalize display of diff-like gathered contents."""
        if self._display == self._print_diff:
            if self._diffref:
                return self._display(nodeset, '')

    def print_gather_keys(self, keys, obj):
        """Generic method for displaying raw keys/content according to current
        object settings (used by clubak)."""
        return self._display(self.__class__._KeySet(keys), obj)

    def _print_content(self, nodeset, content):
        """Display a dshbak-like header block and content."""
        self.out.write(self.format_header(nodeset) + bytes(content) + '\n')

    def _print_diff(self, nodeset, content):
        """Display unified diff between remote gathered outputs."""
        if self._diffref is None:
            self._diffref = (
             nodeset, content)
        else:
            nodeset_ref, content_ref = self._diffref
            nsstr_ref = self._format_nodeset(nodeset_ref)
            nsstr = self._format_nodeset(nodeset)
            if self.verbosity >= VERB_STD:
                if self.node_count:
                    if len(nodeset_ref) > 1:
                        nsstr_ref += ' (%d)' % len(nodeset_ref)
                    if len(nodeset) > 1:
                        nsstr += ' (%d)' % len(nodeset)
            alist = [aline.decode('utf-8', 'ignore') for aline in content_ref]
            blist = [bline.decode('utf-8', 'ignore') for bline in content]
            udiff = difflib.unified_diff(alist, blist, fromfile=nsstr_ref, tofile=nsstr,
              lineterm='')
            output = ''
            for line in udiff:
                if line.startswith('---') or line.startswith('+++'):
                    output += self.color_diffhdr_fmt % line.rstrip()
                else:
                    if line.startswith('@@'):
                        output += self.color_diffctx_fmt % line
                    else:
                        if line.startswith('+'):
                            output += self.color_diffadd_fmt % line
                        else:
                            if line.startswith('-'):
                                output += self.color_diffdel_fmt % line
                            else:
                                output += line
                output += '\n'

            self.out.write(output.encode(STRING_ENCODING))

    def _print_lines(self, nodeset, msg):
        """Display a MsgTree buffer by line with prefixed header."""
        out = self.out
        if self.label:
            header = self.color_stdout_fmt % ('%s: ' % self._format_nodeset(nodeset))
            for line in msg:
                out.write(header.encode(STRING_ENCODING) + line + '\n')

        else:
            for line in msg:
                out.write(line + '\n')

    def vprint(self, level, message):
        """Utility method to print a message if verbose level is high
        enough."""
        if self.verbosity >= level:
            print(message)

    def vprint_err(self, level, message):
        """Utility method to print a message on stderr if verbose level
        is high enough."""
        if self.verbosity >= level:
            print(message, file=(sys.stderr))