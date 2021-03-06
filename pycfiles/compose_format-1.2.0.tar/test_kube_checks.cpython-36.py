# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_kube_checks.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 6254 bytes
from nose.tools import raises
from unittest import TestCase
from compose_flow.kube.checks import BaseChecker, ManifestChecker, AnswersChecker, ValuesChecker
from tests.utils import get_content

class TestCheckerNoPrefix(BaseChecker):
    pass


class TestCheckerSingleCheck(BaseChecker):
    check_prefix = '_test_check_'

    def _test_check_noop(self, rendered: str) -> None:
        pass


class TestCheckerAlwaysError(BaseChecker):
    check_prefix = '_test_check_'

    def _test_check_always_return(self, rendered: str) -> str:
        return 'Fail!'


class TestBaseChecker(TestCase):

    @raises(AttributeError)
    def test_no_checks(self):
        """Ensure checker without a check_prefix errors out"""
        checker = TestCheckerNoPrefix()
        checker.check('')

    def test_noop_check(self):
        """Ensure checker with a single dummy checker runs"""
        checker = TestCheckerSingleCheck()
        errors = checker.check('')
        assert len(errors) == 0

    def test_always_error_check(self):
        """Ensure checker with check that returns an error actually returns a list of errors"""
        checker = TestCheckerAlwaysError()
        errors = checker.check('')
        if not len(errors) > 0:
            raise AssertionError
        elif not 'Fail!' in errors:
            raise AssertionError


class TestManifestChecker(TestCase):

    def setUp(self):
        self.checker = ManifestChecker()

    def test_invalid_zalando_ingress(self):
        """Ensure ManifestChecker returns an error for invalid Zalando ingress manifest"""
        content = get_content('manifests/invalid-zalando-ingress.yaml')
        errors = self.checker.check(content)
        assert len(errors) > 0

    def test_internal_zalando_ingress(self):
        """Ensure ManifestChecker does not return an error for internal Zalando ingress manifest"""
        content = get_content('manifests/internal-zalando-ingress.yaml')
        errors = self.checker.check(content)
        assert not errors

    def test_external_zalando_ingress(self):
        """
        Ensure ManifestChecker does not return an error for an explicitly
        internet-facing Zalando ingress manifest
        """
        content = get_content('manifests/external-zalando-ingress.yaml')
        errors = self.checker.check(content)
        assert not errors

    def test_nginx_ingress(self):
        """
        Ensure ManifestChecker does not return an error for an NGINX ingress
        """
        content = get_content('manifests/nginx-ingress.yaml')
        errors = self.checker.check(content)
        assert not errors

    def test_multidoc_invalid_ingress(self):
        """
        Ensure ManifestChecker returns an error for a multi-document manifest including a single invalid Ingress
        """
        content = get_content('manifests/invalid-ingress-multidoc.yaml')
        errors = self.checker.check(content)
        assert len(errors) > 0

    def test_no_resources_job(self):
        """
        Ensure ManifestChecker returns an error for a Job with no resources
        """
        content = get_content('manifests/no-resources-job.yaml')
        errors = self.checker.check(content)
        assert len(errors) > 0

    def test_no_limits_deployment(self):
        """
        Ensure ManifestChecker returns an error for a Deployment with no limits
        """
        content = get_content('manifests/no-limits-deployment.yaml')
        errors = self.checker.check(content)
        assert len(errors) > 0

    def test_good_job(self):
        """
        Ensure ManifestChecker does not return an error for a good Job
        """
        content = get_content('manifests/good-job.yaml')
        errors = self.checker.check(content)
        assert not errors

    def test_good_cronjob(self):
        """
        Ensure ManifestChecker does not return an error for a valid CronJob
        """
        content = get_content('manifests/good-cronjob.yaml')
        errors = self.checker.check(content)
        assert not errors

    def test_good_init_deployment(self):
        """
        Ensure ManifestChecker does not return an error for a deployment with init containers
        """
        content = get_content('manifests/good-init-deployment.yaml')
        errors = self.checker.check(content)
        assert not errors


class TestAnswersChecker(TestCase):

    def setUp(self):
        self.checker = AnswersChecker()

    def test_multidoc_resources(self):
        """
        Ensure AnswersChecker returns an error for a multi-document answers file
        """
        content = get_content('answers/multidoc-answers.yaml')
        errors = self.checker.check(content)
        assert len(errors) > 0

    def test_no_limits_answers(self):
        """
        Ensure AnswersChecker returns an error for flat answers with resources but no limits
        """
        content = get_content('answers/no-limits-answers.yaml')
        errors = self.checker.check(content)
        assert len(errors) > 0

    def test_no_requests_answers(self):
        """
        Ensure AnswersChecker returns an error for flat answers with resources but no requests
        """
        content = get_content('answers/no-requests-answers.yaml')
        errors = self.checker.check(content)
        assert len(errors) > 0

    def test_good_resources_answers(self):
        """
        Ensure AnswersChecker returns no error for answers with proper resources
        """
        content = get_content('answers/good-resources-answers.yaml')
        errors = self.checker.check(content)
        assert not errors


class TestValuesChecker(TestCase):

    def setUp(self):
        self.checker = ValuesChecker()

    def test_multidoc_resources(self):
        """
        Ensure ValuesChecker returns an error for a multi-document values file
        """
        content = get_content('values/multidoc-values.yaml')
        errors = self.checker.check(content)
        assert len(errors) > 0

    def test_good_resources_answers(self):
        """
        Ensure ValuesChecker returns no errors for values with proper resources
        """
        content = get_content('values/good-resources-values.yaml')
        errors = self.checker.check(content)
        assert not errors