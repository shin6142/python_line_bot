from flask import Flask, request, abort, render_template, redirect
from models import model

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