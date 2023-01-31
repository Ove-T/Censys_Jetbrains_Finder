import requests
requests.packages.urllib3.disable_warnings()
# key的值为在https://search.censys.io/api#/页面中，进行API测试时，Curl请求中Authorization: Basic后的字符串
key = 'xxxx'
header = {"accept":"application/json","Authorization":"Basic "+key}

# 账号检测
def check_auth():
    url = "https://search.censys.io/api/v1/account"
    re = requests.get(url, headers=header)
    return  re.status_code
# 获取查询结果中的ip
def get_ip():
    url = "https://search.censys.io/api/v2/hosts/search?q=services.http.response.headers.location%3A%20account.jetbrains.com%2Ffls-auth&per_page=50&virtual_hosts=EXCLUDE"
    data = requests.get(url,headers=header)
    ip_list=[]
    if data.status_code == 200:
        list = data.json()['result']['hits']
        for x in list:
            services = x['services']
            for y in services:
                if y['port'] == 80:
                    ip_list.append(x['ip'])
                    break
    check_ip(ip_list)

# 对获取的ip进行验证
def check_ip(ip_list):
    for ip in ip_list:
        data = requests.get('http://' + ip,verify=False)
        if 'JetBrains Account' in data.text:
            with open ('ip_list.txt','a+') as f:
                f.write(ip+'\n')

if __name__ == '__main__':
    if check_auth()==200:
        get_ip()
    else:
        print('key值错误')
