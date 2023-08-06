# -- coding: utf-8 --
# __create_time__ : 2022/6/14 14:16
# __email__: codeCui@outlook.com
# --auth__ : cui
# __file__ : JingDong.py
import json
import random
from utils.UserAgent import mac
from utils import request


def fetch_json(text):
    try:
        return json.loads(text.replace('fetchJSON_comment98(', '').replace(');', ''))
    except Exception as err:
        raise ValueError('value err')


def comment(gid=None, cookie=None):
    """
    :param gid: 商品ID
    :param cookie
    :return:
    """
    url = 'https://club.jd.com/comment/productPageComments.action'
    params = {
        'callback': 'fetchJSON_comment98',
        'productId': gid,
        'score': '0',
        'sortType': '5',
        'page': '0',
        'pageSize': '10',
        'isShadowSku': '0',
        'fold': '1'
    }
    headers = {
        'cookie': cookie,
        'user-agent': random.choice(mac),
        'referer': 'https://item.jd.com/'
    }
    resp = request.get(url, headers=headers, params=params)
    if resp:
        result = fetch_json(resp)
        return result
