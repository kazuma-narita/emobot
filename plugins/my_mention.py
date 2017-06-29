from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from mlask import MLAsk
import os
import urllib.request
import json
import re

@respond_to(r'^[a-z0-9\-\._]')
@respond_to(r'^DEBUG [a-z0-9\-\._]')
def message_analyze(message):
    raw_text = message.body['text']
    text = []
    text = raw_text.split(' ')
    if text[0] == 'DEBUG':
        if len(text) > 2:
            if re.match(r'[\d{4}\-\d{2}\-\d{2}|today|yesterday]', text[2]):
                user = text[1]
                date = text[2]
            else:
                user = text[1]
                date = 'today'
        else:
            user = text[1]
            date = 'today'
    else:
        if len(text) > 1:
            if re.match(r'[\d{4}\-\d{2}\-\d{2}|today|yesterday]', text[1]):
                user = text[0]
                date = text[1]
            else:
                user = text[0]
                date = 'today'
        else:
            user = text[0]
            date = 'today'

    #発言内容取得
    url = 'https://slack.com/api/search.messages?token=' + os.environ.get('SLACK_API_TOKEN', '') + '&query=from%3A' + user + '%20on%3A' + date + '&sort=timestamp'
    response = urllib.request.urlopen(url)
    content = json.loads(response.read().decode('utf8'))
    msg_list = []
    for msg in content['messages']['matches']:
        msg_text = re.sub(r'<.+?>', '', msg['text'])
        msg_list.append(msg_text)
    print (msg_list)

    #分析
    msgs = ' '.join(msg_list)
    emotion_analyzer = MLAsk()
    analyzed = (emotion_analyzer.analyze(msgs))
    #print (analyzed)

    #出力
    if text[0] == 'DEBUG':
        output = str(analyzed)
    else:
        if analyzed['text'] == '':
            output = '今日はまだ発言が無いようです。'
        elif 'orientation' not in analyzed or 'activation' not in analyzed:
            output = '発言内容に感情分析できる言葉が含まれていないようです。'
        else:
            result = {('POSITIVE', 'ACTIVE')  : '最高に機嫌いいみたい！',
                      ('POSITIVE', 'NEUTRAL') : '機嫌いいみたい！',
                      ('POSITIVE', 'PASSIVE') : '機嫌は悪く無いかも？',
                      ('NEUTRAL', 'ACTIVE')   : '機嫌いいかも？',
                      ('NEUTRAL', 'NEUTRAL')  : '機嫌は良くも悪くも無く普通。',
                      ('NEUTRAL', 'PASSIVE')  : '機嫌は普通。',
                      ('NEGATIVE', 'ACTIVE')  : 'もしかしたら機嫌悪いかも？',
                      ('NEGATIVE', 'NEUTRAL') : '機嫌悪そう。。。',
                      ('NEGATIVE', 'PASSIVE') : '今は話しかけないほうが良さそう。。。'}

            if analyzed['orientation'] == 'POSITIVE' or analyzed['orientation'] == 'mostly_POSITIVE':
                orientation = 'POSITIVE'
            elif analyzed['orientation'] == 'NEGATIVE' or analyzed['orientation'] == 'mostly_NEGATIVE':
                orientation = 'NEGATIVE'
            else:
                orientation = 'NEUTRAL'

            if analyzed['activation'] == 'ACTIVE' or analyzed['activation'] == 'mostly_ACTIVE':
                activation = 'ACTIVE'
            elif analyzed['activation'] == 'PASSIVE' or analyzed['activation'] == 'mostly_PASSIVE':
                activation = 'PASSIVE'
            else:
                activation = 'NEUTRAL'

            output = result[(orientation, activation)]

    message.reply(output)
