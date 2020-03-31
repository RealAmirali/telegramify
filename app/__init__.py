import os, sys
from urllib.parse import quote
import hashlib
import logging

import requests

from flask import Flask, request


app = Flask(__name__)

app.config['SECRET_KEY'] = b'\xcb\xca\xfc\xb0\xd0xs\xca\xc4\x87P\xdf\xf6\x0b\xaaM'


tgBotToken = os.getenv("TG_BOT_TOKEN")
tgUserID = os.getenv("TG_USER_ID")
hashedPassword = os.getenv("HASHED_PASSWORD")

if not (tgBotToken or tgUserID or hashedPassword):
    logging.info("Please add `TG_BOT_TOKEN`, `TG_USER_ID`, `HASHED_PASSWORD` to your environment and try again")
    sys.exit(1)

baseUrl = "https://api.telegram.org/bot" + tgBotToken + "/sendMessage?chat_id=" + tgUserID + "&text="


@app.route('/')
def index():
    return "<form method='POST' action='/send'><input type='text' name='content'><input type='password' name='password'><input type='submit' value='send'></form>"

@app.route('/send', methods=['POST'])
def send():
    sendedHashedPassword = hashlib.sha256(request.form.get('password').encode()).hexdigest()
    content = request.form.get('content')
    if not content:
        return "<img src='https://http.cat/204' /> <br /><a href='/'>Back to Home</a>", 204
    if not (sendedHashedPassword == hashedPassword):
        return "<img src='https://http.cat/401' /><br /><a href='/'>Back to Home</a>", 401
    
    url = baseUrl + str(quote(content))
    r = requests.get(url)
    return "<img src='https://http.cat/200' /><br /><a href='/'>Back to Home</a>", 200

if __name__ == "__main__":
    app.run()
