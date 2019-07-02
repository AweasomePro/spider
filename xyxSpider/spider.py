
import os,inspect

import requests
import json
from concurrent.futures import ThreadPoolExecutor

from wand.api import library
import wand.color
import wand.image
login_url = 'https://today.yidinghong.net/api/exchg/system/login'

query_Pending_url = 'https://today.yidinghong.net/api/exchg/order/queryPendingOrders?page=1&count=20'
import webbrowser as web
# Accept: application/json, text/plain, */*
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
# Authorization: t1A8wdKPklfMtgkneGIayJ5SkLujz5tj
# Connection: keep-alive
# Cookie: sidebarStatus=1
# Host: today.yidinghong.net
# If-None-Match: W/"41-YT0yqoLC4waWtwKuvEDF0jA6280"
# Referer: https://today.yidinghong.net/
# User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36
# x-token: DOLZrPImBVaDH2t7l3zLiG0cPpBiMc2u86TsQQTOjYTlamfp432IkXYTyUx4Na3sLsYc7x1kI5y1LmT93MPxlW

headers={
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
    "Authorization":"t1A8wdKPklfMtgkneGIayJ5SkLujz5tj",
    "Connection":"keep-alive",
    "Cookie":"sidebarStatus=1",
    "Host":"today.yidinghong.net",
    "Referer":"https://today.yidinghong.net/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}


def login(account, password, faield_test_again=True):
    paylod = {
        'act': account,
        'pwd': password,
        'code': "132465",
        "codeType": "google"
    }
    try:
        r = requests.post(login_url, paylod)
        r_json = json.loads(r.text)
        if r_json['code'] == 200:
            token =r_json['msg']['token']
            print('token为'+token)
            return token
        else:
            return None
    except requests.ConnectTimeout:
        if faield_test_again:
            login(account, faield_test_again=False)
    except Exception as e:
        print('login 异常 -{}'.format(e.__cause__))
        return None


def query_Orders(token):
    try:
        headers['x-token']=token
        response = requests.get(query_Pending_url,headers=headers)
        r_json = json.loads(response.text)
        if r_json['code'] == 200:
            captcha = r_json['captcha']
            if captcha is not None:
                print("验证码"+captcha)
                current_path = os.getcwd()

                with wand.image.Image(blob=captcha, format="svg") as image:
                    png_image = image.make_blob("png")
                with open("captcha.png", "wb") as out:
                    out.write(png_image)
                f =open("captcha.png","w")
                htmlContext = """
                <html>
                    <body>
                        %(captcha)s
                    </body>
                </html>
                """
                pass
            else:
                print('抢单结果'+r_json.text)
    except Exception as e:
        print('query_Orders 异常 -{}'.format(e.__cause__))
    return False
    pass

def multipleThreadQueryOrder(token):
    seed= (token,token,token,token,token)
    with ThreadPoolExecutor(3) as executor:
        for each in seed:
            executor.submit(query_Orders,each)
    pass
if __name__ == '__main__':
    token = login('duihuan052','ss123456')
    if token!=None:
        query_Orders(token)

