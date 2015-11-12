# This import fixes sys.path issues
from .parentpath import *

import unittest
import mock
import json
import urllib2
from ogutils.web import operators

class WebOperatorsTest(unittest.TestCase):
    class MockResponse(object):
        def read(self):
            return 'success'

    class MockJSONResponse(object):
        def read(self):
            return json.dumps({'message': 'success'})

    @staticmethod
    def fail_first(req):
        if not isinstance(req, urllib2.Request):
            raise TypeError('bad open argument')
        if WebOperatorsTest.fail_first.data is not None and WebOperatorsTest.fail_first.data != req.data:
            raise AttributeError('bad data')
        if WebOperatorsTest.fail_first.headers is not None and \
           WebOperatorsTest.fail_first.headers != req.headers:
            raise AttributeError('bad headers')
        if WebOperatorsTest.fail_first.count == 0:
            return WebOperatorsTest.fail_first.response_class()
        else:
            WebOperatorsTest.fail_first.count -= 1
            raise ValueError('failed')

    def setUp(self):
        WebOperatorsTest.fail_first.count = 1
        self.data = {'test': 'ok?'}
        WebOperatorsTest.fail_first.data = self.data
        self.headers = {'Application-type': 'special'}
        WebOperatorsTest.fail_first.headers = self.headers
        WebOperatorsTest.fail_first.response_class = WebOperatorsTest.MockResponse

    @mock.patch('urllib2.urlopen')
    def test_simple_repeat_read_url(self, mock_urlopen):
        mock_urlopen.side_effect = WebOperatorsTest.fail_first
        mock_urlopen.side_effect.count = 1
        self.assertEqual(operators.repeat_read_url_request('http://foo.com', data=self.data,
                                                                             headers=self.headers),
                        'success')

    @mock.patch('urllib2.urlopen')
    def test_too_many_failures_repeat_read_url(self, mock_urlopen):
        mock_urlopen.side_effect = WebOperatorsTest.fail_first
        mock_urlopen.side_effect.count = 5
        with self.assertRaises(ValueError):
            operators.repeat_read_url_request('http://foo.com', retries=4, data=self.data,
                                                                headers=self.headers)

    @mock.patch('urllib2.urlopen')
    def test_simple_repeat_read_json_url(self, mock_urlopen):
        WebOperatorsTest.fail_first.response_class = WebOperatorsTest.MockJSONResponse
        mock_urlopen.side_effect = WebOperatorsTest.fail_first
        mock_urlopen.side_effect.count = 1
        self.assertDictEqual(operators.repeat_read_json_url_request('http://foo.com', data=self.data,
                                                                    headers=self.headers),
                            {'message': 'success'})

    @mock.patch('urllib2.urlopen')
    def test_too_many_failures_repeat_read_json_url(self, mock_urlopen):
        WebOperatorsTest.fail_first.response_class = WebOperatorsTest.MockJSONResponse
        mock_urlopen.side_effect = WebOperatorsTest.fail_first
        mock_urlopen.side_effect.count = 5
        with self.assertRaises(ValueError):
            operators.repeat_read_json_url_request('http://foo.com', retries=4,
                                                                     data=self.data,
                                                                     headers=self.headers)

if __name__ == "__main__":
    unittest.main()
