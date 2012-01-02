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
from soldash.settings import HOSTS, CORES, TIMEOUT, DEFAULTCORENAME

def get_details():
    ''' Query Solr for information on each of the cores of 
    each of the hosts.
    '''
    
    retval = []
    for core in CORES:
        entry = {'core_name': core, 
                 'hosts': copy.deepcopy(HOSTS)}
        for host in entry['hosts']:
            details = query_solr(host, 'details', core)
            if details['status'] == 'ok':
                host['details'] = details['data']
            elif details['status'] == 'error':
                host['details'] = None
                host['error'] = details['data']
                host['exception'] = details['exception']
        retval.append(entry)
    return retval

def get_solr_versions():
    ''' Query each Solr host for system information.
    
    Strip out and return the Solr version, since it's all we're interested
    in for the time being.
    '''
    
    retval = {}
    for host in HOSTS:
        url = 'http://%s:%s/solr/%s/admin/system?wt=json' %(host['hostname'],
                                                            host['port'],
                                                            DEFAULTCORENAME)
        system_data = query_solr(host, None, None, url=url)
        if system_data['status'] == 'ok':
            retval[host['hostname']] = system_data['data']['lucene']['lucene-spec-version']
        else:
            retval[host['hostname']] = None
    return retval
    

def query_solr(host, command, core, params=None, url=None):
    ''' Build a HTTP query to a Solr host and execute it. 
    
    host: host dictionary (see soldash.settings.HOSTS)
    command: command to be performed (see soldash.settings.COMMANDS)
    core: perform this command on a certain core (see soldash.settings.CORES)
    params: extra parameters to pass in the URL.
    url: if a non-empty string, use this string as the URL, instead of building one.
    '''
    socket.setdefaulttimeout(TIMEOUT)
    if not core:
        core = DEFAULTCORENAME
    
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