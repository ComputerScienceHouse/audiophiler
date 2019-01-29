# audiophiler

[![Build Status](https://travis-ci.org/sgreene570/audiophiler.svg?branch=master)](https://travis-ci.org/sgreene570/audiophiler)

s3 audio file storage with templated front end.
<br>
Written for [Computer Science House](https://csh.rit.edu).  More info on the CSH wiki.
Allows house members to store audio files on an s3 bucket (backed by the CSH ceph rgw).
Files can be retrieved for listening through the web interface, or through the <code>get_harold</code> route.
Presigned s3 urls are handed out when the play button is clicked with a 302 return (to prevent the presigned url 
from expiring after the page is loaded).
<br>
TODO:
<br>
* Make front end easier to browse
* Use dynamic front end library (react?, or something)
* Switch over to boto3 instead of boto
* Move helper functions out of init.py

# Installation
From the root directory of the repo, setup a virtualenv with python3, then:
<br>
<code>python setup.py install</code>
<br>
or
<br>
<code>python setup.py develop</code>
# Running audiophiler
<code>export FLASK_APP=audiophiler</code>
<br>
<code>flask run</code>
<br>
See <code>config.py</code> for necessary environment variables.<br>
