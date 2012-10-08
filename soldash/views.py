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

from flask import request, jsonify, g
from flaskext.mako import render_template

from soldash import app
from soldash.helpers import get_details, query_solr, get_solr_versions

@app.route('/')
def homepage():
    ''' Render and return the main homepage HTML. 
        
    This HTML will then be populated by javascript and EJS.
    '''
    return render_template('/main.mako', config=app.config, c=get_details(), versions=get_solr_versions())

@app.route('/execute/<command>', methods=['POST'])
def execute(command):
    ''' Execute a command (one of soldash.settings['COMMANDS']).
    
    Returns the output in JSON form.
    '''
    hostname = request.form['host']
    port = request.form['port']
    
    core = request.form['core']
    if core in ['null', 'None', 'undefined']:
        core = None
    auth = {}
    params = {}
    try:
        auth = {'username': request.form['username'],
                'password': request.form['password']}
    except KeyError, e:
        pass
    try:
        params = {'indexversion': request.form['indexversion']}
    except KeyError, e:
        pass
    host = {'hostname': hostname,
            'port': port,
            'auth': auth}
    return jsonify(query_solr(host, command, core, params=params))

@app.route('/solr_versions', methods=['GET'])
def solr_versions():
    ''' Get the versions of all Solr daemons configured in 
    soldash.settings.HOSTS.
    
    Returns the output in JSON form.
    '''
    
    return jsonify({'data': get_solr_versions()})
