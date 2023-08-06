# -- coding: utf-8 --
# __create_time__ : 2022/6/14 10:32
# __email__: codeCui@outlook.com
# --auth__ : cui
# __file__ : TianMao.py
import hashlib
import json
import random
import re, time
from utils import request
from utils.UserAgent import mac


def loads_jsonp(_jsonp):
    """
    解析天猫返回的jsonp数据
    :param _jsonp: 淘宝或者天猫返回的jsonp结果
    :return:
    """
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except Exception as err:
        raise ValueError('Invalid Input')


def sign(data=None, cookie=None):
    """
    生成天猫和淘宝的sign
    :param data:  发起请求时params中的data
    :param cookie: 浏览器总request headers 中的data
    :return:
    """
    token = re.findall('_m_h5_tk=(.*?)_', cookie)
    a = '12574478'
    t = str(int(round(time.time() * 1000)))
    st = f'{token}&{t}&{a}&{data}'
    sg = hashlib.md5(st.encode('utf-8')).hexdigest()
    return sg, t


def goods_comment(gid=None, cookie=None):
    res = dict()
    url = 'https://rate.tmall.com/list_detail_rate.htm'
    params = {
        "itemId": gid,
        'spuId': '2299946216',
        'sellerId': '676606897',
        'order': '3',
        'currentPage': '1',
        "append": '0',
        'content': '1',
        'tagId': None,
        'posi': None,
        'picture': None,
        'groupId': None,
        'ua': '098#E1hvkpvWvPUvUvCkvvvvvjiWRL5hgjtPRL590jrCPmPWzjtbnLd9tjEjRLFvtjDCRvhvCvvvvvmvvpvZzPAecIqNznswjfaft/2GCYQH7eeevpvhvvmv99vCvvOvCvvvphvUvpCWvvG9vvwMaNLUlEILEcqh0j7Q+ul1Bzc6/X7rej9D+Exr1CAKNB3rAWBlhqUf8r3l+E7rejOdYPexfX9wjLVxfwL9digLXGeDKX6cWq9Cvm9vvvvvphvvvvvvvoHvpv1ZvvmmZhCv2CUvvUEpphvWh9vv9DCvpvQokvhvCQ9v9OH1pwkIvpvUvvmvQmmX5HvRvpvhvv2MMs9Cvvpvvvvv39hvCvvhvvm+vpvBUvotvi8ovm2K84GuUZWE3wy=',
        'needFold': '0',
        '_ksTS': '1655185166978_889',
        'callback': 'jsonp890'

    }
    headers = {
        'cookie': cookie,
        'user-agent': random.choice(mac),
        'referer': 'https://detail.tmall.com/item.htm?spm=a1z10.5-b-s.w4004-14828881390.2.645c69c4fgZC8G&id=600761932303'
    }
    resp = request.get(url, headers=headers, params=params)
    if '令牌过期' in resp:
        res['code'] = -1
        res["msg"] = 'cookie过期'
    else:
        result = loads_jsonp(resp)
        if result.get("url", None):
            res['code'] = -1
            res["msg"] = 'cookie过期'
        else:
            res['code'] = 0
            res['data'] = result
    return res
