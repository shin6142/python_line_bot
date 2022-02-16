from flask import Flask, request, abort, render_template
# from linebot import (
#     LineBotApi, WebhookHandler
# )
# from linebot.exceptions import (
#     InvalidSignatureError
# )
# from linebot.models import (
#     MessageEvent, TextMessage, TextSendMessage, FollowEvent, TemplateSendMessage, ButtonsTemplate, MessageAction
# )
from os.path import join, dirname
from dotenv import load_dotenv
import os

from sqlalchemy import false, true
from models import model


app = Flask(__name__, static_folder='static') 

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ.get("YOUR_CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.environ.get("YOUR_CHANNEL_SECRET")
MY_LINE_ID = os.environ.get("MY_LINE_ID")

# line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
# handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']

#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     return 'OK'

# @handler.add(FollowEvent)
# def handle_follow(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text='初めまして')
#     )
#     profile = line_bot_api.get_profile(event.source.user_id)
#     username = profile.display_name
#     model.add_user(username)


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     if event.message.text=="登録":
#         profile = line_bot_api.get_profile(event.source.user_id)
#         username = profile.display_name
#         model.add_user(username)
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))


@app.route('/', methods=['GET'])
def register_get():
    return render_template('register.html', \
        title = 'Form Sample(get)', \
        message = '名前を入力して下さい。')


@app.route('/', methods=['POST'])
def register_post():
    username = request.form['username']
    model.add_user(username)
    user = model.get_user_by_name(username)
    return show_user_detail(user.id)


@app.route('/check_in/<int:user_id>')
def check_in(user_id):
    user = model.get_user(user_id)
    date_list = model.get_monthly_date_list(user_id)
    import datetime
    dt_now = datetime.date.today()
    for stamp in date_list:
        if stamp == dt_now.day:
            return render_template('user_detail.html', id=user.id, name=user.username, date_list=date_list, is_first=False)
    model.add_stamp(user_id)
    date_list = model.get_monthly_date_list(user_id)
    return render_template('user_detail.html', id=user.id, name=user.username, date_list=date_list, is_first=True)

@app.route('/user_detail/<int:user_id>')
def show_user_detail(user_id):
    user = model.get_user(user_id)
    date_list = model.get_monthly_date_list(user_id)
    return render_template('user_detail.html', id=user.id, name=user.username, date_list=date_list, is_first=False)


@app.route('/user_detail_year/<int:user_id>')
def show_user_detail_year(user_id):
    user = model.get_user(user_id)
    date_list_year = model.get_check_in_date_list(user_id)
    return render_template('user_detail_year.html', id=user.id, name=user.username, date_list_year=date_list_year)

@app.route("/send_message/<int:user_id>")
def send_message(user_id):
    user = model.get_user(user_id)
    username = user.username
#     if username != 'favicon.ico':
#         messages = TextSendMessage(text=f'{username}がジムにチェックインしました')
#         # line_bot_api.broadcast(messages=messages)
#         line_bot_api.push_message(MY_LINE_ID, messages)
    return show_user_detail(user_id)

@app.route('/all_user')
def show_all_user():
    users_list = model.get_all_user()
    return render_template('all_user_list.html', users=users_list)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)