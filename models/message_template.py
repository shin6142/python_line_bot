from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, TemplateSendMessage,
    ButtonsTemplate, MessageAction, CarouselTemplate, CarouselColumn, URIAction, ImageMessage
    )

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