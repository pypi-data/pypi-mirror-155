# The MIT License (MIT)
#
# Copyright (c) 2021-2022 Thorsten Simons (sw@snomis.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Sos of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyrighftware without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copiet notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from logging import getLogger
from http.client import HTTPSConnection
from urllib.parse import urlencode, quote
from ssl import _create_unverified_context  # protected member, one shouldn't do that...
from json import loads, dumps

from hcilib.base.exceptions import HciAccessError

class Hci:
    """
    A class to facilitate authenticated access to HCI MAPI.
    """

    def __init__(self, host: str='localhost', user: str='', password: str='', realm: str=''):
        """
        :param host:      the host to talk to (one of the HCI instances, usually localhost)
        :param user:      a user with rights to use MAPI
        :param password:  its password
        :param realm:     the user's realm (LOCAL for admin, or the IDPs name)
        """
        # setup an https connection to HCI instance
        self.con = HTTPSConnection(host, port=8000, context=_create_unverified_context(), timeout=10)

        # acquire an access token
        params = {'grant_type': 'password',
                  'username': user,
                  'password': password,
                  'client_secret': 'hcisle_secret',
                  'client_id': 'hcisle',
                  'realm': realm
                  }
        self.con.request('POST', f'/auth/oauth/?{urlencode(params)}',
                         headers={'content-type': 'application/x-www-form-urlencoded'})
        res = self.con.getresponse()

        if res.status == 200:
            jbody = loads(res.read())
            self.token = f'Bearer {jbody["access_token"]}'
            self.headers = {'Authorization': f'Bearer {jbody["access_token"]}',
                            'Content-Type': 'application/json',
                            'accept': 'application/json'
                            }
        else:
            raise HciAccessError(f'Generation of HCI access token failed with status code {res.status}')


    def getHciVersion(self) -> dict:
        """
        Function to retrieve the HCI's product version.

        This works without authentication - at least till version 2.1...

        :returns:     a dict of {"productShortName": ...,
                                 "productVersion": ...,
                                 "loginUrl": ...}
        """
        log = getLogger('hcisle.' + __name__)

        # we're not catching exceptions here, leaving it to the caller
        self.con.request('GET', '/api/admin/setup', headers=self.headers)
        res = self.con.getresponse()

        if res.status == 200:
            jbody = loads(res.read())
            ret = {"productShortName": jbody["productShortName"],
                   "productVersion": jbody["productVersion"],
                   "loginUrl": jbody["loginUrl"]}
            log.debug(f'retrieving HCI information returned {ret}')
            return ret
        else:
            raise HciAccessError(f'retrieving HCI information failed with status code {res.status}')


    def getHciServices(self) -> list:
        """
        Function to retrieve a list of configured (enabled) Services in HCI.

        :returns:     a list of service names
        """
        log = getLogger('hcisle.' + __name__)

        reqbody = dumps({"serviceTypes": ["product"],
                         "requestedDetails": ["status"]})

        # we're not catching exceptions here, leaving it to the caller
        self.con.request('POST', '/api/admin/services/query', body=reqbody, headers=self.headers)
        res = self.con.getresponse()

        if res.status == 200:
            jbody = loads(res.read())
            return [x['name'] for x in jbody['serviceConfigs'] if x['status'] != 'Unconfigured']
        else:
            raise HciAccessError(f'retrieving HCI Services failed with status code {res.status}')


if __name__ == '__main__':
    from os import environ

    hci = Hci(host=environ['HCISLE_HOST'],
              user=environ['HCISLE_USER'],
              password=environ['HCISLE_PASSWORD'],
              realm=environ['HCISLE_REALM'])
    print(hci.getHciVersion())
    print(hci.getHciServices())