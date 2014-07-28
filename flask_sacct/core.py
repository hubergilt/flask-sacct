from flask import Flask, request, jsonify
from optparse import OptionParser
import subprocess
import csv

app = Flask(__name__)


def run_sacct(arguments):
    cmd = '''%s --parsable2 --format ALL %s''' % (sacct, arguments)
    app.logger.debug('cmd: %s' % cmd)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, _stderr = process.communicate()
    data = {}
    if process.returncode == 0:
        for line in csv.DictReader(stdout.decode('ascii').splitlines(),
                                   delimiter='|'):
            jobid = line.pop('JobID')
            data[jobid] = line
    else:
        data = 'sacct failed with return code "%s"' % str(process.returncode)

    return data


def parse_request(request):
    ret_val = ''
    if 'starttime' in request.args:
        starttime = request.args.get('starttime')
        ret_val += ' --starttime=%s ' % starttime
    if 'endtime' in request.args:
        endtime = request.args.get('endtime')
        ret_val += ' --endtime=%s ' % endtime

    return ret_val


@app.route('/sacct/user/<username>', methods=['GET'])
def sacct_user(username):
    time_args = parse_request(request)
    app.logger.debug('username: %s' % username)
    app.logger.debug('time: %s' % time_args)
    result = run_sacct('%s --user=%s' % (time_args, username))
    return jsonify(result)


@app.route('/sacct/job/<job>', methods=['GET'])
def sacct_job(job):
    app.logger.debug('job: %s' % job)
    result = run_sacct('--jobs=%s' % job)
    return jsonify(result)


@app.route('/sacct/account/<account>', methods=['GET'])
def sacct_account(account):
    time_args = parse_request(request)
    app.logger.debug('account: %s' % account)
    app.logger.debug('time: %s' % time_args)
    result = run_sacct('%s --allusers --account=%s' % (time_args, account))
    return jsonify(result)


@app.route('/sacct/users/', methods=['GET'])
def sacct_users():
    time_args = parse_request(request)
    users = request.values.getlist('user')
    app.logger.debug('users: %s' % str(users))
    app.logger.debug('time: %s' % time_args)
    result = run_sacct('%s --user=%s' % (time_args, ','.join(users)))
    return jsonify(result)


@app.route('/sacct/jobs/', methods=['GET'])
def sacct_jobs():
    time_args = parse_request(request)
    jobs = request.values.getlist('job')
    app.logger.debug('jobs: %s' % str(jobs))
    app.logger.debug('time: %s' % time_args)
    result = run_sacct('%s --jobs=%s' % (time_args, ','.join(jobs)))
    return jsonify(result)


@app.route('/sacct/accounts/', methods=['GET'])
def sacct_accounts():
    time_args = parse_request(request)
    accounts = request.values.getlist('account')
    app.logger.debug('accounts: %s' % str(accounts))
    app.logger.debug('time: %s' % time_args)
    result = run_sacct('%s --allusers --accounts=%s' % (time_args,
                                                        ','.join(accounts)))
    return jsonify(result)


def run_server():
    '''Run Flask Slurm sacct Webservice Server'''
    parser = OptionParser()

    parser.add_option('-H', '--host',
                      help='IP to listen on [default: %default]',
                      default='127.0.0.1')
    parser.add_option('-P', '--port',
                      help='port to listen on [default: %default]',
                      type='int', default=5000)
    parser.add_option('-s', '--sacct',
                      help='sacct binary to use [default: %default]',
                      default='/usr/bin/sacct')
    parser.add_option('-d', '--debug', action='store_true',
                      help='Run in debug mode [default: %default]',
                      default=False)
    parser.add_option('-t', '--threaded', action='store_true',
                      help='Run in threaded mode [default: %default]',
                      default=False)

    (options, args) = parser.parse_args()
    global sacct
    sacct = options.sacct
    app.run(host=options.host, debug=options.debug, port=options.port, threaded=options.threaded)
