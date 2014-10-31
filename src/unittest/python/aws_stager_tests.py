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
