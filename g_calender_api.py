import datetime, re
import googleapiclient.discovery
import google.auth


class CalenderClass(object):
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.calendar_id = 'yamagashin6142@gmail.com'
        self.gapi_creds = google.auth.load_credentials_from_file('credentials.json', self.SCOPES)[0]
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=self.gapi_creds)



class InsertEvent(CalenderClass):
    def insert_event(self):
    # 追加するスケジュールの情報を設定
        event= {
            'summary': 'テスト02',
            'description': '説明テスト説明テスト説明テスト説明テスト説明テスト説明テスト説明テスト説明テスト説明テスト',
            # 予定の開始時刻(ISOフォーマットで指定)
            'start': {
                'dateTime': datetime.datetime(2022, 1, 31, 0, 00).isoformat(),
                'timeZone': 'Japan'
            },
            # 予定の終了時刻(ISOフォーマットで指定)
            'end': {
                'dateTime': datetime.datetime(2022, 1, 31, 17, 59).isoformat(),
                'timeZone': 'Japan'
            },
        }
        # 予定を追加する
        self.service.events().insert(calendarId = self.calendar_id, body = event).execute()


class GetEvent(CalenderClass):
    def get_event(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = self.service.events().list(
            calendarId= self.calendar_id, timeMin=now,
            maxResults=1, singleEvents=True,
            orderBy='startTime').execute()
        
        events_result = events_result.get('items', None)[0]

        result_dict = {}
        result_dict['title'] = events_result['summary']
        result_dict['link'] = events_result['htmlLink']
        result_dict['start_time'] = events_result['start']
        result_dict['end_time'] = events_result['end']
        if 'description' in result_dict:
                result_dict['description'] = events_result['description']
        else:
            result_dict['description'] = ''

        return result_dict