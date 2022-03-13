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
from urllib.parse import urlencode
import urllib.parse
import hashlib

from models import model




class LineConfig(object):
    YOUR_CHANNEL_ACCESS_TOKEN = os.environ.get("YOUR_CHANNEL_ACCESS_TOKEN")
    YOUR_CHANNEL_SECRET = os.environ.get("YOUR_CHANNEL_SECRET")
    MY_LINE_ID = os.environ.get("MY_LINE_ID")
    line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)

    def make_greeting_text(username):
        greeting_text = f"はじめまして、FitHubです!\n友達登録・会員登録していただきありがとうございます!\nFitHubは{username}さんの健康的な習慣づくりをサポートしていきます!"
        return greeting_text

    def make_button_template(user_id, hash_line_id):
        service_url = "https://python-line-bot-0113.herokuapp.com/"
        mypage_url = f"https://python-line-bot-0113.herokuapp.com/user_detail/{user_id}/{hash_line_id}"
        checkin_url = f"https://python-line-bot-0113.herokuapp.com/check_in/{user_id}/{hash_line_id}"
        message_template = TemplateSendMessage(
            alt_text="FitHubからのお知らせ",
            template=ButtonsTemplate(
                text="FitHubへようこそ!",
                title="FitHub",
                image_size="cover",
                thumbnail_image_url="https://python-line-bot-0113.herokuapp.com/static/images/vertical_man_headphones.jpg",
                actions= [
                    {
                        "type": "uri",
                        "label": "FitHubの使い方をみる",
                        "uri": service_url
                    },
                    {
                        "type": "uri",
                        "label": "マイページ",
                        "uri": mypage_url
                    },
                    {
                        "type": "uri",
                        "label": "本日のトレーニングを記録する",
                        "uri": checkin_url
                    },
                ]
            )
        )
        return message_template


class message_submittion(LineConfig):


    def follow_event(event):
        profile = message_submittion.line_bot_api.get_profile(event.source.user_id)
        line_id = profile.user_id
        username = profile.display_name
        hash_line_id = hashlib.sha256(line_id.encode("utf-8")).hexdigest()
        if model.get_user_by_line_id(line_id) == None:
            model.add_user(username, line_id, hash_line_id)
        elif model.get_user_by_line_id(line_id) == True:
            pass
        greeting_text = message_submittion.make_greeting_text(username)
        user = model.get_user_by_line_id(line_id)
        user_id = user.id
        hash_line_id = user.hash_line_id
        messages = message_submittion.make_button_template(user_id, hash_line_id)
        message_submittion.line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=greeting_text), messages]
        )
    
    def handle_message(event):
        message_submittion.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

 
    def notify_checkin(user_id):
        user = model.get_user(user_id)
        username = user.username
        if username != 'favicon.ico':
            messages = TextSendMessage(text=f'{username}がトレーニンングを開始しました。')
            message_submittion.line_bot_api.broadcast(messages=messages)
            # message_submittion.line_bot_api.push_message(MY_LINE_ID, messages