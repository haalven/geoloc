#!/usr/bin/env python3

# geo location using ip-api.com
# next level

import sys, argparse, pathlib, urllib.request, socket, json

def main() -> int:
    # my path
    my_path = pathlib.Path(__file__)
    my_name = my_path.name

    # get address argument
    parser = argparse.ArgumentParser(prog=my_name)
    parser.add_argument('address', type=str, help='hostname or IP')
    target = parser.parse_args().address

    # request & response
    url = 'http://ip-api.com/json/' + target
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as response:
        payload = response.read().decode('utf-8')

    # JSON deserialization
    location = json.loads(payload)
    if location['status'] == 'fail':
        print('geo location search failed for', target)
        return 1

    # sorted list
    sorted_keys = ('country', 'regionName', 'city', 'isp', 'org', 'query')
    sorted_list = []
    for key in sorted_keys:
        sorted_list.append(location[key])

    # add reverse DNS
    sorted_list.append(socket.gethostbyaddr(target)[0])

    # output
    print(' \u203A '.join(sorted_list))
    return 0

if __name__ == '__main__':
    sys.exit(main())
