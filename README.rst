Flask-sacct
============
Flask-sacct is a Flask webservice that allows an easy web access to 
`Slurm <http://slurm.schedmd.com/>`_ accounting database (sacct).
Sacct information are returned in JSON indexed by jobid.

Dependencies
-----------

- `Flask <http://flask.pocoo.org/>`_
- `Slurm <http://slurm.schedmd.com/>`_

Installation
------------

Install the extension with `pip` ::

    $ pip install git+git://github.com/julcollas/flask-sacct.git

or alternatively if you don't have pip installed ::

    $ python setup.py install

How to Use
----------
::

    $ flask-sacct --host 0.0.0.0 --debug --sacct /my/path/to/sacct --port 1234

Ressources
----------

    /sacct/user/<username>

    /sacct/users/?user=<username>&user=<username>

    /sacct/job/<jobid>

    /sacct/jobs/?job=<jobid>&job=<jobid>

    /sacct/account/<account>

    /sacct/accounts/?account=<account>&account=<account>

Optionals arguments for all ressources except job

    starttime=<starttime>

    endtime=<endtime>

Time format is the one used by sacct

Exemples
---------
::

    curl -s http://localhost:1234/sacct/user/julien?starttime=2014-07-14T12:00&endtime=2014-07-14T16:00

    curl -s http://localhost:1234/sacct/jobs/?job=1234&job=4242
