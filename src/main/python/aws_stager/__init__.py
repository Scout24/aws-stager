from boto.ec2 import connect_to_region
from candidates import CandidateChooser


def fetch_candidate(region, candidate_tag_name):
    connection = connect_to_region("eu-west-1")
    candidates = connection.get_all_tags(filters={
                                         "resource-type": "image",
                                         "key": candidate_tag_name,
                                         })

    candidate_chooser = CandidateChooser(candidates, candidate_tag_name)

    candidate_chooser.validate_candidates(connection)

    candidate_chooser.choose_candidate(connection)
