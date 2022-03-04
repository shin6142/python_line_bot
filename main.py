from flask import Flask, request, abort, render_template
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, TemplateSendMessage,
    ButtonsTemplate, MessageAction, CarouselTemplate, CarouselColumn, URIAction, ImageMessage, RichMenu, RichMenuArea,
    RichMenuBounds, RichMenuSize
    )
from linebot.models.actions import PostbackAction
from os.path import join, dirname
from dotenv import load_dotenv
import os

from sqlalchemy import false, true
from models import model
from controller import line_controller, qrcode_controller

app = Flask(__name__, static_folder='static') 

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#環境変数取得
# YOUR_CHANNEL_ACCESS_TOKEN = os.environ.get("YOUR_CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.environ.get("YOUR_CHANNEL_SECRET")
# MY_LINE_ID = os.environ.get("MY_LINE_ID")

# line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
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


# ----LINE bot------
@handler.add(FollowEvent)
def greeting(event):
    return line_controller.message_submittion.follow_event(event)


@handler.add(MessageEvent, message=TextMessage)
def reply_text(event):
    return line_controller.message_submittion.handle_message(event)


@app.route("/send_message/<int:user_id>")
def send_message(user_id):
    return line_controller.message_submittion.notify_checkin(user_id)
# ----LINE bot------


# -----Web--------
@app.route('/', methods=['GET'])
def register_get():
    return render_template('register.html')


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


@app.route('/all_user')
def show_all_user():
    users_list = model.get_all_user()
    return render_template('all_user_list.html', users=users_list)

@app.route("/create_qr/<int:user_id>")
def qrcode(user_id):
    return qrcode_controller.create_qrcode(user_id)



@app.route('/service')
def show_service_page():
    return render_template('service.html')


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)