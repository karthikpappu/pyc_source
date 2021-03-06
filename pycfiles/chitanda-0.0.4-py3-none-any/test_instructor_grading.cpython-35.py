# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/tests/integration/cli/test_instructor_grading.py
# Compiled at: 2018-10-02 19:35:34
# Size of source mod 2**32: 1161 bytes
from chisubmit.tests.common import cli_test, ChisubmitCLITestCase

class CLIInstructorGrades(ChisubmitCLITestCase):
    fixtures = [
     'users', 'course1', 'course1_users', 'course1_teams',
     'course1_pa1', 'course1_pa1_registrations_with_submissions',
     'course1_pa1_grades',
     'course1_pa2']

    @cli_test
    def test_instructor_list_grades(self, runner):
        _, instructors, _, _ = self.create_clients(runner, 'admin', instructor_ids=['instructor1'], course_id='cmsc40100')
        instructor1 = instructors[0]
        result = instructor1.run('instructor grading list-grades --detailed')
        self.assertEqual(result.exit_code, 0)

    @cli_test
    def test_instructor_grading_status(self, runner):
        _, instructors, _, _ = self.create_clients(runner, 'admin', instructor_ids=['instructor1'], course_id='cmsc40100')
        instructor1 = instructors[0]
        result = instructor1.run('instructor grading show-grading-status --use-stored-grades --by-grader', ['pa1'])
        self.assertEqual(result.exit_code, 0)