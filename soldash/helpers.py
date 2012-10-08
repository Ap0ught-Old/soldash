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
import urllib2
import simplejson
import socket

from flask import jsonify

from soldash import app


def get_details():
    ''' Query Solr for information on each of the cores of 
    each of the hosts.
    '''
    
    retval = []
    for core in app.config['CORES']:
        entry = {'core_name': core, 
                 'hosts': copy.deepcopy(app.config['HOSTS'])}
        for host in entry['hosts']:
            details = query_solr(host, 'details', core)
            host['status'] = details['status']
            if host['status'] == 'ok':
                if details['data']['details']['isMaster'] == 'true':
                    host['type'] = 'master'
                    host['replicationEnabled'] = details['data']['details']['master']['replicationEnabled'] == 'true'
                else:
                    host['type'] = 'slave'
                    host['replicating'] = False
                    if details['data']['details']['slave']['isReplicating'] == 'true':
                        host['replicating'] = details['data']['details']['slave']['totalPercent'] + '%'
                    host['pollingEnabled'] = details['data']['details']['slave']['isPollingDisabled'] == 'false'
                host['indexVersion'] = details['data']['details']['indexVersion']
                host['generation'] = details['data']['details']['generation']
                host['indexSize'] = details['data']['details']['indexSize']
            elif host['status'] == 'error':
                host['error'] = details['data']
                host['exception'] = details['exception']
        retval.append(entry)
    return retval

def get_solr_version(host):
    ''' Query a Solr host for system information.
    
    Strip out and return the Solr version, since it's all we're interested
    in for the time being.
    '''
    
    url = 'http://%s:%s/solr/%s/admin/system?wt=json' %(host['hostname'],
                                                        host['port'],
                                                        app.config['DEFAULTCORENAME'])
    system_data = query_solr(host, None, None, url=url)
    if system_data['status'] == 'ok':
        return system_data['data']['lucene']['lucene-spec-version']
    else:
        return None
    
def query_solr(host, command, core, params=None, url=None):
    ''' Build a HTTP query to a Solr host and execute it. 
    
    host: host dictionary (see soldash.settings['HOSTS'])
    command: command to be performed
    core: perform this command on a certain core (see soldash.settings['CORES'])
    params: extra parameters to pass in the URL.
    url: if a non-empty string, use this string as the URL, instead of building one.
    '''
    socket.setdefaulttimeout(app.config['TIMEOUT'])
    if not core:
        core = app.config['DEFAULTCORENAME']
    
    if not url:
        if command == 'reload':
            url = 'http://%s:%s/solr/admin/cores?action=RELOAD&wt=json&core=%s' % (host['hostname'], 
                                                                                   host['port'],
                                                                                   core)
        else:
            url = 'http://%s:%s/solr/%s/replication?command=%s&wt=json' % (host['hostname'], 
                                                                           host['port'], 
                                                                           core,
                                                                           command)
    if params:
        for key in params:
            url += '&%s=%s' % (key, params[key])
    if host.get('auth', {}):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, 
                             host['auth']['username'], 
                             host['auth']['password'])
        auth_handler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(auth_handler)
        urllib2.install_opener(opener)
    try:
        conn = urllib2.urlopen(url)
        retval = {'status': 'ok', 
                  'data': simplejson.load(conn)}
    except urllib2.HTTPError, e:
        retval = {'status': 'error',
                  'data': 'conf',
                  'exception': str(e)}
    except urllib2.URLError, e:
        retval = {'status': 'error', 
                  'data': 'down',
                  'exception': str(e)}
    return retval