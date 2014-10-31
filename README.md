aws-stager [![Build Status](https://travis-ci.org/ImmobilienScout24/aws-stager.svg?branch=master)](https://travis-ci.org/ImmobilienScout24/aws-stager)[![Coverage Status](https://img.shields.io/coveralls/ImmobilienScout24/aws-stager.svg)](https://coveralls.io/r/ImmobilienScout24/aws-stager)
==========

Stage your AMIs using EC2 tags.


Intent
======
Allow separated build steps to share AMI-ids through the AWS tagging feature.

Minimal example:

### Build config 1:

* Build ami, deploy it
* Run system tests on it
* Tag it with `deploy-tested`

### Build config 2:

* Fetch ami tagged with `deploy-tested`, deploy it to prod environment.


Usage
=====


### `aws-tag-candidate AMI_ID CANDIDATE_TAG_NAME`


Tags the ami defined by `AMI_ID` with 
`"aws-staging-mark" = CANDIDATE_TAG_NAME`
All tags are delete from AMIs previously tagged with this key/value pair.


The AMI-id will then be available for retrieval by your build chain using :

### `aws-fetch-candidate CANDIDATE_TAG_NAME`

Outputs the AMI-id (and nothing else) in case there is exactly one AMI
tagged with 
`"aws-staging-mark" = CANDIDATE_TAG_NAME`

In case several (or no) AMIs have this tag, this will produce an error.


License
=======
MIT. See license file.
