import requests
import time
import sys
from rich import print


def slow_print(str, sleep_sec=5):
    for c in str + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(sleep_sec / 20)

def token_checker(token):
    url = "https://www.clubhouseapi.com/api/me"
    headers = {
        'CH-Languages': 'en-US',
        'CH-Locale': 'en_US',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'CH-AppBuild': '305',
        'CH-AppVersion': '1.0.9',
        'CH-UserID': '1387526936',
        'User-Agent': 'clubhouse/305 (iPhone; iOS 14.4; Scale/2.00)',
        'Connection': 'close',
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Token ' + token
    }
    return_blocked_ids = 'True'
    timezone_identifier = 'Asia/Tehran'
    return_following_ids = 'True'
    data = '{"return_blocked_ids": "' + return_blocked_ids + '","timezone_identifier": "' + timezone_identifier + '","return_following_ids": "' + return_following_ids + '"}'
    resp = requests.post(url, headers=headers, data=data)
    result = resp.json()
    if result.get('success'):
        success_status = str(result["success"])
        if success_status == 'True':
            user_id = str(result["user_profile"]["user_id"])
            name = str(result["user_profile"]["name"])
            username = str(result["user_profile"]["username"])
            email = str(result["email"])
            photo_url = str(result["user_profile"]["photo_url"])
            return True, user_id, name, username, email, photo_url
        else:
            return False, 'error: cant find bot user_id', '', '', '', ''
    else:
        return False, 'error: invalid token', '', '', '', ''


def get_token_list(token_list_address):
    tokens_array = []
    # read proxy list file
    file = open(token_list_address)
    for token in file:
        # read token
        token = token.replace('\n', '')
        # check not null
        if token:
            # add tokens to array
            tokens_array.append(token)
    if len(tokens_array) > 0:
        return True, tokens_array
    else:
        return False, 'cant fetch token list'


def save_toke_to_file(new_token):
    f = open("valid_token_list.txt", "a")
    f.write(new_token + '\n')
    f.close()
def save_UserID_to_file(new_token):
    f = open("valid_UserID_list.txt", "a")
    f.write(new_token + '\n')
    f.close()


# get token list
token_list_address = 'unknown_tokens.txt'
token_list_status, tokens_array = get_token_list(token_list_address)

if (token_list_status):
    # check tokens
    counter_token = 0
    counter_number=0
    for token in tokens_array:
        counter_number=counter_number+1
        checker_status, user_id, name, username, email, photo_url = token_checker(token)
        if checker_status:
            counter_token = counter_token + 1
            save_toke_to_file(token)
            save_UserID_to_file(user_id)
            print("[white]"+str(counter_number)+"-[/][green]"+token+"[/]")
            #print('user_id=' + user_id)
            #print('name=' + name)
            #print('username=' + username)
            #print('email=' + email)
            #print('photo_url=' + photo_url)
        else:
            print("[white]"+str(counter_number)+"-[/][red]"+token+"[/]")
        #time.sleep(2)
    print('===============================================')
    print('total valid token=>' + str(counter_token) + ' from=>' + str(len(tokens_array)) + ' token')
    if counter_token == 0:
        print('canot find valid token')
else:
    print('token list file is empty')
