# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/clients/plastic.py
# Compiled at: 2020-04-14 20:27:46
"""A client for Plastic SCM."""
from __future__ import unicode_literals
import logging, os, re
from rbtools.clients import SCMClient, RepositoryInfo
from rbtools.clients.errors import InvalidRevisionSpecError, TooManyRevisionsError, SCMError
from rbtools.utils.checks import check_install
from rbtools.utils.filesystem import make_tempfile
from rbtools.utils.process import execute

class PlasticClient(SCMClient):
    """A client for Plastic SCM.

    This is a wrapper around the cm executable that fetches repository
    information and generates compatible diffs.
    """
    name = b'Plastic'
    supports_patch_revert = True
    REVISION_CHANGESET_PREFIX = b'cs:'

    def __init__(self, **kwargs):
        """Initialize the client.

        Args:
            **kwargs (dict):
                Keyword arguments to pass through to the superclass.
        """
        super(PlasticClient, self).__init__(**kwargs)

    def get_repository_info(self):
        """Return repository information for the current working tree.

        Returns:
            rbtools.clients.RepositoryInfo:
            The repository info structure.
        """
        if not check_install([b'cm', b'version']):
            logging.debug(b'Unable to execute "cm version": skipping Plastic')
            return None
        else:
            self.workspacedir = execute([b'cm', b'gwp', b'.', b'--format={1}'], split_lines=False, ignore_errors=True).strip()
            logging.debug(b'Workspace is %s', self.workspacedir)
            split = execute([b'cm', b'ls', self.workspacedir, b'--format={8}'], split_lines=True, ignore_errors=True)
            split = [ x for x in split if x ]
            m = re.search(b'^rep:(.+)$', split[0], re.M)
            if not m:
                return None
            path = m.group(1)
            return RepositoryInfo(path=path, local_path=path, supports_changesets=True, supports_parent_diffs=False)

    def parse_revision_spec(self, revisions=[]):
        """Parse the given revision spec.

        Args:
            revisions (list of unicode, optional):
                A list of revisions as specified by the user. Items in the list
                do not necessarily represent a single revision, since the user
                can use SCM-native syntaxes such as ``r1..r2`` or ``r1:r2``.
                SCMTool-specific overrides of this method are expected to deal
                with such syntaxes.

        Raises:
            rbtools.clients.errors.InvalidRevisionSpecError:
                The given revisions could not be parsed.

            rbtools.clients.errors.TooManyRevisionsError:
                The specified revisions list contained too many revisions.

        Returns:
            dict:
            A dictionary with the following keys:

            ``base`` (:py:class:`NoneType`):
                Always None.

            ``tip`` (:py:class:`unicode`):
                A revision to use as the tip of the resulting diff.

            These will be used to generate the diffs to upload to Review Board
            (or print). The Plastic implementation requires that one and only
            one revision is passed in. The diff for review will include the
            changes in the given changeset or branch.
        """
        n_revisions = len(revisions)
        if n_revisions == 0:
            raise InvalidRevisionSpecError(b'Either a changeset or a branch must be specified')
        else:
            if n_revisions == 1:
                return {b'base': None, 
                   b'tip': revisions[0]}
            raise TooManyRevisionsError
        return

    def diff(self, revisions, include_files=[], exclude_patterns=[], no_renames=False, extra_args=[]):
        """Perform a diff across all modified files in a Plastic workspace.

        Parent diffs are not supported (the second value in the tuple).

        Args:
            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

            include_files (list of unicode, optional):
                A list of files to whitelist during the diff generation.

            exclude_patterns (list of unicode, optional):
                A list of shell-style glob patterns to blacklist during diff
                generation.

            extra_args (list, unused):
                Additional arguments to be passed to the diff generation.

        Returns:
            dict:
            A dictionary containing the following keys:

            ``diff`` (:py:class:`bytes`):
                The contents of the diff to upload.

            ``changenum`` (:py:class:`unicode`):
                The number of the changeset being posted (if ``revisions``
                represents a single changeset).
        """
        changenum = None
        tip = revisions[b'tip']
        if tip.startswith(self.REVISION_CHANGESET_PREFIX):
            logging.debug(b'Doing a diff against changeset %s', tip)
            try:
                changenum = str(int(tip[len(self.REVISION_CHANGESET_PREFIX):]))
            except ValueError:
                pass

        else:
            logging.debug(b'Doing a diff against branch %s', tip)
            if not getattr(self.options, b'branch', None):
                self.options.branch = tip
        diff_entries = execute([
         b'cm', b'diff', tip, b'--format={status} {path} rev:revid:{revid} rev:revid:{parentrevid} src:{srccmpath} dst:{dstcmpath}{newline}'], results_unicode=False, split_lines=True)
        diff = self._process_diffs(diff_entries)
        return {b'diff': diff, 
           b'changenum': changenum}

    def _process_diffs(self, diff_entries):
        """Process the given diff entries.

        Args:
            diff_entries (list):
                The list of diff entries.

        Returns:
            bytes:
            The processed diffs.
        """
        diff_lines = []
        empty_filename = make_tempfile()
        tmp_diff_from_filename = make_tempfile()
        tmp_diff_to_filename = make_tempfile()
        for f in diff_entries:
            f = f.strip()
            if not f:
                continue
            m = re.search(b'(?P<type>[ACMD]) (?P<file>.*) (?P<revspec>rev:revid:[-\\d]+) (?P<parentrevspec>rev:revid:[-\\d]+) src:(?P<srcpath>.*) dst:(?P<dstpath>.*)$', f)
            if not m:
                raise SCMError(b'Could not parse "cm log" response: %s' % f)
            changetype = m.group(b'type')
            filename = m.group(b'file')
            if changetype == b'M':
                oldfilename = m.group(b'srcpath')
                oldspec = m.group(b'revspec')
                newfilename = m.group(b'dstpath')
                newspec = m.group(b'revspec')
                self._write_file(oldfilename, oldspec, tmp_diff_from_filename)
                dl = self._diff_files(tmp_diff_from_filename, empty_filename, oldfilename, b'rev:revid:-1', oldspec, changetype)
                diff_lines += dl
                self._write_file(newfilename, newspec, tmp_diff_to_filename)
                dl = self._diff_files(empty_filename, tmp_diff_to_filename, newfilename, newspec, b'rev:revid:-1', changetype)
                diff_lines += dl
            else:
                newrevspec = m.group(b'revspec')
                parentrevspec = m.group(b'parentrevspec')
                logging.debug(b'Type %s File %s Old %s New %s', changetype, filename, parentrevspec, newrevspec)
                old_file = new_file = empty_filename
                if changetype in ('A', ) or changetype in ('C', ) and parentrevspec == b'rev:revid:-1':
                    self._write_file(filename, newrevspec, tmp_diff_to_filename)
                    new_file = tmp_diff_to_filename
                elif changetype in ('C', ):
                    self._write_file(filename, parentrevspec, tmp_diff_from_filename)
                    old_file = tmp_diff_from_filename
                    self._write_file(filename, newrevspec, tmp_diff_to_filename)
                    new_file = tmp_diff_to_filename
                elif changetype in ('D', ):
                    self._write_file(filename, parentrevspec, tmp_diff_from_filename)
                    old_file = tmp_diff_from_filename
                else:
                    raise SCMError(b'Unknown change type "%s" for %s' % (
                     changetype, filename))
                dl = self._diff_files(old_file, new_file, filename, newrevspec, parentrevspec, changetype)
                diff_lines += dl

        os.unlink(empty_filename)
        os.unlink(tmp_diff_from_filename)
        os.unlink(tmp_diff_to_filename)
        return (b'').join(diff_lines)

    def _diff_files(self, old_file, new_file, filename, newrevspec, parentrevspec, changetype):
        """Do the work of producing a diff for Plastic.

        Args:
            old_file (bytes):
                The absolute path to the old file.

            new_file (bytes):
                The absolute path to the new file.

            filename (bytes):
                The file in the Plastic workspace.

            newrevspec (bytes):
                The revid spec of the new file.

            parentrevspec (bytes):
                The revid spec of the old file.

            changetype (bytes):
                The change type as a single character string.

        Returns:
            list of bytes:
            The computed diff.
        """
        if filename.startswith(self.workspacedir):
            filename = filename[len(self.workspacedir):]
        dl = execute([b'diff', b'-urN', old_file, new_file], extra_ignore_errors=(1,
                                                                                  2), results_unicode=False)
        dl = dl.replace(b'\r\r\n', b'\r\n')
        dl = dl.splitlines(True)
        if len(dl) == 1 and dl[0].startswith(b'Files %s and %s differ' % (
         old_file.encode(b'utf-8'),
         new_file.encode(b'utf-8'))):
            dl = [
             b'Binary files %s and %s differ\n' % (
              old_file.encode(b'utf-8'),
              new_file.encode(b'utf-8'))]
        if dl == [] or dl[0].startswith(b'Binary files '):
            if dl == []:
                return []
            dl.insert(0, b'==== %s (%s) ==%s==\n' % (
             filename, newrevspec, changetype))
            dl.append(b'\n')
        else:
            dl[0] = b'--- %s\t%s\n' % (filename, parentrevspec)
            dl[1] = b'+++ %s\t%s\n' % (filename, newrevspec)
            if dl[(-1)][(-1)] != b'\n':
                dl.append(b'\n')
        return dl

    def _write_file(self, filename, filespec, tmpfile):
        """Retrieve a file from Plastic and write it to a temp file.

        Args:
            filename (bytes):
                The filename to fetch.

            filespec (bytes):
                The revision of the file to fetch.

            tmpfile (unicode):
                The name of the temporary file to write to.
        """
        logging.debug(b'Writing "%s" (rev %s) to "%s"', filename.decode(b'utf-8'), filespec.decode(b'utf-8'), tmpfile)
        execute([b'cm', b'cat', filespec, b'--file=' + tmpfile])