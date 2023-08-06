# -- coding: utf-8 --
# __create_time__ : 2022/6/14 15:32
# __email__: codeCui@outlook.com
# --auth__ : cui
# __file__ : Vip.py
import hashlib
import json

import requests
from urllib.parse import quote


def comment():
    url = 'https://mapi.vip.com/vips-mobile/rest/content/reputation/queryBySpuId_for_pc?' \
          'callback=getCommentDataCb&' \
          'app_name=shop_pc&' \
          'app_version=4.0&' \
          'warehouse=VIP_NH&' \
          'fdc_area_id=103105102&' \
          'client=pc&' \
          'mobile_platform=1&' \
          'province_id=103105&' \
          'api_key=70f71280d5d547b2a7bb370a529aeea1&' \
          'user_id=&' \
          'mars_cid=1655191668830_8301fc93fadd8f4970013ac99e26c666&' \
          'wap_consumer=a&' \
          'spuId=2761628102484803595&' \
          'brandId=1710613848&' \
          'page=1&' \
          'pageSize=10&' \
          'timestamp=1655192940000&' \
          'keyWordNlp=%E5%85%A8%E9%83%A8-%E6%8C%89%E9%BB%98%E8%AE%A4%E6%8E%92%E5%BA%8F&' \
          '_=1655192857878'
    headers = {
        'referer': 'https://detail.vip.com/',
        'cookie': 'vip_cps_cuid=CU165519166805686fa339a092f369f1; vip_cps_cid=1655191668058_0f95b38a8a113a9c88145d2856651c21; cps_share=cps_share; vip_wh=VIP_NH; cps=adp%3Antq8exyc%3A%40_%401655191668057%3Amig_code%3A4f6b50bf15bfa39639d85f5f1e15b10f%3Aac014miuvl0000b5sq8cbc48974sfboa; PAPVisitorId=cfb3edb886ff51216be06a090428e326; vip_new_old_user=1; vip_address=%257B%2522pname%2522%253A%2522%255Cu798f%255Cu5efa%255Cu7701%2522%252C%2522cname%2522%253A%2522%255Cu53a6%255Cu95e8%255Cu5e02%2522%252C%2522pid%2522%253A%2522103105%2522%252C%2522cid%2522%253A%2522103105102%2522%257D; vip_province=103105; vip_province_name=%E7%A6%8F%E5%BB%BA%E7%9C%81; vip_city_name=%E5%8E%A6%E9%97%A8%E5%B8%82; vip_city_code=103105102; user_class=a; mst_area_code=104104; mars_sid=f59452ccfdaf616c74023b92daa4fcc1; mars_pid=0; visit_id=F9B9A9885D12BEFE77037C2CAA596FC7; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A0%7Cul%3A3105; vip_tracker_source_from=; vip_access_times=%7B%22list%22%3A2%2C%22detail%22%3A2%7D; pg_session_no=7; VipDFT=-1; mars_cid=1655191668830_8301fc93fadd8f4970013ac99e26c666',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    return resp
