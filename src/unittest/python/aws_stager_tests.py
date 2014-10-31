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

from unittest import TestCase

from mock import patch, Mock

from aws_stager import fetch_candidate


class AwsStagerTests(TestCase):

    def setUp(self):
        self.print_patcher = patch("aws_stager.candidates.print", create=True)
        self.print_patcher.start()

    def tearDown(self):
        self.print_patcher.stop()

    @patch("aws_stager.connect_to_region")
    def test_should_connect_to_given_region(self, connect_to_region):
        fetch_candidate("any-aws-region", "any-tag-name")

        connect_to_region.assert_called_with("any-aws-region")

    @patch("aws_stager.connect_to_region")
    def test_should_fetch_all_potential_candidates(self, connect_to_region):
        fetch_candidate("any-aws-region", "any-tag-name")

        connection = connect_to_region.return_value
        connection.get_all_tags.assert_called_with(
            filters={
                'resource-type': 'image',
                'value': 'any-tag-name',
                'key': 'aws-staging-mark'
            })

    @patch("aws_stager.CandidateChooser")
    @patch("aws_stager.connect_to_region")
    def test_should_choose_from_candidates(self, connect_to_region, candidate_chooser):
        connection = connect_to_region.return_value
        candidate_tag = Mock(res_id="any-ami-id")
        connection.get_all_tags.return_value = [candidate_tag]

        fetch_candidate("any-aws-region", "any-tag-name")

        candidate_chooser.assert_called_with([candidate_tag], "any-tag-name")
