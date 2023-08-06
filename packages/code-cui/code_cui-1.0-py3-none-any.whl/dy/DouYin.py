# -- coding: utf-8 --
# __create_time__ : 2022/6/14 15:14
# __email__: codeCui@outlook.com
# --auth__ : cui
# __file__ : DouYin.py
import hashlib
import json
import random
from utils import request, UserAgent

MD5KEY = 'zd2019@@1157'


def md5_token(item):
    a = hashlib.md5(str(item).encode('utf-8')).hexdigest()  # 第一次只加密 itemId
    key = a + MD5KEY  # 第一次解加密结果加上key 进行二次加密得到token
    token = hashlib.md5(key.encode('utf-8'))
    return token.hexdigest()


def comment(itemId=None):
    url = 'https://ec.snssdk.com/product/ajaxitem'
    headers = {
        "user-agent": random.choice(UserAgent.android)
    }
    token = md5_token(itemId)
    params = {
        'id': itemId,
        'shop_id': 'uqrxitDU',
        'pay_type': '1',
        'uid': '',
        'token': token,
        'aid': '',
        'b_type_new': '0'
    }
    resp = request.get(url, params=params, headers=headers)
    result = json.loads(resp)
    return result



