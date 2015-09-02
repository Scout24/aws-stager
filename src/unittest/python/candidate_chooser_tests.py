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

from mock import Mock, patch

from aws_stager.candidates import CandidateChooser, CandidateError


class CandidateChooserTest(unittest.TestCase):

    def test_should_enforce_at_least_one_candidate_found(self):
        candidate_chooser = CandidateChooser([], "any-tag-name")
        self.assertRaises(CandidateError,
                          candidate_chooser.choose_candidate)

    def test_should_enforce_no_more_than_one_candidate_found(self):
        candidate_chooser = CandidateChooser([Mock(), Mock()],
                                             "any-tag-name")
        self.assertRaises(CandidateError,
                          candidate_chooser.choose_candidate)

    @patch("aws_stager.candidates.print", create=True)
    def test_should_print_candidate(self, _print):
        candidate_chooser = CandidateChooser([Mock(res_id="candidate")], "any-tag-name")

        candidate_chooser.choose_candidate()

        _print.assert_called_with("candidate")
