# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/teamscale_precommit_client/precommit_client.py
# Compiled at: 2020-04-21 02:31:18
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import datetime, time, os, sys, argparse
from teamscale_precommit_client.git_utils import get_current_branch, get_current_timestamp
from teamscale_precommit_client.git_utils import get_changed_files_and_content, get_deleted_files
from teamscale_precommit_client.data import PreCommitUploadData
from teamscale_client import TeamscaleClient
from teamscale_precommit_client.client_configuration_utils import get_teamscale_client_configuration
from teamscale_precommit_client.git_utils import get_repo_root_from_file_in_repo
PRECOMMIT_CONFIG_FILENAME = b'.teamscale-precommit.config'

class PrecommitClient:
    """Client for precommit analysis"""
    PRECOMMIT_WAITING_TIME_IN_SECONDS = 2

    def __init__(self, teamscale_config, repository_path, analyzed_file=None, verify=True, omit_links_to_findings=False, exclude_findings_in_changed_code=False, fetch_existing_findings=False, fetch_all_findings=False, fetch_existing_findings_in_changes=False, fail_on_red_findings=False, log_to_stderr=False):
        """Constructor"""
        self.teamscale_client = TeamscaleClient(teamscale_config.url, teamscale_config.username, teamscale_config.access_token, teamscale_config.project_id, verify)
        self.repository_path = repository_path
        self.analyzed_file = analyzed_file
        self.omit_links_to_findings = omit_links_to_findings
        self.exclude_findings_in_changed_code = exclude_findings_in_changed_code
        self.fetch_existing_findings = fetch_existing_findings
        self.fetch_all_findings = fetch_all_findings
        self.fetch_existing_findings_in_changes = fetch_existing_findings_in_changes
        self.fail_on_red_findings = fail_on_red_findings
        self.log_to_stderr = log_to_stderr
        self.changed_files = {}
        self.deleted_files = []
        self.added_findings = []
        self.removed_findings = []
        self.existing_findings = []
        self.findings_in_changed_code = []
        self.current_branch = b''
        self.parent_commit_timestamp = 0

    def run(self):
        """Performs the precommit analysis. Depending on the modifications made and the flags provided to the client,
        this triggers precommit analysis or just queries existing findings."""
        self._calculate_modifications()
        self._retrieve_current_branch()
        self._retrieve_parent_commit_timestamp()
        if self.changed_files or self.deleted_files:
            self._do_precommit_analysis()
            self._print_precommit_results_as_error_string()
        elif not self.fetch_all_findings and not self.fetch_existing_findings:
            print(b'No changed files found. Did you forget to `git add` new files?')
            exit(0)
        if self.fetch_existing_findings_in_changes:
            self._get_existing_findings_in_changes()
            self._print_findings(b'Existing findings:', self.existing_findings, self._get_precommit_branch())
        elif self.fetch_existing_findings or self.fetch_all_findings:
            self._get_existing_findings()
            self._print_findings(b'Existing findings:', self.existing_findings, self.current_branch)
        if self.fail_on_red_findings and self._did_precommit_analysis_yield_red_findings():
            exit(1)

    def _calculate_modifications(self):
        """Calculates the changed and deleted files in the repository."""
        if not self.repository_path or not os.path.exists(self.repository_path) or not os.path.isdir(self.repository_path):
            raise RuntimeError(b'Invalid path to file in repository: %s' % self.repository_path)
        self.changed_files = get_changed_files_and_content(self.repository_path)
        self.deleted_files = get_deleted_files(self.repository_path)

    def _retrieve_current_branch(self):
        """Retrieves the current branch from the repository."""
        self.current_branch = get_current_branch(self.repository_path)

    def _retrieve_parent_commit_timestamp(self):
        """Retrieves the commit timestamp from the repository."""
        self.parent_commit_timestamp = int(get_current_timestamp(self.repository_path))

    def _do_precommit_analysis(self):
        """Uploads changed and deleted files to Teamscale, waits for the results, and interprets them."""
        self._upload_precommit_data()
        time.sleep(PrecommitClient.PRECOMMIT_WAITING_TIME_IN_SECONDS)
        print(b'Waiting for precommit analysis results...')
        print(b'')
        self._wait_and_get_precommit_result()

    def _upload_precommit_data(self):
        """Uploads the currently changed files for precommit analysis."""
        self.teamscale_client.branch = self.current_branch
        print(b"Uploading changes on branch '%s' in '%s'..." % (self.current_branch, self.repository_path))
        precommit_data = PreCommitUploadData(uniformPathToContentMap=self.changed_files, deletedUniformPaths=self.deleted_files)
        self.teamscale_client.upload_files_for_precommit_analysis(datetime.datetime.fromtimestamp(self.parent_commit_timestamp), precommit_data)

    def _wait_and_get_precommit_result(self):
        """Gets the current precommit results. Waits synchronously until server is ready. """
        self.added_findings, self.removed_findings, self.findings_in_changed_code = self.teamscale_client.get_precommit_analysis_results()

    def _get_precommit_branch(self):
        """Returns the precommit branch of the current user."""
        return b'__precommit__%s' % self.teamscale_client.username

    def _print_findings(self, message, findings, branch):
        """Print the specified list of findings for the specified branch, in a way most text editors understand. """
        log_to_stderr = self.log_to_stderr and len(findings) > 0
        self._print(b'', log_to_stderr)
        self._print(message, log_to_stderr)
        for formatted_finding in self._format_findings(findings, branch):
            self._print(formatted_finding, log_to_stderr)

    @staticmethod
    def _print(message, print_to_err=False):
        if print_to_err:
            print(message, file=sys.stderr)
        else:
            print(message)

    def _print_precommit_results_as_error_string(self):
        """Print the current precommit results formatting them in a way, most text editors understand."""
        branch = self._get_precommit_branch()
        self._print_findings(b'New findings:', self.added_findings, branch)
        if not self.exclude_findings_in_changed_code:
            self._print_findings(b'Findings in changed code:', self.findings_in_changed_code, branch)

    def _did_precommit_analysis_yield_red_findings(self):
        """Returns whether the analysis resulted in any RED findings."""
        added_red_findings = list(filter(lambda finding: finding.assessment == b'RED', self.added_findings))
        return len(added_red_findings) > 0

    def _get_existing_findings(self):
        """Gets the existing findings. This either fetches the findings in the path specified by the call to the script
        or all findings if `fetch_all_findings` is `True`."""
        if self.changed_files or self.deleted_files:
            self.teamscale_client.branch = self._get_precommit_branch()
        else:
            self.teamscale_client.branch = self.current_branch
        uniform_path = os.path.relpath(self.analyzed_file, self.repository_path)
        if self.fetch_all_findings:
            uniform_path = b''
        self.existing_findings = self.teamscale_client.get_findings(uniform_path=uniform_path, timestamp=None)
        self._remove_precommit_findings_from_existing_findings()
        return

    def _remove_precommit_findings_from_existing_findings(self):
        """Ensures no precommit findings are among the existing findings."""
        self.existing_findings = [ finding for finding in self.existing_findings if finding not in self.added_findings and finding not in self.removed_findings and finding not in self.findings_in_changed_code
                                 ]

    def _get_existing_findings_in_changes(self):
        """Gets the existing findings in the changed files."""
        self.teamscale_client.branch = self._get_precommit_branch()
        self.existing_findings = []
        for uniform_path in self.changed_files:
            self.existing_findings.extend(self.teamscale_client.get_findings(uniform_path=uniform_path, timestamp=None))

        self._remove_precommit_findings_from_existing_findings()
        return

    def _format_findings(self, findings, branch):
        """Formats the given findings as error or warning strings."""
        self.teamscale_client.branch = branch
        if len(findings) == 0:
            return [b'> No findings.']
        else:
            sorted_findings = sorted(findings)
            if self.omit_links_to_findings:
                return [ b'%s:%i:1: %s: %s' % (os.path.join(self.repository_path, finding.uniformPath), finding.startLine, self._get_finding_severity_message(finding=finding), finding.message) for finding in sorted_findings
                       ]
            return [ b'%s:%i:1: %s: %s (%s)' % (os.path.join(self.repository_path, finding.uniformPath), finding.startLine, self._get_finding_severity_message(finding=finding), finding.message, b'%s&t=%s' % (self.teamscale_client.get_finding_url(finding), self.teamscale_client._get_timestamp_parameter(timestamp=None))) for finding in sorted_findings
                   ]
            return

    @staticmethod
    def _get_finding_severity_message(finding):
        """Formats the given finding's assessment as severity."""
        if finding.assessment == b'RED':
            return b'error'
        return b'warning'


def _parse_args():
    """Parses the precommit client command line arguments."""
    parser = argparse.ArgumentParser(description=b'Precommit analysis client for Teamscale.')
    parser.add_argument(b'path', metavar=b'path', type=str, nargs=1, help=b'path to any file in the repository')
    parser.add_argument(b'--exclude-findings-in-changed-code', dest=b'exclude_findings_in_changed_code', action=b'store_const', const=True, default=False, help=b'Determines whether to exclude findings in changed code (default: False)')
    parser.add_argument(b'--fetch-existing-findings', dest=b'fetch_existing_findings', action=b'store_const', const=True, default=False, help=b'When this option is set, existing findings in the specified file are fetched in addition to precommit findings. (default: False)')
    parser.add_argument(b'--fetch-existing-findings-in-changes', dest=b'fetch_existing_findings_in_changes', action=b'store_const', const=True, default=False, help=b'When this option is set, existing findings in all changed files are fetched in addition to precommit findings. (default: False)')
    parser.add_argument(b'--fetch-all-findings', dest=b'fetch_all_findings', action=b'store_const', const=True, default=False, help=b'When this option is set, all existing findings in the repo are fetched in addition to precommit findings. (default: False)')
    parser.add_argument(b'--fail-on-red-findings', dest=b'fail_on_red_findings', action=b'store_const', const=True, default=False, help=b'When this option is set, the precommit client will exit with a non-zero return value whenever RED findings were among the precommit findings. (default: False)')
    parser.add_argument(b'--omit-links-to-findings', dest=b'omit_links_to_findings', action=b'store_const', const=True, default=False, help=b'By default, each finding includes a link to the corresponding finding in Teamscale. Setting this option omits these links. (default: False)')
    parser.add_argument(b'--verify', default=True, type=_bool_or_string, help=b"Path to different certificate file. See requests' verify parameter in http://docs.python-requests.org/en/latest/user/advanced/#ssl-cert-verification.\nOther possible values: True, False (default: True)")
    parser.add_argument(b'--log-to-stderr', dest=b'log_to_stderr', action=b'store_true', help=b'When this option is set, any finding will be logged to stderr instead of stdout: (default: False)')
    return parser.parse_args()


def _bool_or_string(string):
    """Helper to interpret different ways of specifying boolean values."""
    if string in ('t', 'true', 'True'):
        return True
    if string in ('f', 'false', 'False'):
        return False
    return string


def _configure_precommit_client(parsed_args):
    """Reads the precommit analysis configuration and creates a precommit client with the corresponding config."""
    path_to_file_in_repo = parsed_args.path[0]
    repo_path = get_repo_root_from_file_in_repo(os.path.normpath(path_to_file_in_repo))
    config_file = os.path.join(repo_path, PRECOMMIT_CONFIG_FILENAME)
    config = get_teamscale_client_configuration(config_file)
    return PrecommitClient(config, repository_path=repo_path, analyzed_file=path_to_file_in_repo, verify=parsed_args.verify, omit_links_to_findings=parsed_args.omit_links_to_findings, exclude_findings_in_changed_code=parsed_args.exclude_findings_in_changed_code, fetch_existing_findings=parsed_args.fetch_existing_findings, fetch_all_findings=parsed_args.fetch_all_findings, fetch_existing_findings_in_changes=parsed_args.fetch_existing_findings_in_changes, fail_on_red_findings=parsed_args.fail_on_red_findings, log_to_stderr=parsed_args.log_to_stderr)


def run():
    """Performs precommit analysis."""
    parsed_args = _parse_args()
    precommit_client = _configure_precommit_client(parsed_args)
    precommit_client.run()


if __name__ == b'__main__':
    run()