#!/usr/bin/python
# --*-- coding: utf-8 --*--
# author: Jack.Z


import requests
import sys
import random
import hmac
import hashlib
import binascii
import time
import json
from requests.packages.urllib3.exceptions import InsecurePlatformWarning, InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RefreshCDN(object):
    def __init__(self, action, refresh_url):
        self.secret_id = 'secert_id'
        self.secret_key = 'secret_key'
        self.request_host = 'cdn.api.qcloud.com'
        self.request_url = '/v2/index.php'
        self.Nonce = random.randint(1, sys.maxint)
        self.method = 'POST'
        self.action = action
        self.signature = None
        self.timestamp = int(time.time())
        self.tgt_url = refresh_url
        self.api_url = 'https://%s%s' % (self.request_host, self.request_url)
        self.region = 'gz'
        self.request_client = "Python_Tools"
        self.params = {}

    def init_params(self):
        self.params = {
            'Nonce': self.Nonce,
            'Timestamp': self.timestamp,
            'Region': self.region,
            'RequestClient': self.request_client,
            'SecretId': self.secret_id,
            'Action': self.action,
        }
        if self.params['Action'] == 'RefreshCdnUrl':
            self.params['urls.0'] = self.tgt_url
        else:
            self.params['dirs.0'] = self.tgt_url

    def sign(self):
        source_string = '{0}{1}{2}?{3}'.format(self.method.upper(), self.request_host, self.request_url, '&'.join(
                k.replace('_', '.') + '=' + str(self.params[k]) for k in sorted(self.params.keys())))
        hashed = hmac.new(self.secret_key, source_string, hashlib.sha1)
        self.signature = binascii.b2a_base64(hashed.digest())[:-1]

    def refresh_handler(self):
        self.params['Signature'] = self.signature
        req = requests.post(url=self.api_url, data=self.params, timeout=10, verify=False)
        return json.loads(req.text)


class ErrorOutput(object):

    @staticmethod
    def args_num_error():
        """
        输出错误信息
        """
        print
        print 'Usage : ' + sys.argv[0] + '  Actions ' + ' refresh_url '
        print
        sys.exit(1)

    @staticmethod
    def actions_match_error():
        """
        输出错误信息
        """
        print
        print "Actions include RefreshCdnUrl and RefreshCdnDir"
        print
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[1] == 'RefreshCdnUrl':
            cdn = RefreshCDN(action=sys.argv[1], refresh_url=sys.argv[2])
            cdn.init_params()
            cdn.sign()
            print cdn.refresh_handler()
        elif sys.argv[1] == 'RefreshCdnDir':
            cdn = RefreshCDN(sys.argv[1], sys.argv[2])
            cdn.init_params()
            cdn.sign()
            print cdn.refresh_handler()
        else:
            print ErrorOutput.actions_match_error()
    else:
        print ErrorOutput.args_num_error()
