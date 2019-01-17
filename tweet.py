import tweepy
import datetime
import sys
import time

# 各種キーのセット
Consumer_key = '****'
Consumer_secret = '****'
Access_token = '****'
Access_secret = '****'

auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_token, Access_secret)

# APIインスタンスの生成
api = tweepy.API(auth)

content = input('content: ')
while '\\n' in content:
    content = content.replace('\\n', '\n')  # 改行文字の処理

argv = input('time: ')
date_time = datetime.datetime.strptime(argv, '%Y-%m-%d %H:%M')  # datetimeオブジェクトへ変換
date_time += datetime.timedelta(minutes=-1)  # 1分戻す
date = date_time.strftime('%Y-%m-%d')
time = date_time.strftime('%H:%M')

time_delta = []  # 実際のツイート時刻までの誤差

def tweet(sec, delete=True):
    ''' sec はstr型で 23.456 のようにミリ秒まで入れて6文字'''
    '''デフォルトでツイートは削除'''
    while True:
        if str(datetime.datetime.now())[:23] >= date+' '+time+':'+sec:
            status_id = api.update_status(status=content+(sec if delete==True else '')).id
            if delete:
                api.destroy_status(status_id)
            created_at = str(datetime.datetime.fromtimestamp(((int(status_id)>>22)+1288834974657)/1000.0))[:-3]
            print('succeeded: '+created_at)
            time_delta.append(float(str(float(created_at[-6:])-float(sec))))
            break

# テストツイート(20秒~55秒まで1秒ごとに)
print('now: '+str(datetime.datetime.now()))
i = 0
while True:
    if str(datetime.datetime.now())[:23] > date+' '+time+':55.000':
        break
    if str(datetime.datetime.now())[:23] < date+' '+time+':'+'{:0<6}'.format(20+i*1.0)[:6]:
        tweet('{:0<6}'.format(20+i*1.0)[:6])
    i += 1

del time_delta[0]  # 1回目のテストツイートは外れ値になりやすいので除外
ave = sum(time_delta)/len(time_delta)
delta = ave-(ave-min(time_delta))/2  # 本番ツイートまでの誤差を指定

print('wait a moment...')
tweet('{:0<6}'.format(60.0-delta)[:6], delete=False)
