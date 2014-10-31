from boto.ec2 import connect_to_region
from candidates import CandidateChooser, CANDIDATE_MARK_KEY


def fetch_candidate(region, candidate_tag_name):
    connection = connect_to_region(region)
    candidates = connection.get_all_tags(filters={
                                         "resource-type": "image",
                                         "key": CANDIDATE_MARK_KEY,
                                         "value": candidate_tag_name
                                         })

    candidate_chooser = CandidateChooser(candidates, candidate_tag_name)

    candidate_chooser.validate_candidates(connection)

    candidate_chooser.choose_candidate(connection)
