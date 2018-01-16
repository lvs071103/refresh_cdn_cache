#!/usr/bin/python
# --*-- coding: utf-8 --*--
# author: Jack.Z


import json
import requests
import sys
import logging
import hashlib
from time import strftime, gmtime


def generate_md5_password(check_code_string):
    check_code = hashlib.md5()
    check_code.update(check_code_string)
    return check_code.hexdigest()


def refresh_cdn(cdn_url):
    """
    :param cdn_url: When multiple URL is separated by semicolon
    """
    api_url = 'http://ccm.chinanetcenter.com/ccm/servlet/contReceiver?'
    username = "username"
    password = 'p4word'

    md5sum_pass = generate_md5_password(username + password + cdn_url)

    post_data = {
        'username': username,
        'passwd': md5sum_pass,
        'url': cdn_url
    }

    req = requests.post(url=api_url, data=post_data)
    return req.text


def log_format(message):
    logging.basicConfig(level=logging.DEBUG, filename="/tmp/refresh_cdn.log", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info(message)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: %s [URL|DIR]" % sys.argv[0]
        print "When multiple URL(DIR) is separated by semicolon"
    else:
        print refresh_cdn(sys.argv[1])
        # log_format(urls + ' ' + refresh_cdn(urls))
