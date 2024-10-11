from unittest.mock import patch

from psycopg2 import OperationalError as PsycopgError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch('main.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """test waiting for database if database ready"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])
        
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """test waiting for database when getting OperationalError"""
        # psycopg error (raised as operationalerror from postgres)
        # is raised when database is not accepting connections

        # operational error (also raised as operational error)
        # is raised by django when the database is accepting connections
        # but django is unable to find all the requirements needed to run
        patched_check.side_effect = [PsycopgError] * 2 + \
            [OperationalError] * 3 + [True]
        
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])