# sudo pip3 install python-dotenv
from dotenv import load_dotenv
from os.path import exists
from db_conn import *
import time
import json
import os

class TwitchAPI():

    def __init__(self):
        if not exists(".env"):
            raise Exception(".env file not found")
        
        load_dotenv()
        self.CLIENT_ID = os.getenv('CLIENT_ID')
        self.CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        self.TWITCH_USER = os.getenv('TWITCH_USER')
        self.TWITCH_USER_ID = os.getenv('TWITCH_USER_ID')

    def get_twitch_data(self, db):
        if not self.is_valid(db):
            self.refresh_token(db)
        
        data = dict()

        token = db.get_evar(db.ACCESS_TOKEN)

        stream_curl_req = f"curl -X GET \
            'https://api.twitch.tv/helix/channels?broadcaster_id={self.TWITCH_USER_ID}' \
            -H 'Authorization: Bearer {token}' \
            -H 'Client-Id: {self.CLIENT_ID}'"
        
        result = json.loads(os.popen(stream_curl_req).read())
        data["game_name"] = result["data"][0]["game_name"]
        data["title"] = result["data"][0]["title"]

        follows_curl_req = f"curl -X GET \
            'https://api.twitch.tv/helix/users/follows?to_id={self.TWITCH_USER_ID}' \
            -H 'Authorization: Bearer {token}' \
            -H 'Client-Id: {self.CLIENT_ID}'"
        
        result = json.loads(os.popen(follows_curl_req).read())
        follow_data = result['data']
        follows = []
        for user in follow_data:
            follows.append(user['from_login'])

        data["followers"] = follows

        return data

    def is_valid(self, db):
        token = db.get_evar(db.ACCESS_TOKEN)
        curl_req = f"curl -X GET 'https://id.twitch.tv/oauth2/validate' \
            -H 'Authorization: Bearer {token}'"
        result = json.loads(os.popen(curl_req).read())
        return "status" not in result
    
    def refresh_token(self, db):
        curl_req = "curl -X POST 'https://id.twitch.tv/oauth2/token" + \
            f"?client_id={self.CLIENT_ID}" + \
            f"&client_secret={self.CLIENT_SECRET}" + \
            "&grant_type=client_credentials'"
        result = json.loads(os.popen(curl_req).read())
        db.set_evar(db.ACCESS_TOKEN, result["access_token"])

if __name__ == "__main__":
    twitch_api = TwitchAPI()
    db = DBConn()

    while True:
        try:
            db.connect()

            data = twitch_api.get_twitch_data(db)

            curr_game = db.get_evar(db.CURR_GAME)

            new_game = data["game_name"]

            if new_game != curr_game:
                db.set_evar(db.CURR_GAME, new_game)
                sql = "INSERT INTO EVENTS (ev_type, ev_extra) VALUES " + \
                    f"('GAMECHANGE', '{new_game}')"
                db.execute(sql)

            followers = data["followers"]

            for f in followers:
                sql = f"SELECT * FROM FOLLOWERS WHERE user_login='{f}'"
                res = db.query(sql)
                if len(res) == 0:
                    sql = "INSERT INTO EVENTS (ev_type, ev_extra) VALUES " + \
                        f"('FOLLOW', '{f}')"
                    db.execute(sql)
                    sql = f"INSERT INTO FOLLOWERS (user_login) VALUES ('{f}')"
                    db.execute(sql)

            db.disconnect()
            time.sleep(5)
        except:
            pass