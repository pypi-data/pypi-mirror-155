import os
import typesense


TYPESENSE_API_KEY = os.environ.get('TYPESENSE_API_KEY', 'xyz')
TYPESENSE_SEARCH_KEY = os.environ.get('TYPESENSE_SEARCH_KEY', '9B1PUuRZU5szyFE6HZGRHi19f03aWIql')
TYPESENSE_TIMEOUT = os.environ.get('TYPESENSE_TIMEOUT', '120')
TYPESENSE_HOST = os.environ.get('TYPESENSE_HOST', 'typesense.acdh-dev.oeaw.ac.at')
TYPESENSE_PORT = os.environ.get('TYPESENSE_PORT', '443')
TYPESENSE_PROTOCOL = os.environ.get('TYPESENSE_PROTOCOL', 'https')
TYPESENSE_CLIENT = typesense.Client(
    {
        'nodes': [
            {
                'host': TYPESENSE_HOST,
                'port': TYPESENSE_PORT,
                'protocol': TYPESENSE_PROTOCOL
            }
        ],
        'api_key': TYPESENSE_API_KEY,
        'connection_timeout_seconds': int(TYPESENSE_TIMEOUT)
    }
)

CFTS_SCHEMA_NAME = os.environ.get('CFTS_SCHEMA_NAME', 'cfts')

CFTS_SCHEMA = {
    'name': CFTS_SCHEMA_NAME,
    'fields': [
        {
            'name': 'id',
            'type': 'string',
        },
        {
            'name': 'rec_id',
            'type': 'string'
        },
        {
            'name': 'project',
            'type': 'string'
        },
        {
            'name': 'title',
            'type': 'string'
        },
        {
            'name': 'full_text',
            'type': 'string'
        },
        {
            'name': 'date',
            'type': 'int64',
            'facet': True,
            'optional': True
        },
        {
            'name': 'year',
            'type': 'int32',
            'optional': True,
            'facet': True
        },
        {
            'name': 'persons',
            'type': 'string[]',
            'facet': True,
            'optional': True
        },
        {
            'name': 'places',
            'type': 'string[]',
            'facet': True,
            'optional': True
        },
        {
            'name': 'orgs',
            'type': 'string[]',
            'facet': True,
            'optional': True
        },
        {
            'name': 'works',
            'type': 'string[]',
            'facet': True,
            'optional': True
        },
        {
            'name': 'keywords',
            'type': 'string[]',
            'facet': True,
            'optional': True
        }
    ]
}

CFTS_COLLECTION = TYPESENSE_CLIENT.collections[CFTS_SCHEMA_NAME]
