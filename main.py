import json
import sys

import requests
import re

if __name__ == '__main__':
    session = requests.Session()
    url_pass_neu = "https://pass.neu.edu.cn/tpass/login?service=http%3A%2F%2Fhub.17wanxiao.com%2Fcas-dongbei%2Fcas%2Fcjgy%2Flight.action%3Fflag%3Ddongbei_dongbeidaxue%26amp%3BecardFunc%3Dindex "
    # url_pass_neu = "https://e-report.neu.edu.cn/login"
    r = session.get(url=url_pass_neu)
    lt_list = re.compile(r'name="lt" value="(.+?)"').findall(r.text)
    lp_list = re.compile(r'id="loginForm" action="(.+?)"').findall(r.text)
    if len(lt_list) != 1 or len(lp_list) != 1:
        print('bad get neu login page request')
        exit(0)
    lt = lt_list[0]
    login_path = lp_list[0]
    if len(sys.argv) != 3:
        print('usage:\npython main.py <id> <password>')
        exit(0)
    username = sys.argv[1]
    password = sys.argv[2]
    login_body = f'rsa={username}{password}{lt}&ul={len(username)}&pl={len(password)}&lt={lt}&execution=e1s1&_eventId=submit'
    login_header: dict = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'pass.neu.edu.cn',
        'Origin': 'https://pass.neu.edu.cn',
    }
    r = session.post(url=f'https://pass.neu.edu.cn{login_path}', data=login_body, headers=login_header)
    data_list = re.compile(r'data:\'(.+?)\'').findall(r.text)
    if len(data_list) != 1:
        print('bad login neu request\n'
              'please check whether your id or password is correct\n'
              'or please wait for a minute and try again')
        print(r.text)
        exit(0)
    data_dict = json.loads(data_list[0][9:])
    url_17wan_xiao = "http://hub.17wanxiao.com/cas-dongbei/bsacs/redirect.action"
    post_header: dict = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'hub.17wanxiao.com',
        'Origin': 'http://hub.17wanxiao.com',
        'Cookie': f'JSESSIONID={session.cookies.get("JSESSIONID")}; SERVERID= {session.cookies.get("SERVERID")}'
    }
    r = session.post(url=url_17wan_xiao, data=data_list[0], headers=post_header)
    r = session.get(url=json.loads(r.text)["url"])
    r = session.get(url=r.url.replace("%20", ""))
    url_boot_call_back = "https://ecardh5.17wanxiao.com/ecardh5/bootcallback"
    post_header: dict = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }
    session.headers.update(post_header)
    r = session.post(url=url_boot_call_back, data="gotowhere=XYK_BASE_INFO")
    print(json.loads(r.text)["data"]["main_fare"])
