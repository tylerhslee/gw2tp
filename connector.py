# -*- coding: utf-8 -*-
"""
Connector object that requests data from the GW2 API.
"""
import re
import requests

from yaml import load

with open('./config.yml', 'r') as rf:
    API_KEY = load(rf)['api-config']['apikey']


class Connector(object):

    _PAGE_SIZE = 200
    _BIG_PAGE = 9999

    def __init__(self, apikey, version='v2'):
        self.apikey = apikey

        base_url = 'https://api.guildwars2.com/'
        self.api_url = base_url + version

    def _complete_url(self, *args, params={}):
        # Always include the apikey in the URL
        params['apikey'] = self.apikey

        # Build query string
        query = '{name}={value}'
        p = [query.format(name=k, value=params[k]) for k in params.keys()]
        qstr = '?{params}'.format(params='&'.join(p))

        # Build URL to the specific endpoint
        paths = '/' + '/'.join([k for k in args])
        return self.api_url + paths + qstr

    def get(self, *args, params={}):
        r = requests.get(self._complete_url(*args, params=params))
        return r

    # Query absurdly high page number, so that it tells me the maximum number
    # of valid pages
    def get_max_page(self, *args):
        resp = self.get(*args, params={'page': Connector._BIG_PAGE,
                                       'page_size': Connector._PAGE_SIZE})
        regex = r'0\s-\s(\d+)\.'
        return int(re.search(regex, resp.json()['text']).group(1))


if __name__ == '__main__':
    connector = Connector(API_KEY)
    r = connector.get('commerce', 'prices', params={'ids': '811,421'})
    print(r.json())
