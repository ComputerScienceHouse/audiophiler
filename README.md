# audiophiler
s3 audio file storage with templated front end.
<br>
Currently uses [csh bootstrap](https://github.com/ComputerScienceHouse/csh-material-bootstrap)
and [dropzone](https://github.com/enyo/dropzone) as submodules for front end design.
Written for [Computer Science House](https://csh.rit.edu).  Soon to be the new HAROLD system for CSH.
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
See the example <code>config.sample.py</code> to add any necessary runtime variables.
