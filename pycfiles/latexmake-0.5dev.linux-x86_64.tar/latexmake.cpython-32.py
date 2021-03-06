# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.2/dist-packages/latexmake.py
# Compiled at: 2013-07-23 10:56:55
"""
    latexmake
    ~~~~~~~~~

    Python module for latexmake which completely automates the process of
    generating a LaTeX document.

    :copyright: (c) 2012-2013 by Marc Schlaich and Jan Kanis
    :license: GPL version 3 or later, see LICENSE for more details.
"""
from os import path
from io import open
from collections import defaultdict
from itertools import chain
from subprocess import Popen, call
from textwrap import dedent
from hashlib import sha256
import argparse, subprocess, errno, filecmp, fnmatch, logging, os, re, shutil, sys, time, copy, errno
try:
    from inotify.watcher import Watcher
    from inotify import _inotify as inotify
    from inotify._inotify import IN_MODIFY, IN_DELETE_SELF, IN_MOVE_SELF
except ImportError:
    Watcher = None
    IN_MODIFY, IN_DELETE_SELF, IN_MOVE_SELF = (2, 1024, 2048)

try:
    import notify2
    from dbus.exceptions import DBusException
except ImportError:
    notify2 = None

__author__ = 'Marc Schlaich'
__version__ = '0.5dev'
__license__ = 'GPL3+'
BIB_PATTERN = re.compile('\\\\bibdata\\{(.*)\\}')
CITE_PATTERN = re.compile('\\\\citation\\{(.*)\\}')
BIBCITE_PATTERN = re.compile('\\\\bibcite\\{(.*)\\}\\{(.*)\\}')
BIBENTRY_PATTERN = re.compile('@.*\\{(.*),\\s')
ERROR_PATTERN = re.compile('(?:^! (.*\\nl\\..*)$)|(?:^! (.*)$)|(No pages of output.)', re.M)
LATEX_RERUN_PATTERN = re.compile('|'.join([
 'LaTeX Warning: Reference .* undefined',
 'LaTeX Warning: There were undefined references\\.',
 'LaTeX Warning: Label\\(s\\) may have changed\\.',
 '.*Warning:.*Rerun to get.*',
 'No file .*(\\.toc|\\.lof)\\.',
 '\\*\\* WARNING \\*\\* Failed to convert input string to UTF16']))
TEXLIPSE_MAIN_PATTERN = re.compile('^mainTexFile=(.*)(?:\\.tex)$', re.M)
LATEX_FLAGS = [
 '-interaction=nonstopmode', '-shell-escape', '--synctex=1']
MAX_RUNS = 4
NO_LATEX_ERROR = "Could not run command '%s'. Is your latex distribution under your PATH?"
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
WATCH_MASK = IN_MODIFY | IN_DELETE_SELF | IN_MOVE_SELF

class LatexMaker(object):
    """
    Main class for generation process.
    """

    def __init__(self, project_name, opt, log=None):
        self.opt = opt
        self.project_name = project_name
        self.log = log
        if self.log == None:
            self.log = globals()['log']
        if self.opt.command:
            self.latex_cmd = self.opt.command
        else:
            if self.opt.pdf:
                self.latex_cmd = 'pdflatex'
            else:
                self.latex_cmd = 'latex'
        self.out = ''
        self.glossaries = dict()
        self.latex_run_counter = 0
        self.bib_file = ''
        return

    def _read_latex_files(self):
        """
        Check if some latex output files exist
        before first latex run, process them and return
        the generated data.

            - Parsing *.aux for citations counter and
              existing glossaries.
            - Getting content of files to detect changes.
                - *.toc file
                - all available glossaries files
        """
        if os.path.isfile('%s.aux' % self.project_name):
            cite_counter = self.generate_citation_counter()
            self.read_glossaries()
        else:
            cite_counter = {'%s.aux' % self.project_name: defaultdict(int)}
        fname = '%s.toc' % self.project_name
        if os.path.isfile(fname):
            with open(fname, 'rb') as (fobj):
                toc_sha = sha256(fobj.read()).digest()
        else:
            toc_sha = ''
        gloss_files = dict()
        for gloss in self.glossaries:
            ext = self.glossaries[gloss][1]
            filename = '%s.%s' % (self.project_name, ext)
            if os.path.isfile(filename):
                with open(filename) as (fobj):
                    gloss_files[gloss] = fobj.read()
                continue

        return (
         cite_counter, toc_sha, gloss_files)

    def _is_toc_changed(self, toc_sha):
        """
        Test if the *.toc file has changed during
        the first latex run.
        """
        fname = '%s.toc' % self.project_name
        if os.path.isfile(fname):
            with open(fname, 'rb') as (fobj):
                if sha256(fobj.read()).digest() != toc_sha:
                    return True

    def _need_bib_run(self, old_cite_counter):
        """
        Determine if you need to run "bibtex".
        1. Check if *.bib exists.
        2. Check latex output for hints.
        3. Test if the numbers of citations changed
           during first latex run.
        4. Examine *.bib for changes.
        """
        with open('%s.aux' % self.project_name) as (fobj):
            match = BIB_PATTERN.search(fobj.read())
            if not match:
                return False
            self.bib_file = match.group(1)
        if not os.path.isfile('%s.bib' % self.bib_file):
            self.log.warning('Could not find *.bib file.')
            return False
        if re.search('No file %s.bbl.' % self.project_name, self.out) or re.search('LaTeX Warning: Citation .* undefined', self.out):
            return True
        if old_cite_counter != self.generate_citation_counter():
            return True
        if os.path.isfile('%s.bib.old' % self.bib_file):
            new = '%s.bib' % self.bib_file
            old = '%s.bib.old' % self.bib_file
            if not filecmp.cmp(new, old):
                return True

    def read_glossaries(self):
        """
        Read all existing glossaries in the main aux-file.
        """
        filename = '%s.aux' % self.project_name
        with open(filename) as (fobj):
            main_aux = fobj.read()
        pattern = '\\\\@newglossary\\{(.*)\\}\\{.*\\}\\{(.*)\\}\\{(.*)\\}'
        for match in re.finditer(pattern, main_aux):
            name, ext_i, ext_o = match.groups()
            self.glossaries[name] = (ext_i, ext_o)

    def check_errors(self):
        """
        Check if errors occured during a latex run by
        scanning the output.
        """
        errors = ERROR_PATTERN.findall(self.out)
        if not errors:
            return True
        else:
            self.log.error('! Errors occurred:')
            error = '\n'.join([error.replace('\r', '').strip() for error in chain(*errors) if error.strip()])
            self.log.error(error)
            self.log.error('! See "%s.log" for details.' % self.project_name)
            if self.opt.exit_on_error:
                raise LatexMkError('\n'.join((error,
                 'See "{}.log" for details.'.format(self.project_name))))
            return False

    def generate_citation_counter(self):
        """
        Generate dictionary with the number of citations in all
        included files. If this changes after the first latex run,
        you have to run "bibtex".
        """
        cite_counter = dict()
        filename = '%s.aux' % self.project_name
        with open(filename) as (fobj):
            main_aux = fobj.read()
        cite_counter[filename] = _count_citations(filename)
        for match in re.finditer('\\\\@input\\{(.*\\.aux)\\}', main_aux):
            filename = match.groups()[0]
            try:
                counter = _count_citations(filename)
            except IOError:
                pass
            else:
                cite_counter[filename] = counter

        return cite_counter

    def latex_run(self):
        """
        Start latex run.
        """
        self.log.info('Running %s...' % self.latex_cmd)
        cmd = [self.latex_cmd]
        cmd.extend(LATEX_FLAGS + ['-jobname', self.project_name])
        cmd.extend(self.opt.texoptions)
        cmd.append('{}.tex'.format(self.project_name))
        self.log.debug('Running ' + ' '.join(cmd))
        try:
            proc = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.out = proc.stdout.read().decode('utf-8', 'replace')
        except OSError as e:
            _fatal_error(NO_LATEX_ERROR % self.latex_cmd, error=e)

        self.latex_run_counter += 1
        return self.check_errors()

    def bibtex_run(self):
        """
        Start bibtex run.
        """
        self.log.info('Running bibtex...')
        try:
            with open(os.devnull, 'w') as (null):
                self.log.debug('Running bibtex ' + self.project_name)
                Popen(['bibtex', self.project_name], stdout=null).wait()
        except OSError as e:
            _fatal_error(NO_LATEX_ERROR % 'bibtex', error=e)

        shutil.copy('%s.bib' % self.bib_file, '%s.bib.old' % self.bib_file)

    def makeindex_runs(self, gloss_files):
        """
        Check for each glossary if it has to be regenerated
        with "makeindex".

        @return: True if "makeindex" was called.
        """
        gloss_changed = False
        for gloss in self.glossaries:
            make_gloss = False
            ext_i, ext_o = self.glossaries[gloss]
            fname_in = '%s.%s' % (self.project_name, ext_i)
            fname_out = '%s.%s' % (self.project_name, ext_o)
            if re.search('No file %s.' % fname_in, self.out):
                make_gloss = True
            if not os.path.isfile(fname_out):
                make_gloss = True
            else:
                with open(fname_out) as (fobj):
                    try:
                        if gloss_files[gloss] != fobj.read():
                            make_gloss = True
                    except KeyError:
                        make_gloss = True

            if make_gloss:
                self.log.info('Running makeindex (%s)...' % gloss)
                try:
                    cmd = [
                     'makeindex', '-q', '-s',
                     '%s.ist' % self.project_name,
                     '-o', fname_in, fname_out]
                    self.log.debug(' '.join(cmd))
                    with open(os.devnull, 'w') as (null):
                        Popen(cmd, stdout=null).wait()
                except OSError as e:
                    _fatal_error(NO_LATEX_ERROR % 'makeindex', error=e)

                gloss_changed = True
                continue

        return gloss_changed

    def open_preview(self):
        """
        Try to open a preview of the generated document.
        """
        self.log.info('Opening preview...')
        if self.opt.pdf:
            ext = 'pdf'
        else:
            ext = 'dvi'
        filename = '%s.%s' % (self.project_name, ext)
        if sys.platform == 'win32':
            try:
                os.startfile(filename)
            except OSError:
                self.log.error('Preview-Error: Extension .%s is not linked to a specific application!' % ext)

        try:
            cmd = 'open' if sys.platform == 'darwin' else 'xdg-open'
            call([cmd, filename])
        except OSError as e:
            self.log.error('Preview-Error: opening previewer failed with the following message:\n' + str(e))

    def need_latex_rerun(self):
        """
        Test for all rerun patterns if they match the output.
        """
        match = LATEX_RERUN_PATTERN.search(self.out)
        if match:
            self.log.debug('rerun pattern found: "{}"'.format(match.group()))
            return True
        return False

    def run(self):
        """Run the LaTeX compilation."""
        self.old_dir = []
        if self.opt.clean:
            self.old_dir = os.listdir('.')
        cite_counter, toc_sha, gloss_files = self._read_latex_files()
        ok = self.latex_run()
        self.read_glossaries()
        gloss_changed = self.makeindex_runs(gloss_files)
        if gloss_changed or self._is_toc_changed(toc_sha):
            ok = self.latex_run()
        if self._need_bib_run(cite_counter):
            self.bibtex_run()
            ok = self.latex_run()
        while self.latex_run_counter < MAX_RUNS:
            if not self.need_latex_rerun():
                break
            ok = self.latex_run()

        if self.opt.check_cite:
            cites = set()
            with open('%s.aux' % self.project_name) as (fobj):
                aux_content = fobj.read()
            for match in BIBCITE_PATTERN.finditer(aux_content):
                name = match.groups()[0]
                cites.add(name)

            with open('%s.bib' % self.bib_file) as (fobj):
                bib_content = fobj.read()
            for match in BIBENTRY_PATTERN.finditer(bib_content):
                name = match.groups()[0]
                if name not in cites:
                    self.log.warn('Bib entry not cited: "%s"' % name)
                    continue

        if self.opt.clean:
            ending = '.dvi'
            if self.opt.pdf:
                ending = '.pdf'
            for fname in os.listdir('.'):
                if not (fname in self.old_dir or fname.endswith(ending)):
                    try:
                        os.remove(fname)
                    except IOError:
                        pass

                    continue

        if self.opt.preview:
            self.open_preview()
        if ok:
            msg = '{}.tex compiled'.format(self.project_name)
            self.log.info(msg)
            if self.opt.notify:
                notify(msg, icon='face-smile')


class PollEvent(object):

    def __init__(self, path, mask):
        self.path = path
        self.mask = mask


class PollWatcher(object):
    """
    A fallback watcher that conforms to the interface of 
    inotify.watcher.Watcher but uses polling.
    """

    def __init__(self, sleep=2):
        self.watchlist = {}
        self.removed = set()
        self.sleeptime = sleep

    def add(self, pth, mask):
        if mask != WATCH_MASK:
            warnings.warn('PollWatcher.add does not support a nonstandard mask')
        self.watchlist[pth] = os.path.getmtime(pth)

    def path(self, pth):
        if pth in self.watchlist:
            return (0, IN_MODIFY)
        else:
            return
            return

    def remove_path(self, pth):
        del self.watchlist[pth]
        self.removed.discard(pth)

    def watches(self):
        for path in self.watchlist.keys():
            yield (path, 0, IN_MODIFY)

    def read(self, buf=None):
        """A simple polling loop checking file's mtime"""
        events = []
        while not events:
            for f, t in self.watchlist.items():
                if f in self.removed:
                    continue
                try:
                    mtime = os.stat(f).st_mtime
                    if mtime > t:
                        events.append(PollEvent(f, IN_MODIFY))
                        self.watchlist[f] = mtime
                except OSError as e:
                    if e.errno in (errno.EACCESS, errno.ELOOP, errno.ENOENT, errno.ENOTDIR):
                        events.append(PollEvent(f, IN_DELETE_SELF))
                        self.removed.add(f)
                    else:
                        raise

            if buf == 0:
                break
            time.sleep(self.sleeptime)

        return events


class LatexWatcher(object):

    def __init__(self, project_name, args):
        self.project_name = project_name
        self.args = args
        self.log = log
        if '-recorder' not in args.texoptions:
            self.args.texoptions.insert(0, '-recorder')
        if self.args.watchmethod == 'inotify' and Watcher:
            self.watcher = Watcher()
            self.log.debug('loaded inotify watcher')
        else:
            self.watcher = PollWatcher()
            self.log.info('inotify not available, falling back on polling watcher')
        self.add_watch(args.filename)
        for w in args.watchfiles:
            self.add_watch(w)

        maker_args = copy.copy(self.args)
        maker_args.preview = False
        maker_args.exit_on_error = True
        self.maker = LatexMaker(self.project_name, maker_args)

    def run(self):
        try:
            self.build()
            if self.args.preview:
                self.maker.open_preview()
            while True:
                self.build()

        except KeyboardInterrupt:
            self.log.info('')
            self.log.info('exiting')

    def update_files(self):
        old_watches = [path for path, wd, mask in self.watcher.watches() if path not in self.args.watchfiles]
        with open(self.project_name + '.fls') as (record):
            for l in record.readlines():
                l = l.rstrip('\n')
                if not l.startswith('INPUT '):
                    continue
                if self.args.texonly and not l.endswith('.tex'):
                    continue
                pth = l.split(' ', 1)[1]
                if not self.args.watch_system:
                    spath = path.abspath(pth).lstrip(path.sep)
                    if spath.startswith(('usr', 'lib', 'etc')):
                        continue
                if not self.watcher.path(pth):
                    self.add_watch(pth)
                else:
                    try:
                        old_watches.remove(pth)
                    except ValueError:
                        pass

        if self.args.filename in old_watches:
            raise LatexMkError("Filename {} is no longer present in LaTeX's list of inputs".format(self.args.filename))
        for pth in old_watches:
            self.remove_watch(pth)

    def add_watch(self, pth):
        self.log.debug('adding watch for ' + pth)
        self.watcher.add(pth, IN_MODIFY | IN_DELETE_SELF | IN_MOVE_SELF)

    def remove_watch(self, pth):
        self.log.debug('removing watch for ' + pth)
        self.watcher.remove_path(pth)

    def wait(self):
        """wait for changes to files"""
        watchmask = IN_MODIFY | IN_DELETE_SELF | IN_MOVE_SELF
        events = []
        while not events:
            try:
                events = [e for e in self.watcher.read() if e.mask & watchmask]
            except OSError as e:
                if e.errno != errno.EINTR:
                    raise

        time.sleep(0.1)
        self.watcher.read(0)
        self.log.debug('events:' + ''.join('\n {} {}'.format(e.path, '|'.join(inotify.decode_mask(e.mask))) for e in events))
        self.log.info('file(s) changed: ' + ' '.join(e.path for e in events))

    def build(self):
        try:
            self.maker.run()
        except LatexMkError as e:
            if self.args.exit_on_error:
                raise

        self.update_files()
        self.wait()


class LatexMkError(Exception):
    pass


class NotifyHandler(logging.Handler):
    """
    A Logging handler that sends messages to the Gnome notification system
    using the notify2 library. Default level is WARN. 
    """

    def __init__(self, level=logging.WARN, *args):
        logging.Handler.__init__(self, *args, level=level)
        self.notification = notify2.Notification('')
        self.timestamp = 0
        self.errors = []

    def emit(self, record):
        now = time.time()
        if now - self.timestamp > 10:
            del self.errors[:]
        self.errors.append(record.getMessage())
        self.notification.update('LatexMk error:', '\n'.join(self.errors), icon='dialog-error')
        self.notification.show()
        self.timestamp = now


def _fatal_error(msg, error=None):
    """
    Log the error to the logger and raise a LatexMkError
    """
    log.error(msg)
    raise LatexMkError(msg) from error


def _parse_texlipse_config():
    """
    Read the project name from the texlipse
    config file ".texlipse".
    """
    if not os.path.isfile('.texlipse'):
        time.sleep(0.1)
    try:
        with open('.texlipse') as (fobj):
            content = fobj.read()
    except EnvironmentError as e:
        _fatal_error('Could not open .texlipse file: ' + str(e), e)

    match = TEXLIPSE_MAIN_PATTERN.search(content)
    if match:
        project_name = match.groups()[0]
        log.info('Found inputfile in ".texlipse": {}.tex'.format(project_name))
        return project_name
    _fatal_error('Parsing .texlipse file failed.')


def projectname(name):
    """
    return the actual project name given a .tex or .texlipse filename
    """
    if name == '.texlipse':
        name = _parse_texlipse_config()
        log.info('Project name is "{}"'.format(name))
    if name.endswith('.tex'):
        name = name[:-4]
    return name


def notify(sum, msg='', icon=''):
    """
    Display a notification. 
    For some standard icon names, see
    http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html#names
    """
    if notify2:
        notify2.Notification(sum, msg, icon=icon).show()


def _count_citations(aux_file):
    """
    Counts the citations in an aux-file.

    @return: defaultdict(int) - {citation_name: number, ...}
    """
    counter = defaultdict(int)
    with open(aux_file) as (fobj):
        content = fobj.read()
    for match in CITE_PATTERN.finditer(content):
        name = match.groups()[0]
        counter[name] += 1

    return counter


def main():
    """
    Set up "argparse" and pass the options to
    a new instance of L{LatexMaker}.
    """
    doctext1, *doctext2 = dedent(__doc__).partition('\n:copyright:')
    doctext = ''.join([doctext1, '\n:version: {}'.format(__version__)] + doctext2) + ' '
    parser = argparse.ArgumentParser(description=doctext, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', default=None, nargs='?', help='input filename. If omitted the current directory\n                            will be searched for a single *.tex file. Specify \n                            ".texlipse" to find the .tex file from a *.texlipse\n                            project file.')
    parser.add_argument('-f', dest='filename', help="The .tex file to watch. Same as the program's \n                          first argument.")
    parser.add_argument('-c', '--clean', action='store_true', dest='clean', default=False, help='Clean all temporary files after converting.')
    parser.add_argument('-q', '--quiet', action='count', dest='quiet', default=0, help="Don't print status messages to stdout. Specify twice not to show error messages either.")
    parser.add_argument('-d', '--debug', action='store_const', dest='quiet', const=-1, default=0, help='Show debugging information.')
    parser.add_argument('-n', '--no-exit', action='store_false', dest='exit_on_error', default=True, help="Don't exit if error occurs.")
    parser.add_argument('-N', '--notify', action='store_true', dest='notify', default=False, help='Notify through the desktop environment if a \n                          rebuild is finished and if errors occured. Currently \n                          only available on Gnome.')
    parser.add_argument('-p', '--preview', action='store_true', dest='preview', default=False, help='Try to open preview of generated document.')
    parser.add_argument('--dvi', action='store_false', dest='pdf', default=True, help='use "latex" instead of pdflatex')
    parser.add_argument('-t', '--tex-command', dest='command', help='The latex compiler command to use.')
    parser.add_argument('--check-cite', action='store_true', dest='check_cite', default=False, help='Check bibtex file for uncited entries.')
    parser.add_argument('-P', '--texoutput', action='store_true', default=False, help='Show the output of the called commands')
    parser.add_argument('--pvc', '--preview-continuously', dest='continuous', action='store_true', default=False, help='preview continuously. Keep running, watching the \n                          .tex file and any .tex dependencies for changes \n                          and rebuilding the document on changes. ')
    parser.add_argument('-w', '--watch', dest='watch', action='store_true', default=False, help='Turn on all options useful for running in the \n                          background and building the latex file on changes. \n                          This implies --pvc, -n and -N (if available).')
    parser.add_argument('--watch-system', action='store_true', default=False, help='Also watch system files. By default files under \n                          /usr and /etc are not watched for changes.')
    parser.add_argument('--watch-all', action='store_false', default=True, dest='texonly', help='Also watch imported files that do not end in .tex\n                          for changes.')
    parser.add_argument('--latex-options', action='append', dest='texoptions', nargs='+', default=[], help='Additional options to pass to latex.')
    parser.add_argument('--makeglossaries-options', action='append', dest='glossariesoptions', nargs='+', default=[], help='Additional options to pass to `makeglossaries`.')
    parser.add_argument('--watchfile', dest='watchfiles', nargs='+', default=[], help='Also watch these files for changes.')
    parser.add_argument('--watchmethod', nargs=1, choices=['inotify', 'poll'], default='inotify', help='Specify the method used to detect file changes.')
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
    args, rest = parser.parse_known_args()
    if rest:
        parser.error('unrecognized arguments: {}. Specify at most one filename'.format(' '.join('"{}"'.format(r) for r in rest)))
    if args.filename == None:
        tex_files = fnmatch.filter(os.listdir('.'), '*.tex')
        if len(tex_files) == 1:
            args.filename = tex_files[0]
        else:
            if len(tex_files) == 0:
                parser.error('could not find one *.tex file in current directory')
            else:
                parser.error('multiple *.tex files in current directory, specify only one')
    if args.texoptions:
        args.texoptions = [op for list in args.texoptions for op in list]
    args.verbosity = {-1: logging.DEBUG,  0: logging.INFO,  1: logging.ERROR, 
     2: logging.FATAL}[min(args.quiet, 2)]
    log.setLevel(args.verbosity)
    log.debug('arguments: ' + str(args))
    if args.watch:
        args.continuous = True
        args.exit_on_error = False
        if notify2:
            args.notify = True
    if args.notify:
        if notify2 is None:
            parser.error("Unable to use desktop notification ('-N', '--notify'). Could not load package 'notify2'.")
        try:
            notify2.init('LatexMk')
            log.addHandler(NotifyHandler())
        except DBusException as e:
            log.error('Failed to initialize DBus: ' + str(e))
            parser.error("Unable to use desktop notification ('-N', '--notify'). Failed to initialize DBus.")

    try:
        if args.continuous:
            LatexWatcher(projectname(args.filename), args).run()
        else:
            LatexMaker(projectname(args.filename), args).run()
    except LatexMkError as e:
        log.error('! Exiting...')
        sys.exit(1)

    return


if __name__ == '__main__':
    main()