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
import os

from models import model, message_template, qr_creater



#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ.get("YOUR_CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.environ.get("YOUR_CHANNEL_SECRET")
MY_LINE_ID = os.environ.get("MY_LINE_ID")

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


class LineConfig(object):
    line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(YOUR_CHANNEL_SECRET)


class message_submittion(LineConfig):

    def follow_event(event):
        profile = line_bot_api.get_profile(event.source.user_id)
        username = profile.display_name
        if model.get_user_by_name(username) == None:
            model.add_user(username)
        greeting_text = message_template.make_greeting_text(username)
        user = model.get_user_by_name(username)
        user_id = user.id
        messages = message_template.make_button_template(user_id)
        line_bot_api.reply_message(
                event.reply_token,
            [TextSendMessage(text=greeting_text), messages]
        )
    
    def handle_message(event):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

    
    def notify_checkin(user_id):
        user = model.get_user(user_id)
        username = user.username
        if username != 'favicon.ico':
            messages = TextSendMessage(text=f'{username}がジムにチェックインしました')
            line_bot_api.broadcast(messages=messages)
            # line_bot_api.push_message(MY_LINE_ID, messages)




# richMenu
def make_rich_menu():
    rich_menu_to_create = RichMenu(
        size = RichMenuSize(width=2500, height=1686),
        selected = True,
        name = 'richmenu',
        chat_bar_text = 'メニュー',
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=1273, height=868),
                action=PostbackAction(data='renew')
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1278, y=0, width=1211, height=864),
                action=PostbackAction(data='deadline')
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=864, width=1268, height=818),
                action=PostbackAction(data="not_submitted")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1273, y=877, width=1227, height=805),
                action=PostbackAction(data="forget")
            )
        ]
    )
    richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    with open("static/image/man_run.svg", 'rb') as f:
        line_bot_api.set_rich_menu_image(richMenuId, "image/png", f)
    line_bot_api.set_default_rich_menu(richMenuId)

def make_greeting_text(username):
    greeting_text = f"はじめまして、FitHubです!\n友達登録・会員登録していただきありがとうございます!\nFitHubは{username}の健康的な習慣づくりをサポートしていきます!"
    return greeting_text


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
                    "label": "FitHubの使い方をみる",
                    "uri": f"https://python-line-bot-0113.herokuapp.com/service"
                },
                {
                    "type": "uri",
                    "label": "記録を確認する",
                    "uri": f"https://python-line-bot-0113.herokuapp.com/user_detail/{user_id}"
                },
                {
                    "type": "uri",
                    "label": "本日のトレーニングを記録する",
                    "uri": f"https://python-line-bot-0113.herokuapp.com/check_in/{user_id}"
                },
            ]
        )
    )
    return message_template