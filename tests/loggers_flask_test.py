# This import fixes sys.path issues
from .parentpath import *

import os
import re
import unittest
import logging
import StringIO
from ogutils.loggers import flask
from ogutils.system import streams

LOCAL_LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')

class FlaskLoggerTest(unittest.TestCase):
    def clear_logs(self):
        for fname in os.listdir(LOCAL_LOG_DIR):
            file_path = os.path.join(LOCAL_LOG_DIR, fname)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def read_console_log(self):
        with open(os.path.join(LOCAL_LOG_DIR, 'console.log'), 'r') as console:
            return ''.join(console.readlines())

    def setUp(self):
        if not os.path.exists(LOCAL_LOG_DIR):
            os.makedirs(LOCAL_LOG_DIR)
        self.clear_logs()
        self.log_matcher = re.compile('\[\d\d\/[\w]+\/\d\d\d\d \d\d:\d\d:\d\d\] Log Me!\n')
        self.logger = flask.build_flask_like_logger(
            'flask_logger',
            log_level=logging.INFO,
            log_dir=LOCAL_LOG_DIR)

    def tearDown(self):
        self.logger.handlers = []
        self.clear_logs()

    def test_logger_default_level(self):
        self.logger.debug('Skip me')
        self.assertEquals(self.read_console_log(), '')

    def test_logger_stdout(self):
        stdout = StringIO.StringIO()
        with streams.StdRedirector(stdout=stdout):
            self.assertEqual(len(re.findall(self.log_matcher, self.read_console_log())), 0)
            self.logger.info('Log Me!')
            self.assertEqual(len(re.findall(self.log_matcher, self.read_console_log())), 1)
            self.assertEqual(len(re.findall(self.log_matcher, stdout.getvalue())), 1)
            self.logger.info('Log Me!')
            self.assertEqual(len(re.findall(self.log_matcher, self.read_console_log())), 2)
            self.assertEqual(len(re.findall(self.log_matcher, stdout.getvalue())), 2)

    def test_logger_stderr(self):
        stderr = StringIO.StringIO()
        with streams.StdRedirector(stderr=stderr):
            self.assertEqual(len(re.findall(self.log_matcher, self.read_console_log())), 0)
            self.logger.error('Log Me!')
            self.assertEqual(len(re.findall(self.log_matcher, self.read_console_log())), 1)
            self.assertEqual(len(re.findall(self.log_matcher, stderr.getvalue())), 1)
            self.logger.error('Log Me!')
            self.assertEqual(len(re.findall(self.log_matcher, self.read_console_log())), 2)
            self.assertEqual(len(re.findall(self.log_matcher, stderr.getvalue())), 2)

if __name__ == "__main__":
    unittest.main()
