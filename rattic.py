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
        name, point = name.split('_')
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
        l = self._makerequest(endpoint + '/')
        for c in l['objects']:
            print c['id'], c['title']

    def set(self, endpoint, listids):
        return self._makerequest(endpoint + '/set/' + ';'.join(listids) + '/')

    def get(self, endpoint, args):
        cred = self._makerequest(endpoint + '/' + str(args['-i']) + '/')
        print "Title: %s" % (cred['title'])
        print "Username: %s" % (cred['username'])
        print "Password: %s" % (cred['password'])
        print "Description:\n  %s" % (cred['description'])
    

if __name__ == "__main__":

    yellow = '\033[1;33m{0}\033[1;m'
    green = "\033[1;36m{0}\033[00m"    
    red = "\033[01;31m{0}\033[00m"

    def usage():
        print "Usage:"
        print "./rattic.py", yellow.format("<command> <args>")
        print "available commands:"
        print "    list       Lists all objects"
        print "    show", green.format("-i"), yellow.format("ID"), "Shows an object's details"    

    if len(argv) < 2:
        usage()

    else:
        api = RatticAPI(server='https://demo.rattic.org/', creds=('admin', 'b6797a0307b2d6defe5abe23a4f28e932cc687d6'))

        commands = {'list': 'list',
                    'show': 'get'}

        try:
            funct = commands[argv[1]]+'_cred'

            
            if len(argv) == 2:
                getattr(api, funct)()

            else:
                args = dict(zip(*[iter(argv[2:])] * 2))
                getattr(api, funct)(args=args)
        
        except KeyError:
            print red.format("error: Rattic command not found.")
            usage()
