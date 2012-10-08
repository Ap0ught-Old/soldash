# -*- coding: utf-8 -*-
settings = {
'HOSTS': [
    {
        'hostname': '127.0.0.1',
        'port': 8983,
        'auth': {'username': 'test', 'password': 'test'}
    }
],

'CORES': ['de_DE-items', 'fr_FR-items'],

'TIMEOUT': 1,

'JS_REFRESH': 2,

'HIDE_STATUS_MSG_SUCCESS': 2,

'HIDE_STATUS_MSG_ERROR': 5,

'DEBUG': True,

'DEFAULTCORENAME': 'collection1',

'RESPONSEHEADERS': {0: 'ok'},

'COMMANDS': [
    {'command': 'fetchindex', 'title': 'Fetch Index', 'reverse': 'abortfetch'},
    {'command': 'enablepoll', 'title': 'Polling', 'reverse': 'disablepoll'},
    {'command': 'enablereplication', 'title': 'Replication', 'reverse': 'disablereplication'}, 
    {'command': 'details', 'title': False}, 
    {'command': 'filelist', 'title': 'File List'},
    {'command': 'backup', 'title': 'Backup'},
    {'command': 'reload', 'title': 'Reload Index'}
],




# one or more directories
'MAKO_DIR': 'soldash/templates',
# optional, if specified Mako will cache to this directory
'MAKO_CACHEDIR': '/tmp',
# optional, if specified Mako will respect the cache size
'MAKO_CACHESIZE': 500
}