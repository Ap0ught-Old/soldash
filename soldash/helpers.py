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

import copy
import json
import socket
import urllib2

from flask import jsonify
import requests

from soldash import app


def get_details(data):
    """ Query Solr for information on a core in a host
    data should be in the form {'core': 'name', 'host': {'hostname': ...}}
    """
    
    retval = data['host']
    retval['core'] = data['core']
    details = query_solr(data['host'], 'details', data['core'])
    retval['status'] = details['status']
    if retval['status'] == 'ok':
        if details['data']['details']['isMaster'] == 'true':
            retval['type'] = 'master'
            retval['replicationEnabled'] = details['data']['details']['master']['replicationEnabled'] == 'true'
        else:
            retval['type'] = 'slave'
            retval['replicating'] = False
            if details['data']['details']['slave']['isReplicating'] == 'true':
                retval['replicating'] = details['data']['details']['slave']['totalPercent'] + '%'
            retval['pollingEnabled'] = details['data']['details']['slave']['isPollingDisabled'] == 'false'
        retval['indexVersion'] = details['data']['details']['indexVersion']
        retval['generation'] = details['data']['details']['generation']
        retval['indexSize'] = details['data']['details']['indexSize']
    elif retval['status'] == 'error':
        retval['error'] = details['data']
        retval['exception'] = details['exception']
    return retval

def repackage_details(details):
    """ Constructs a single dict from a list of get_details() results """
    retval = {}
    for entry in details:
        retval.setdefault(entry['core'], {})[entry['hostname']] = entry
    return retval

def get_solr_version(host):
    """ Query a Solr host for system information.
    
    Strip out and return the Solr version, since it's all we're interested
    in for the time being.
    """
    
    url = 'http://%s:%s/solr/%s/admin/system?wt=json' %(host['hostname'],
                                                        host['port'],
                                                        app.config['DEFAULTCORENAME'])
    system_data = query_solr(host, None, None, url=url)
    if system_data['status'] == 'ok':
        return system_data['data']['lucene']['lucene-spec-version']
    else:
        return None

def query_solr(host, command, core, params=None, url=None):
    """ Build a HTTP query to a Solr host and execute it. 
    
    host: host dictionary (see soldash.settings['HOSTS'])
    command: command to be performed
    core: perform this command on a certain core (see soldash.settings['CORES'])
    params: extra parameters to pass in the URL.
    url: if a non-empty string, use this string as the URL, instead of building one.
    """
    if not core:
        core = app.config['DEFAULTCORENAME']
    
    if not url:
        if command == 'reload':
            url = 'http://%s:%s/solr/admin/cores?action=RELOAD&wt=json&core=%s' % (host['hostname'], 
                                                                                   host['port'],
                                                                                   core)
        elif command == 'select':
            url = 'http://%s:%s/solr/%s/select?wt=json&q=%s' % (host['hostname'],
                                                                host['port'],
                                                                core,
                                                                params['q'])
        else:
            url = 'http://%s:%s/solr/%s/replication?command=%s&wt=json' % (host['hostname'], 
                                                                           host['port'], 
                                                                           core,
                                                                           command)
    if params:
        for key in params:
            url += '&%s=%s' % (key, params[key])
    try:
        resp = requests.get(url, auth=(host['auth'].get('username'), host['auth'].get('password')))
    except requests.ConnectionError, e:
        return {'status': 'error', 'data': 'down', 'exception': str(e)}
    return {'status': 'ok', 'data': resp.json}