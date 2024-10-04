import os
import random
import string
import time
import names
from curl_cffi import requests as req

proxies = None

requests=req.Session()
requests.impersonate='chrome110'
def get_headers(Country,Language):
    while True:
        try:

            an_agent=f'Mozilla/5.0 (Linux; Android {random.randint(9,13)}; {"".join(random.choices(string.ascii_uppercase, k=3))}{random.randint(111,999)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
            res = requests.get("https://www.facebook.com/",headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'},proxies=proxies, timeout=30)
            js_datr = res.text.split('["_js_datr","')[1].split('",')[0]
            r=requests.get('https://www.instagram.com/api/v1/web/accounts/login/ajax/',headers={
                'user-agent': an_agent
            },proxies=proxies,timeout=30).cookies

            headers1 = {
                'authority': 'www.instagram.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': f'{Language}-{Country},en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': f'dpr=3; csrftoken={r["csrftoken"]}; mid={r["mid"]}; ig_nrcb=1; ig_did={r["ig_did"]}; datr={js_datr}',
                'sec-ch-prefers-color-scheme': 'light',
                'sec-ch-ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': an_agent,
                'viewport-width': '980',
            }
            response1 = requests.get('https://www.instagram.com/', headers=headers1,proxies=proxies,timeout=30)
            appid=response1.text.split('APP_ID":"')[1].split('"')[0]
            rollout=response1.text.split('rollout_hash":"')[1].split('"')[0]
            headers = {
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': f'{Language}-{Country},en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
                'content-type': 'application/x-www-form-urlencoded',
                'cookie': f'dpr=3; csrftoken={r["csrftoken"]}; mid={r["mid"]}; ig_nrcb=1; ig_did={r["ig_did"]}; datr={js_datr}',
                'origin': 'https://www.instagram.com',
                'referer': 'https://www.instagram.com/accounts/signup/email/',
                'sec-ch-prefers-color-scheme': 'light',
                'sec-ch-ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': an_agent,
                'viewport-width': '360',
                'x-asbd-id': '198387',
                'x-csrftoken': r["csrftoken"],
                'x-ig-app-id': str(appid),
                'x-ig-www-claim': '0',
                'x-instagram-ajax': str(rollout),
                'x-requested-with': 'XMLHttpRequest',
                'x-web-device-id': r["ig_did"],
            }
            return headers
        except Exception as E:
            print(E)

def Get_UserName(Headers,Name,Email):
    try:

        updict = {"referer": 'https://www.instagram.com/accounts/signup/birthday/'}
        Headers = {key: updict.get(key, Headers[key]) for key in Headers}
        while True:


            data = {
                'email': Email,
                'name': Name+str(random.randint(1,99)),
            }

            response = requests.post(
                'https://www.instagram.com/api/v1/web/accounts/username_suggestions/',
                headers=Headers,
                data=data,
                proxies=proxies,
                timeout=30
            )
            if 'status":"fail' in response.text:
                print(response.text)
            elif 'status":"ok' in response.text :
                print(response.text)
                return random.choice(response.json()['suggestions'])
            else:print(response.text)

    except Exception as E:
        print(E)


def Send_SMS(Headers,Email):
    try:
        data = {
            'device_id': Headers['cookie'].split('mid=')[1].split(';')[0],
            'email': Email,
}

        response = requests.post(
            'https://www.instagram.com/api/v1/accounts/send_verify_email/',
            headers=Headers,
            data=data,
            proxies=proxies,
            timeout=30
        )
        return response.text
    except Exception as E:
        print(E)



def Validate_Code(Headers,Email,Code):

    try:
        updict = {"referer": 'https://www.instagram.com/accounts/signup/emailConfirmation/'}
        Headers = {key: updict.get(key, Headers[key]) for key in Headers}



        data = {
            'code': Code,
            'device_id': Headers['cookie'].split('mid=')[1].split(';')[0],
            'email': Email,
        }

        response = requests.post(
            'https://www.instagram.com/api/v1/accounts/check_confirmation_code/',
            headers=Headers,
            data=data,
            proxies=proxies,
            timeout=30
        )
        return response



    except Exception as E:
        print(E)



def Create_Acc(Headers,Email,SignUpCode):

    try:
        firstname=names.get_first_name()
        UserName=Get_UserName(headers,firstname,Email)
        Password=firstname.strip()+'@'+str(random.randint(111,999))

        updict = {"referer": 'https://www.instagram.com/accounts/signup/username/'}
        Headers = {key: updict.get(key, Headers[key]) for key in Headers}


        data = {
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{round(time.time())}:{Password}',
            'email': Email,
            'username': UserName,
            'first_name': firstname,
            'month': random.randint(1,12),
            'day': random.randint(1,28),
            'year': random.randint(1990,2001),
            'client_id': Headers['cookie'].split('mid=')[1].split(';')[0],
            'seamless_login_enabled': '1',
            'tos_version': 'row',
            'force_sign_up_code': SignUpCode,
        }
        print(data)

        response = requests.post(
            'https://www.instagram.com/api/v1/web/accounts/web_create_ajax/',
            headers=Headers,
            data=data,
            proxies=proxies,
            timeout=30

        )
        print(response.text)
        if '"account_created":true' in response.text:
            print('UserName : ' + UserName)
            print('PassWord : ' + Password)
            print('Sessionid : ' +response.cookies['sessionid'])
            print('Csrftoken : ' +response.cookies['csrftoken'])
            print('Ds_user_id : ' +response.cookies['ds_user_id'])
            print('Ig_did : ' +response.cookies['ig_did'])
            print('Rur : ' +response.cookies['rur'])
            print('Mid : ' + Headers['cookie'].split('mid=')[1].split(';')[0])
            print('Datr : ' + Headers['cookie'].split('datr=')[1])
        else:
            pass
    except Exception as E:
        print(E)


if __name__ == "__main__":
    print('Tool Made By @NamasteHacker')

    headers=get_headers(Country='US',Language='en')   # Enter Your Country With Your Local Language In Short Code
    Email=input('Enter Your Email : ')       # Enter Your Email
    ss=Send_SMS(headers,Email)
    print(ss)
    if 'email_sent":true' in ss:
        code=input('Enter Code : ')
        a=Validate_Code(headers,Email,code)
        print(a.text)
        if 'status":"ok' in a.text:
            SignUpCode=a.json()['signup_code']
            Create_Acc(headers,Email,SignUpCode)
        else:
            print(a.text)
    else :pass



