from flask import Flask, request, abort, render_template, make_response
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, TemplateSendMessage,
    ButtonsTemplate, MessageAction, CarouselTemplate, CarouselColumn, URIAction, ImageMessage
    )
from os.path import join, dirname
from dotenv import load_dotenv
import os
import pyqrcode

from sqlalchemy import false, true
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


def make_button_template(user_id):
    message_template = TemplateSendMessage(
        alt_text="FitHubからのお知らせ",
        template=ButtonsTemplate(
            text="トレーニングの記録",
            title="FitHub",
            image_size="cover",
            thumbnail_image_url="https://python-line-bot-0113.herokuapp.com/static/images/woman_yoga.svg",
            actions= [
                {
                    "type": "uri",
                    "label": "本日のトレーニングを記録する",
                    "uri": f"https://python-line-bot-0113.herokuapp.com/user_detail/{user_id}"
                },
                {
                    "type": "uri",
                    "label": "記録を確認する",
                    "uri": f"https://python-line-bot-0113.herokuapp.com/check_in/{user_id}"
                }
            ]
        )
    )
    return message_template


# ----LINE bot------
@handler.add(FollowEvent)
def handle_image_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    username = profile.display_name
    if model.get_user_by_name(username) == None:
        model.add_user(username)
    user = model.get_user_by_name(username)
    user_id = user.id
    messages = make_button_template(user_id)
    line_bot_api.reply_message(
        event.reply_token,
        messages
    )

# ----TODO------

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     if event.message.text=="登録":
#         profile = line_bot_api.get_profile(event.source.user_id)
#         username = profile.display_name
#         model.add_user(username)
#     messages = event.message.text
#     line_bot_api.reply_message(event.reply_token, messages=messages)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    messages = make_button_template()
    line_bot_api.reply_message(
        event.reply_token,
        messages
    )
# ----LINE bot------

# -----Web--------
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

@app.route("/create_qr/<int:user_id>")
def create_qrcode(user_id):
    qr_filename = "qr.png"
    qr_url = f'https://python-line-bot-0113.herokuapp.com/check_in/{user_id}'
    code = pyqrcode.create(qr_url, error='L', version=4, mode='binary')
    code.png(qr_filename, scale=5, module_color=[0, 0, 0, 128], background=[255, 255, 255])
    response = make_response()
    response.data  = open(qr_filename, "rb").read()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=checkInQRCode.png'
    os.remove(qr_filename)
    return response

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)