from unittest import TestCase

from mock import patch

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
