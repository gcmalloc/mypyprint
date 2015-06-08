import requests
import re
from BeautifulSoup import BeautifulSoup
import sys

VALUES = re.compile("<tr><td align=right>(.+?)</td><td><b>(.+?)</b></td></tr>")

def get_info(username):
    response = requests.post("http://windows.epfl.ch/checkAD/AdResult.asp", data={'go': 'Rechercher', 'username': username})
    ret_dict = {}
    if response.status_code != 200:
        raise Error("status code was {!s}".format(response.status_code))
    else:
        print('bougacha' in response.content)
        values = VALUES.findall(response.content)
        if values:
            for k, v in values:
                ret_dict[k.strip(' =')] = v.strip(' =')
    return ret_dict

if __name__ == '__main__':
    print("\n".join(["{}: {}".format(k, v) for k, v in get_ad(sys.argv[1]).iteritems()]))
