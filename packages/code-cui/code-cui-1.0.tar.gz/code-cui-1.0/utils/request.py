# -- coding: utf-8 --
# __create_time__ : 2022/6/14 10:24
# __email__: codeCui@outlook.com
# --auth__ : cui
# __file__ : request.py
import requests


def get(url=None, params=None, headers=None, verify=True):
    if params is not None:
        resp = requests.get(url=url, params=params, headers=headers, verify=verify)
        if resp.status_code == 200:
            return resp.text
        else:
            return False
    else:
        resp = requests.get(url, headers=headers, verify=verify)
        if resp.status_code == 200:
            return resp.text
        else:
            return False


def post(url=None, data=None, headers=None, verify=True):
    resp = requests.post(url=url, data=data, headers=headers, verify=verify)
    if resp.status_code == 200:
        return resp.text
    else:
        return False
