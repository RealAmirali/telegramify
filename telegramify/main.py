import os, sys
from urllib.parse import quote
import hashlib
import logging

import requests

from flask import Flask, request, render_template

import config

app = Flask(__name__)

app.config['SECRET_KEY'] = config.secret_key


tgBotToken = config.TG_BOT_TOKEN
tgUserID = config.TG_USER_ID
hashedPassword = config.HASHED_PASSWORD

if not (tgBotToken or tgUserID or hashedPassword):
    logging.info("Please add `TG_BOT_TOKEN`, `TG_USER_ID`, `HASHED_PASSWORD` to your config.py and try again")
    sys.exit(1)

baseUrl = "https://api.telegram.org/bot" + tgBotToken + "/sendMessage?chat_id=" + tgUserID + "&text="


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/send', methods=['POST'])
def send():
    sendedHashedPassword = hashlib.sha256(request.form.get('password').encode()).hexdigest()
    content = request.form.get('content')
    if not content:
        return render_template("response.html", code=204, legend="No Content"), 204
    if not (sendedHashedPassword == hashedPassword):
        return render_template("response.html", code=401, legend="Unauthorized"), 401
    
    url = baseUrl + str(quote(content))
    r = requests.get(url)
    if r.status_code == 200:
        return render_template("response.html", code=200, legend="Sent"), 200
    else:
        return render_template("response.html", code=500, legend="Internal Error"), 500
