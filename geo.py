#!/usr/bin/env python3

# geo location using ip-api.com
# next level

import sys, argparse, pathlib, urllib.request, socket, json

def main() -> int:
    # my path
    my_path = pathlib.Path(__file__)

    # get address argument
    parser = argparse.ArgumentParser(prog=my_path.name)
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
        if not location[key] in sorted_list:
            sorted_list.append(location[key])

    # add reverse DNS
    try:
        sorted_list.append(socket.gethostbyaddr(target)[0])
    except:
        pass

    # output
    print('\x1b[1m \u203A \x1b[0m'.join(sorted_list))
    return 0

if __name__ == '__main__':
    sys.exit(main())
