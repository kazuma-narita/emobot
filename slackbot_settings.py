# coding: utf-8
import os

# botアカウントのトークンを指定
API_TOKEN = os.environ.get('SLACKBOT_API_TOKEN', '')

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = '使い方\n今日の発言を分析：@bot "分析したいユーザID"\n例) @bot user_id\n特定の日の発言を分析：@bot "分析したいユーザID" "2017-06-30 or today or yesterday"\n例) @bot user_id 2017-06-30'

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']
