class CandidateError(BaseException):
    pass


class CandidateChooser(object):

    def __init__(self, candidates, candidate_tag_name):
        self.candidates = candidates
        self.candidate_tag_name = candidate_tag_name

    def validate_candidates(self, connection):
        if not self.candidates:
            raise CandidateError("There are no AMIs tagged with {0}".format(
                self.candidate_tag_name))

        if len(self.candidates) > 1:
            connection.delete_tags([c.res_id for c in self.candidates],
                                   [self.candidate_tag_name])
            raise CandidateError("There is more than one AMI tagged with {0}. Removed all tags.".format(
                self.candidate_tag_name))

    def choose_candidate(self, connection):
        sole_candidate = self.candidates[0]

        candidate_ami = sole_candidate.res_id
        connection.delete_tags(candidate_ami, [self.candidate_tag_name])

        print(candidate_ami)
