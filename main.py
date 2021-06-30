import json
import sys
import requests
import re
import smtplib
import traceback
from email.mime.text import MIMEText
from email.header import Header

from requests.packages import urllib3



def get_card_money(username, password):
    session = requests.Session()
    urllib3.disable_warnings()
    url_pass_neu = "https://pass.neu.edu.cn/tpass/login?service=https%3A%2F%2Fportal.neu.edu.cn%2Ftp_up%2F"
    try:
        r = session.get(url_pass_neu)
        print(r)
        print(r.text)
        lt_list = re.compile(r'name="lt" value="(.+?)"').findall(r.text)
        lp_list = re.compile(r'id="loginForm" action="(.+?)"').findall(r.text)
        if len(lt_list) != 1 or len(lp_list) != 1:
            print('bad get neu login page request')
            exit(0)
        lt = lt_list[0]
        login_path = lp_list[0]
        login_body = f'rsa={username}{password}{lt}&ul={len(username)}&pl={len(password)}&lt={lt}' \
                     '&execution=e1s1&_eventId=submit'
        login_header: dict = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'pass.neu.edu.cn',
            'Origin': 'https://pass.neu.edu.cn',
        }
        r = session.post(url=f'https://pass.neu.edu.cn{login_path}', data=login_body, headers=login_header,
                         allow_redirects=False)
        if not r.headers.__contains__("Location"):
            print("bad login neu request, please check your ID or PWD")
            exit(0)
        session.get(url=r.headers["Location"], allow_redirects=False)
        r = session.post("https://portal.neu.edu.cn/tp_up/up/subgroup/getCardMoney", data={})
        r_dict = json.loads(r.text)
        if not r_dict.__contains__("card_balance"):
            print("bad get card balance")
            exit(0)
        return float(r_dict["card_balance"]) / 100
    except Exception as e:
        print(e)


def send_warn_email(mail_host, mail_user, mail_pass, mail_receiver, subject, content):
    try:
        from_: Header = Header("饭卡余额小助手", 'utf-8')
        to: Header = Header("小主", 'utf-8')
        svr = smtplib.SMTP()
        svr.connect(mail_host)
        svr.login(mail_user, mail_pass)
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = from_
        message['To'] = to
        svr.sendmail(mail_user, mail_receiver, message.as_string())
        print("send mail successfully")
    except Exception as e:
        print("fail to send mail")
        print(e)
        traceback.print_exc()


if __name__ == '__main__':
    args_len = len(sys.argv)
    if args_len < 3:
        print("Missing enough arguments, at least 2: user, pass")
        exit(1)
    if 4 < args_len < 8:
        print(
            "Missing enough arguments, expect 7: user, pass, warn_num, mail_host, mail_user, mail_pass, mail_receiver")
        exit(1)
    if args_len > 8:
        print("Too many arguments")
        exit(1)

    user = sys.argv[1]
    pwd = sys.argv[2]
    balance = get_card_money(user, pwd)

    if args_len <= 3 or "" in sys.argv[3:8]:
        print("running without sending email, just print balance")
        print(balance)
    else:
        warn_num = sys.argv[3]
        print("running with sending email")
        if balance < float(warn_num):
            send_warn_email(sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], '快饿死了……', '你的饭卡余额低于设定值了哦')
            pass
        else:
            print('unnecessary to send email')
