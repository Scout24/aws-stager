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
