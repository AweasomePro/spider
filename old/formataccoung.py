

def formatAccount():
    with open('account.txt','r',encoding='utf-8') as f:
        data = f.readline()
        print(data)
        with open('accountres.txt','a+',encoding='utf-8') as f2:
            account_lisst = data.split('账号')
            for account in account_lisst:
                print('输入'+account)
                f2.write('账号'+account)
                f2.write('\n')
            print('xx')

if __name__ == '__main__':
    formatAccount()
