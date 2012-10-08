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

    'HIDE_STATUS_MSG_SUCCESS': 2,

    'HIDE_STATUS_MSG_ERROR': 5,

    'DEBUG': True,

    'DEFAULTCORENAME': 'de_DE-items',

    # one or more directories
    'MAKO_DIR': 'soldash/templates',
    # optional, if specified Mako will cache to this directory
    'MAKO_CACHEDIR': '/tmp',
    # optional, if specified Mako will respect the cache size
    'MAKO_CACHESIZE': 500
}