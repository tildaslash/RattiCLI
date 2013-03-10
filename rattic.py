#!/usr/bin/python

import requests

class RatticAPI(object):
    VERSION = 'v1'
    def __init__(self, creds=None, server=None):
        if server is not None:
            self.server = server
        if creds is not None:
            self.creds = creds

    def __getattr__(self, name):
        (name, point) = name.split('_', 1)
        method = object.__getattribute__(self, name)
	def wrapped(*args, **kwargs):
            return method(endpoint=point, *args, **kwargs)
        return wrapped

    def _getauthheader(self):
        (user, key) = self.creds
        return 'ApiKey ' + user + ':' + key

    def _getheaders(self):
        return {
            'authorization': self._getauthheader(),
            'accept': 'application/json',
        }

    def _makerequest(self, path):
        reply = requests.get(self.server + 'api/' + self.VERSION + '/' + path, headers=self._getheaders())
        reply.raise_for_status()
        return reply.json

    def list(self, endpoint):
        return self._makerequest(endpoint + '/')

    def set(self, endpoint, listids):
        return self._makerequest(endpoint + '/set/' + ';'.join(listids) + '/')

    def get(self, endpoint, id):
        return self._makerequest(endpoint + '/' + str(id) + '/')


api = RatticAPI(server='http://admin01:8000/', creds=('daniel', '745d623a557f81751d9153d8a654ce87d1e13f77'))
d = api.list_cred()
e = api.list_tag()

for c in api.list_cred()['objects']:
    print c['id'], c['title']

for t in api.list_tag()['objects']:
    print t['name']

for s in api.set_cred(listids=map(str, [4,2,7,1]))['objects']:
    print s['id'], s['title']

print api.get_cred(id=5)

