from flask import make_response

import os
import pyqrcode

def create_qrcode(user_id, hash_line_id):
    qr_filename = "qr.png"
    qr_url = f'https://python-line-bot-0113.herokuapp.com/check_in/{user_id}/{hash_line_id}'
    code = pyqrcode.create(qr_url, error='L', version=4, mode='binary')
    code.png(qr_filename, scale=5, module_color=[0, 0, 0, 128], background=[255, 255, 255])
    response = make_response()
    response.data  = open(qr_filename, "rb").read()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=checkInQRCode.png'
    os.remove(qr_filename)
    return response