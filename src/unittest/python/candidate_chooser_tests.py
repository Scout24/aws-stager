import unittest

from mock import Mock, patch

from aws_stager.candidates import CandidateChooser, CandidateError


class CandidateChooserTest(unittest.TestCase):

    def test_should_enforce_at_least_one_candidate_found(self):
        candidate_chooser = CandidateChooser([], "any-tag-name")
        self.assertRaises(CandidateError,
                          candidate_chooser.validate_candidates, Mock())

    def test_should_enforce_no_more_than_one_candidate_found(self):
        candidate_chooser = CandidateChooser([Mock(), Mock()],
                                             "any-tag-name")
        self.assertRaises(CandidateError,
                          candidate_chooser.validate_candidates, Mock())

    def test_should_delete_all_candidate_tags_when_more_than_one_candidate_found(self):
        candidate_chooser = CandidateChooser([Mock(res_id="c1"), Mock(res_id="c2")],
                                             "any-tag-name")
        connection = Mock()

        self.assertRaises(CandidateError,
                          candidate_chooser.validate_candidates, connection)
        connection.delete_tags.assert_called_with(['c1', 'c2'], ['any-tag-name'])

    @patch("aws_stager.candidates.print", create=True)
    def test_should_print_candidate(self, _print):
        candidate_chooser = CandidateChooser([Mock(res_id="candidate")], "any-tag-name")

        candidate_chooser.choose_candidate(Mock())

        _print.assert_called_with("candidate")
