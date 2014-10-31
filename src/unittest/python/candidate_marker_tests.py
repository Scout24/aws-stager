#  The MIT License (MIT)
#
#  Copyright (c) 2014 ImmobilienScout GmbH
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import unittest

from mock import Mock

from aws_stager.candidates import CandidateMarker


class CandidateMarkerTest(unittest.TestCase):

    def setUp(self):
        self.connection = Mock()
        self.candidate_marker = CandidateMarker("any-tag-name", "any-ami-id")

    def test_should_delete_existing_candidate_tags(self):
        self.connection.get_all_tags.return_value = [Mock(res_id="tag-1"),
                                                     Mock(res_id="tag-2")]

        self.candidate_marker.delete_existing_candidate_tags(self.connection)

        self.connection.get_all_tags.assert_called_with(
            filters={
                'resource-type': 'image',
                'value': 'any-tag-name',
                'key': 'aws-staging-mark'
            })
        self.connection.delete_tags.assert_called_with(
            ['tag-1', 'tag-2'],
            {'aws-staging-mark': 'any-tag-name'})

    def test_should_mark_candidate(self):
        self.candidate_marker.mark_candidate(self.connection)

        self.connection.create_tags.assert_called_with(
            ['any-ami-id'],
            {'aws-staging-mark': 'any-tag-name'},
        )
