from __future__ import print_function


class CandidateError(BaseException):
    pass


CANDIDATE_MARK_KEY = "aws-staging-mark"


class CandidateChooser(object):

    def __init__(self, candidates, candidate_tag_name):
        self.candidates = candidates
        self.candidate_tag_name = candidate_tag_name

    def validate_candidates(self, connection):
        if not self.candidates:
            raise CandidateError("There are no AMIs tagged with {0}".format(
                self.candidate_tag_name))

        if len(self.candidates) > 1:
            raise CandidateError("There is more than one AMI tagged with {0}. Giving up.".format(
                self.candidate_tag_name))

    def choose_candidate(self, connection):
        sole_candidate = self.candidates[0]

        candidate_ami = sole_candidate.res_id
        connection.delete_tags(candidate_ami, {CANDIDATE_MARK_KEY: self.candidate_tag_name})

        print(candidate_ami)


class CandidateMarker(object):

    def __init__(self, candidate_tag_name, ami_id):
        self.candidate_tag_name = candidate_tag_name
        self.ami_id = ami_id

    def delete_existing_candidate_tags(self, connection):
        existing_tags = connection.get_all_tags(
            filters={
                "resource-type": "image",
                "key": CANDIDATE_MARK_KEY,
                "value": self.candidate_tag_name,
            })

        if existing_tags:
            connection.delete_tags(
                [tag.res_id for tag in existing_tags],
                {
                    CANDIDATE_MARK_KEY: self.candidate_tag_name
                })

    def mark_candidate(self, connection):
        connection.create_tags([self.ami_id], {
            CANDIDATE_MARK_KEY: self.candidate_tag_name,
        })
