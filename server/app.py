# -*- coding: utf-8 -*-

from flask import Flask, request
import json
import random

app = Flask('slackbot')
SLACK_TOKEN = YOUR_SLACK_TOKEN
member_list = []

def __add_member(request_text):
    raw_lists = request_text.split()

    for i in range(2, len(raw_lists)):
        if not raw_lists[i] in member_list:
            member_list.append(raw_lists[i])


def __del_member(request_text):
    print request_text
    raw_lists = request_text.split()

    for i in range(2, len(raw_lists)):
        if raw_lists[i] in member_list:
            member_list.remove(raw_lists[i])


def __get_member_list():
    result = ''
    for member in member_list:
        result = ' '.join([result, member])

    return result


def __get_lucky():
    result = ''
    shuffled_list = random.sample(member_list, len(member_list))

    i = 0
    for member in shuffled_list:
        i = i + 1
        if i % 2 == 0:
            result = '  //  '.join([member, result])
        else:
            result = ','.join([member, result])

    return result


@app.route('/', methods=['POST'])
def receive_request():
    token = request.form['token']
    if token != SLACK_TOKEN:
        result = {'text': 'wrong request!'}
	return json.dumps(result)

    trigger_word = request.form['trigger_word']
    text = request.form['text']

    result = {}
    if u'추가' in text:
        __add_member(text)
        current_members = ': '.join([u'현재 멤버', __get_member_list()])
        result = {'text': current_members}
    elif u'리스트' in text:
        current_members = ': '.join([u'현재 멤버', __get_member_list()])
        result = {'text': current_members}
    elif u'삭제' in text:
        __del_member(text)
        current_members = ': '.join([u'현재 멤버', __get_member_list()])
        result = {'text': current_members}
    else:
        selected_team = ': '.join([u'추첨 결과', __get_lucky()])
        result = {'text': selected_team}

    return json.dumps(result, ensure_ascii=False)

if __name__ == '__main__':
    app.run(port=5000)
