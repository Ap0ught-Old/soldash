# -*- coding: utf-8 -*-

#Copyright 2011 Aengus Walton <aengus.walton@edelight.de>
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
#

from flask import request, jsonify, abort, redirect
from flaskext.mako import render_template

from soldash import app
import soldash.helpers as h

@app.route('/')
def homepage():
    """ Render and return the main homepage HTML. 
    """
    versions = {}
    for host in app.config['HOSTS']:
        versions[host['hostname']] = h.get_solr_version(host)
    return render_template('/main.mako', c=h.get_details(), versions=versions, h=h)

@app.route('/execute/<command>', methods=['GET'])
def execute(command):
    """ Execute a command
    """
    hostname = request.args.get('hostname')
    core = request.args.get('core')
    params = {}
    if command == 'filelist':
        params['indexversion'] = request.args.get('indexversion')
    if core not in app.config['CORES']:
        abort(400, 'Invalid core')
    # TODO: check validity of command name
    try:
        host = [obj for obj in app.config['HOSTS'] if obj['hostname'] == hostname][0]
    except KeyError:
        abort(400, 'Invalid hostname')
    # TODO: Error checking from Solr
    retval = h.query_solr(host, command, core, params=params)
    if command == 'filelist':
        return jsonify(retval)
    return redirect('/')
