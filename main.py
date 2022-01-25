from flask import Flask, request, abort, render_template
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, TemplateSendMessage, ButtonsTemplate, MessageAction
)
from os.path import join, dirname
from dotenv import load_dotenv
import os
from models import model


app = Flask(__name__, static_folder='static') 

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ.get("YOUR_CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.environ.get("YOUR_CHANNEL_SECRET")
MY_LINE_ID = os.environ.get("MY_LINE_ID")

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='初めまして')
    )
    profile = line_bot_api.get_profile(event.source.user_id)
    username = profile.display_name
    model.add_user(username)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    profile = line_bot_api.get_profile(event.source.user_id)
    username = profile.display_name
    model.add_user(username)
# @app.route("/", methods=['GET'])
# def show_index():
#     return render_template('index.html')

@app.route("/<username>")
def send_message(username):
    if username != 'favicon.ico':
        messages = TextSendMessage(text=f'{username}がジムにチェックインしました')
        # line_bot_api.broadcast(messages=messages)
        line_bot_api.push_message(MY_LINE_ID, messages)
    return render_template('index.html')


@app.route('/', methods=['GET'])
def register_get():
	return render_template('register.html', \
		title = 'Form Sample(get)', \
		message = '名前を入力して下さい。')

@app.route('/', methods=['POST'])
def register_post():
	username = request.form['username']
	model.add_user(username)

@app.route('/user_detail/<username>')
def show_user_detail(username):
    user = model.get_user(username)
    return render_template('user_detail.html', id=user.id, name=user.username )

@app.route('/<int:user_id>')
def check_in(user_id):
    model.add_stamp(user_id)

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)