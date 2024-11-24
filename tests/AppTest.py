from unittest.mock import patch
import unittest
from http import HTTPStatus
import logging
from flaskr import before_server_stop, create_app
from flaskr.infrastructure.databases.postgres.db import Session

class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the Flask app with the test configuration
        cls.app = create_app('default')
        cls.client = cls.app.test_client()

        # Create application context
        with cls.app.app_context():
            # Any setup you need to do, e.g., creating test data
            pass
        
    @patch('logging.Logger.info', wraps=logging.getLogger('default').info)
    def test_should_calling_log_info_before_server_stop(self, info_mock):
        expectedInfo = 'Closing application ...'
        
        before_server_stop()

        info_mock.assert_called_once_with(expectedInfo)

    @classmethod
    def tearDownClass(cls):
        Session.remove()