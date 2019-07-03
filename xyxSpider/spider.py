import os, inspect
from datetime import datetime

import requests
import json
from concurrent.futures import ThreadPoolExecutor

login_url = 'https://today.yidinghong.net/api/exchg/system/login'
from cairosvg import svg2png
import threading, queue, time

query_Pending_url = 'https://today.yidinghong.net/api/exchg/order/queryPendingOrders?page=1&count=20'

lock_order_url = 'https://today.yidinghong.net/api/exchg/order/lockOrder'
threadPool = ThreadPoolExecutor(4)
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

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Authorization": "geEj2jAsH7HMxt14uYDLv0PWR9BuolNq",
    "Connection": "keep-alive",
    "Cookie": "sidebarStatus=0",
    "Host": "today.yidinghong.net",
    "Referer": "https://today.yidinghong.net/",
    "If-None-Match": "W/\"41-YT0yqoLC4waWtwKuvEDF0jA6280",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
}

query_count = 0


class GlobalState:

    class LockOrderHandler(threading.Thread):

        def run(self):
            while True:
                orderId = GlobalState.orderIdQueue.get()
                lockOrder(orderId)
                pass

    orderIdQueue = queue.Queue(10)
    cond = threading.Condition()
    wait_captcha_handle_event = threading.Event()

    handle_captcha_lock = threading.Lock()

    def __init__(self, act, pwd):
        self.__act = act
        self.__pwd = pwd
        self.__token = None
        self.__need_handle_captcha = False
        self.__captcha = None
        self.__orders = []
        self.wait_captcha_handle_event.clear()
        self.__last_query_order_time = 0
        pass

    def set_captcha(self, captcha):
        self.__captcha = captcha

    def login(self, faield_test_again=True):
        paylod = {
            'act': self.__act,
            'pwd': self.__pwd,
            'code': "132465",
            "codeType": "google"
        }
        try:
            r = requests.post(login_url, paylod)
            r_json = json.loads(r.text)
            if r_json['code'] == 200:
                token = r_json['msg']['token']
                print('登录成功')
                self.__token = token
                self.startConsumeOrder()
                self.loopQueryOrder()
            else:
                print('登录失败')

        except requests.ConnectTimeout:
            if faield_test_again:
                login(faield_test_again=False)
        except Exception as e:
            print('login 异常 -{}'.format(e.__cause__))
            raise e
        pass



    def startConsumeOrder(self):
        handler = self.LockOrderHandler()
        handler.start()
        pass

    def loopQueryOrder(self):
        while True:
            self.query_Orders()

    def __putOrder(self):

        pass

    def __try_lock_order(self):
        pass

    def handle_captcha(self):
        self.__need_handle_captcha = True
        try:
            value = input('请输入验证码:')
            self.query_Orders(value)
        except Exception as e:
            print('query_Orders 异常 -{}'.format(e.__cause__))

            raise e
        return False

    def query_Orders(self, captcha=None):
        querySpace = time.time() - self.__last_query_order_time
        print('space is '+str(querySpace))
        sleepTime = abs(1-querySpace)
        if sleepTime >1:
            sleepTime =1
        print('wait ='+str(sleepTime))
        time.sleep(sleepTime)

        if self.__need_handle_captcha and captcha is None:
            print('等待验证码被处理\n')
            self.wait_captcha_handle_event.wait(timeout=10)

        try:
            print("开始查询订单")
            headers['x-token'] = self.__token
            url = query_Pending_url
            if captcha is not None:
                url = query_Pending_url + "&captcha=" + captcha
            response = requests.get(url, headers=headers)
            self.__last_query_order_time = time.time()
            r_json = json.loads(response.text)
            if r_json['code'] == 200:
                if 'captcha' in r_json:
                    captcha = r_json['captcha']
                    svg2png(bytestring=captcha, write_to='output.png')
                    self.handle_captcha()
                    pass
                else:
                    self.__need_handle_captcha = False
                    msg = r_json['msg']
                    orderData = msg['data']
                    totalCount = msg['totalCount']
                    print(str(msg))
                    if len(orderData) > 0:
                        print('发送有单子的时间' + str(datetime.now()))
                        self.orderIdQueue.put(orderData[0]['oid'])
                    # self.wait_captcha_handle_event.set()
            else:
                print(response.text)
                pass
        except Exception as e:
            print('query_Orders 异常 -{}'.format(e.__cause__))

            raise e
        pass


def login(account, password, faield_test_again=True):
    paylod = {
        'act': account,
        'pwd': password,
        'code': "132465",
        "codeType": "google"
    }
    try:
        r = requests.post(login_url, paylod, headers=headers)
        r_json = json.loads(r.text)
        if r_json['code'] == 200:
            token = r_json['msg']['token']
            print('token为' + token)
            return token
        else:
            return None
    except requests.ConnectTimeout:
        if faield_test_again:
            login(account, faield_test_again=False)
    except Exception as e:
        print('login 异常 -{}'.format(e.__cause__))
        return None


def parse_orders(json):
    return json['msg']['data']


def query_Orders(token, captcha=None):
    try:
        print("开始查询订单 当前查询次数" + str(query_count))
        headers['x-token'] = token
        url = query_Pending_url
        if captcha is not None:
            url = query_Pending_url + "&captcha=" + captcha
        print("url 是" + url)
        response = requests.get(url, headers=headers)
        print(response.text + "\n")
        r_json = json.loads(response.text)
        if r_json['code'] == 200:

            if 'captcha' in r_json:
                captcha = r_json['captcha']
                svg2png(bytestring=captcha, write_to='output.png')
                value = input('请输入验证码:')
                print("输入了" + value)
                query_Orders(token, value)
                # with wand.image.Image(blob=captcha, format="svg") as image:
                #     png_image = image.make_blob("png")
                # with open("captcha.png", "wb") as out:
                #     out.write(png_image)
                # f =open("captcha.png","w")
                # htmlContext = """
                # <html>
                #     <body>
                #         %(captcha)s
                #     </body>
                # </html>
                # """
                pass
            else:
                msg = r_json['msg']
                orderData = msg['data']
                totalCount = msg['totalCount']
                if totalCount > 0:
                    print('发送有单子的时间' + str(datetime.now()))
                    findOrder = True
                    print('开始去抢单')
                    if totalCount == 1:
                        lockOrder(orderData[0]['oid'])
                    else:
                        for order in orderData:
                            threadPool.submit(lockOrder, lockOrder(order['oid']))

                    pass
                print('查单结果' + str(r_json))
        else:
            print(response.text)
            pass
    except Exception as e:
        print('query_Orders 异常 -{}'.format(e.__cause__))

        raise e
    return False
    pass


def lockOrder(oid):
    print('oid 是' + str(oid))
    try:
        pay_load = {
            'oid': oid,
            'status': 'pending'
        }
        print('锁单发起请求的时间' + str(datetime.now()))
        response = requests.post(lock_order_url, pay_load, headers=headers)
        print('发起响应的时间' + str(datetime.now()))

        print('锁单结果 result:' + response.text)
    except Exception as e:
        raise e
    pass


def multipleThreadQueryOrder(token):
    seed = (token,)
    with ThreadPoolExecutor(3) as executor:
        for each in seed:
            executor.submit(query_Orders, each)
    pass


findOrder = False
if __name__ == '__main__':
    manager = GlobalState('duihuan052', 'ss123456')
    manager.login(faield_test_again=True)

    # token = login('duihuan052', 'ss123456')
    # if token != None:
    #     query_Orders(token)
    #
    # while findOrder is not True:
    #     time.sleep(0.5)
    #     query_Orders(token)
    # pass
