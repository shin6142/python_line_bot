import pyqrcode
FILE_PNG_A = 'qrcode_C.png'


def create_qr(user_id):
    file_name = f'check_in_{user_id}.png'
    url = f'https://python-line-bot-0113.herokuapp.com/user_detail/{user_id}'
    code = pyqrcode.create(url, error='L', version=4, mode='binary')
    code.png(FILE_PNG_A, scale=5, module_color=[0, 0, 0, 128], background=[255, 255, 255])