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
        """Gets follower and game data."""
        if not self.is_valid(db):
            self.refresh_token(db)
        token = db.get_evar(db.ACCESS_TOKEN)

        data = dict()

        game_data = self.get_data("channels?broadcaster_id=", token)
        data["game_name"] = game_data[0]["game_name"]
        data["title"] = game_data[0]["title"]

        follow_data = self.get_data("users/follows?to_id=", token)
        follows = [user['from_login'] for user in follow_data]
        data["followers"] = follows

        return data

    def is_valid(self, db):
        """Determines validity of current Access Token."""
        token = db.get_evar(db.ACCESS_TOKEN)
        curl_req = f"curl -X GET 'https://id.twitch.tv/oauth2/validate' \
            -H 'Authorization: Bearer {token}'"
        result = json.loads(os.popen(curl_req).read())
        return "status" not in result
    
    def refresh_token(self, db):
        """Refreshes Access Token."""
        curl_req = "curl -X POST 'https://id.twitch.tv/oauth2/token" + \
            f"?client_id={self.CLIENT_ID}" + \
            f"&client_secret={self.CLIENT_SECRET}" + \
            "&grant_type=client_credentials'"
        result = json.loads(os.popen(curl_req).read())
        db.set_evar(db.ACCESS_TOKEN, result["access_token"])

    def get_data(self, request, token):
        """Returns api data given request and token."""
        req = self.get_request(request, token)

        return json.loads(os.popen(req).read())['data']
    
    def get_request(self, request, token):
        """Returns URL request to open given request and token."""
        return f"curl -X GET \
            'https://api.twitch.tv/helix/{request}{self.TWITCH_USER_ID}' \
            -H 'Authorization: Bearer {token}' -H 'Client-Id: {self.CLIENT_ID}'"

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
                sql = f"INSERT INTO EVENTS (ev_type, ev_msg, ev_extra) VALUES \
                    ('GAMECHANGE', '{new_game}', '" + "{}')"
                db.execute(sql)

            followers = data["followers"]

            for f in followers:
                sql = f"SELECT * FROM FOLLOWERS WHERE user_login='{f}'"
                if len(db.query(sql)) == 0:
                    sql = f"INSERT INTO EVENTS (ev_type, ev_msg, ev_extra) VALUES \
                        ('FOLLOW', '{f}', '" + "{}')"
                    db.execute(sql)
                    sql = f"INSERT INTO FOLLOWERS (user_login) VALUES ('{f}')"
                    db.execute(sql)

            db.disconnect()
            time.sleep(5)
        except:
            pass # Needed to prevent error on reboot
