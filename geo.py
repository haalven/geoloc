#!/usr/bin/env python3

# geo location using ip-api.com


import urllib.request
from json import loads
from sys import argv, exit
from socket import gethostbyaddr
from re  import search



# api-get

def api_get(url, p):

    url = url.strip('/')
    url += '/' + p

    try:
        with urllib.request.urlopen(url) as r:
            return loads(r.read().decode('utf-8'))
    except Exception as e: print('api error:', e)



# addr -> hostname

def hn_by_addr(ipaddr):

    ip = str(ipaddr).strip().lower()

    if not ip: return ''

    try: hostname = str(gethostbyaddr(ip)[0])
    except Exception: hostname = ''

    return hostname if hostname else '<no hostname>'



# add info

def add_info(field):

    if field in result:

        if result[field] and not (result[field] in info):

            info.append(result[field].replace(chr(39),chr(700)))



# api location

url = 'http://ip-api.com/json/'


# cli arg

myname = argv.pop(0).split('/')[-1]

syntax = f'syntax: {myname} <address>'

if len(argv) < 1: exit(syntax)


# globals

result, info = {}, []


# contact api

result = api_get(url, argv[0])


# check result

try:
    if not (result['status'] == 'success'):
        exit()

except Exception: exit('no result')


# fill location info

for f in [  'country',
            'regionName',
            'city',
            'isp',
            'org',
            'query' ]:

    add_info(f)


# reverse ip -> hostname

if search(r'\d+\.\d+\.\d+\.\d+', result['query']):  # ip4

    hostname = hn_by_addr( result['query'] )

    if hostname: info.append(hostname)


# output

if info: print( ' ➔ '.join(info) )

