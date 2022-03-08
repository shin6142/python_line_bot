from statistics import mode
from flask import request, render_template, redirect
from linebot.models.actions import PostbackAction
from os.path import join, dirname
from dotenv import load_dotenv
import os
from pyparsing import line_end
from sqlalchemy import false, true
import json, requests, jwt, sys

from models import model

import checkIn_controller
import os


class LineAuthenticationConfig(object):
    LINE_CHANNEL_ID_LOGIN = os.environ.get("LINE_CHANNEL_ID_LOGIN")
    LINE_CHANNEL_SECRET_LOGIN = os.environ.get("LINE_CHANNEL_SECRET_LOGIN")
    REDIRECT_URL = os.environ.get("REDIRECT_URL")


class LineAuthentication(LineAuthenticationConfig):

    def index():
        return render_template("index.html",
                           random_state="line1216",
                           channel_id=LineAuthentication.LINE_CHANNEL_ID_LOGIN,
                           redirect_url=LineAuthentication.REDIRECT_URL)

    def line_login():
        # 認可コードを取得する
        request_code = request.args["code"]
        uri_access_token = "https://api.line.me/oauth2/v2.1/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data_params = {
            "grant_type": "authorization_code",
            "code": request_code,
            "redirect_uri": LineAuthentication.REDIRECT_URL,
            "client_id": LineAuthentication.LINE_CHANNEL_ID_LOGIN,
            "client_secret": LineAuthentication.LINE_CHANNEL_SECRET_LOGIN
        }

        # トークンを取得するためにリクエストを送る
        response_post = requests.post(uri_access_token, headers=headers, data=data_params)
        # 今回は"id_token"のみを使用する
        line_id_token = json.loads(response_post.text)["id_token"]

        # ペイロード部分をデコードすることで、ユーザ情報を取得する
        decoded_id_token = jwt.decode(line_id_token,
                                    LineAuthentication.LINE_CHANNEL_SECRET_LOGIN,
                                    audience=LineAuthentication.LINE_CHANNEL_ID_LOGIN,
                                    issuer='https://access.line.me',
                                    algorithms=['HS256'])

        user_profile = decoded_id_token
        user = model.get_user_by_line_id(user_profile["sub"])
        user_id = user.id
        return checkIn_controller.check_in(user_id)