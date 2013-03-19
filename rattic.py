#!/usr/bin/python
from sys import argv 
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
        return reply.json()

    def list(self, endpoint):
        return self._makerequest(endpoint + '/')

    def set(self, endpoint, listids):
        return self._makerequest(endpoint + '/set/' + ';'.join(listids) + '/')

    def get(self, endpoint, id):
        return self._makerequest(endpoint + '/' + str(id) + '/')

def cred_print(cred):
    print "Title: %s" % (cred['title'])
    print "Username: %s" % (cred['username'])
    print "Password: %s" % (cred['password'])
    print "Description:\n%s" % (cred['description'])
    

command = argv[1]


api = RatticAPI(server='url', creds=('username', 'apikey'))
if command == 'list':
    l = api.list_cred()
    for c in l['objects']:
        print c['id'], c['title']

elif command == 'show':
    c = api.get_cred(id=int(argv[2]))
    cred_print(c)
