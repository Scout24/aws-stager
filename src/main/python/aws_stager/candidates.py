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
