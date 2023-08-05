import requests
import collections
import json
import os
from urlparse import urlparse
from utils import remove_none


class HemanEngine(object):
    debug = None
    methods = {
        'GET': requests.get,
    }

    def __init__(self, config, debug=False):
        self.url = config['url']
        self.debug = debug

    def req_to_service(self, req):
        headers = {'Authorization': 'token %s' % req.token}

        url = self.url + '/' + req.url
        data = req.data
        req.headers.update(headers)

        result = self.methods[req.command](url,
                                           data=json.dumps(data),
                                           headers=req.headers)
        result.raise_for_status()

        if result.status_code == 204:
            return []

        r = result.json()
        if isinstance(r, dict):
            return r.get('_items', r)
        return r

    def req_to_curl(self,req):
        headers = {'Authorization': 'token %s' % req.token}

        url = requests.compat.urljoin(self.url, req.url)
        data = req.data

        header_ = ''
        for header_key, header_value in req.headers.iteritems():
            header_ += ' -H "{header_key}:{header_value}"'.format(**locals())

        data_ = ''
        if data:
            data_ = '-d \'{data}\''.format(**locals())

        curl_command = 'curl -k -X {req.command} -i {header_} \'{url}\' {data_}'.format(**locals())
        return curl_command

    def req(self, req):
        if self.debug:
            return self.req_to_curl(req)
        else:
            return self.req_to_service(req)


class Heman_REQ(object):
    token = None
    url = None
    data = None
    headers = {'Content-type': 'application/json'}

    def __init__(self, token, url, data=None):
        self.token = token
        self.url = requests.compat.urljoin(self.url, url)
        self.data = data


class Heman_GET(Heman_REQ):
    command = 'GET'


class HemanOTResults(object):
    SUPPORTED_OT = ['OT101', 'OT102', 'OT103', 'OT105', 'OT106', 'OT201', 'OT204', 'OT205', 'OT301', 'OT302',
                    'OT303', 'OT304', 'OT305', 'OT401', 'OT501', 'OT501', 'OT503', 'OT504', 'OT603', 'OT603g',
                    'OT701', 'OT703', 'OT900', 'OT910', 'OT920'
                    ]
    name = None
    path = None

    @classmethod
    def ot_supported(cls, ot):
        return ot in cls.SUPPORTED_OT

    @classmethod
    def path(cls, ot, contract_id, period):
        if ot not in cls.SUPPORTED_OT:
            raise NotImplementedError()
        return '{ot}Results/{contract_id}/{period}'.format(**locals())


class Ramman(object):
    engine = None

    def __init__(self, config, debug=False):
        self.engine = HemanEngine(config, debug)

    @property
    def debug(self):
        return self.engine.debug

    @debug.setter
    def debug(self, x):
        self.engine.debug = x

    def get(self, contract_id, partner_token, ot, period=''):
        if not HemanOTResults.ot_supported(ot):
            raise NotImplementedError

        url = HemanOTResults.path(ot, contract_id, period)

        req = Heman_GET(partner_token, url)
        return self.engine.req(req)
