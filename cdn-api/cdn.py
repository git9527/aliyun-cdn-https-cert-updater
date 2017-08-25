#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys,os
import urllib, urllib2
import base64
import hmac
import hashlib
from hashlib import sha1
import time
import uuid
import json
from optparse import OptionParser
import ConfigParser
import traceback

access_key_id = '';
access_key_secret = '';
cdn_server_address = 'https://cdn.aliyuncs.com'
CONFIGFILE = os.getcwd() + '/aliyun.ini'
CONFIGSECTION = 'Credentials'
cmdlist = '''
接口说明请参照pdf文档
'''

def percent_encode(str):
    res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res

def compute_signature(parameters, access_key_secret):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])

    canonicalizedQueryString = ''
    for (k,v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)

    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])

    h = hmac.new(access_key_secret + "&", stringToSign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature

def compose_url(user_params):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    parameters = { \
            'Format'        : 'JSON', \
            'Version'       : '2014-11-11', \
            'AccessKeyId'   : access_key_id, \
            'SignatureVersion'  : '1.0', \
            'SignatureMethod'   : 'HMAC-SHA1', \
            'SignatureNonce'    : str(uuid.uuid1()), \
            'TimeStamp'         : timestamp, \
    }

    for key in user_params.keys():
        parameters[key] = user_params[key]

    signature = compute_signature(parameters, access_key_secret)
    parameters['Signature'] = signature
    url = cdn_server_address + "/?" + urllib.urlencode(parameters)
    return url

def make_request(user_params, quiet=False):
    url = compose_url(user_params)
    print url
def configure_accesskeypair(args, options):
    if options.accesskeyid is None or options.accesskeysecret is None:
        print("config miss parameters, use --id=[accesskeyid] --secret=[accesskeysecret]")
        sys.exit(1)
    config = ConfigParser.RawConfigParser()
    config.add_section(CONFIGSECTION)
    config.set(CONFIGSECTION, 'accesskeyid', options.accesskeyid)
    config.set(CONFIGSECTION, 'accesskeysecret', options.accesskeysecret)
    cfgfile = open(CONFIGFILE, 'w+')
    config.write(cfgfile)
    cfgfile.close()

def setup_credentials():
    config = ConfigParser.ConfigParser()
    try:
        config.read(CONFIGFILE)
        global access_key_id
        global access_key_secret
        access_key_id = config.get(CONFIGSECTION, 'accesskeyid')
        access_key_secret = config.get(CONFIGSECTION, 'accesskeysecret')
    except Exception, e:
		print traceback.format_exc()
		print("can't get access key pair, use config --id=[accesskeyid] --secret=[accesskeysecret] to setup")
		sys.exit(1)



if __name__ == '__main__':
    parser = OptionParser("%s Action=action Param1=Value1 Param2=Value2\n" % sys.argv[0])
    parser.add_option("-i", "--id", dest="accesskeyid", help="specify access key id")
    parser.add_option("-s", "--secret", dest="accesskeysecret", help="specify access key secret")
	
    (options, args) = parser.parse_args()
    if len(args) < 1:
		parser.print_help()
		sys.exit(0)

    if args[0] == 'help':
		print cmdlist
		sys.exit(0)
    if args[0] != 'config':
		setup_credentials()
    else: #it's a configure id/secret command
        configure_accesskeypair(args, options)
        sys.exit(0)

    user_params = {}
    idx = 1
    if not sys.argv[1].lower().startswith('action='):
        user_params['action'] = sys.argv[1]
        idx = 2

    for arg in sys.argv[idx:]:
        try:
            key, value = arg.split('=')
            user_params[key.strip()] = value
        except ValueError, e:
            print(e.read().strip())
            raise SystemExit(e)
    make_request(user_params)

