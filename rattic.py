#!/usr/bin/python
from sys import argv
import requests
import json

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
        return json.loads(reply.content)

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
    

if __name__ == "__main__":

    yellow = '\033[1;33m{0}\033[1;m'
    green = "\033[1;36m{0}\033[00m"    
    red = "\033[01;31m{0}\033[00m"

    def usage():
        print "Usage:"
        print "./rattic.py", yellow.format("<command> <args>")
        print "available commands:"
        print green.format("    list"), "   Lists all objects"
        print green.format("    show <object id>"), "   shows an object's details"    

    if len(argv) < 2:
        usage()

    else:
        api = RatticAPI(server='https://demo.rattic.org/', creds=('admin', 'b6797a0307b2d6defe5abe23a4f28e932cc687d6'))

        commands = {'list': 'list',
                    'show': 'show'}

        try:
            funct = commands[argv[1]]

            if funct == 'list':
                l = api.list_cred()
                for c in l['objects']:
                    print c['id'], c['title']

            elif funct  == 'show':
                c = api.get_cred(id=int(argv[2]))
                cred_print(c)
        except KeyError:
            print red.format("error: Rattic command not found.")
            usage()
