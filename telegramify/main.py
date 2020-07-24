import sys
from urllib.parse import quote
import hashlib
import logging
import uuid

import requests

import toml
from flask import Flask, request, render_template, flash, redirect, url_for

app = Flask(__name__)

try:
    config = toml.loads(open('config.toml', 'r').read())
    app.config['tgBotToken'] = config['tgBotToken']
    app.config['tgUserID'] = config['tgUserID']
    app.config['hashedPassword'] = config['hashedPassword']
    is_init = False
except:
    is_init = True

app.config['SECRET_KEY'] = uuid.uuid4().bytes

@app.route('/')
def index():
    if is_init == True:
        return redirect(url_for('init'))

    return render_template("index.html")

@app.route('/init', methods=['GET', 'POST'])
def init():
    if request.method == 'GET':
        return render_template("init.html")
    else:
        tgBotToken = request.form.get('BotToken')
        tgUserID = request.form.get('UserID')
        password = request.form.get('Password')

        if not (tgBotToken and tgUserID and password):
            flash('Please fill every field')
            return render_template("init.html", color='red')

        hashedPassword = hashlib.sha256(password.encode()).hexdigest()
        config = toml.dumps({'tgBotToken': tgBotToken, 'tgUserID': tgUserID, 'hashedPassword': hashedPassword})
        with open('config.toml', 'w') as f:
            f.write(config)

        app.config['tgBotToken'] = tgBotToken
        app.config['tgUserID'] = tgUserID
        app.config['hashedPassword'] = hashedPassword

        flash("Config file successfully changed")
        return render_template('init.html', color='green')

@app.route('/send', methods=['POST'])
def send():
    baseUrl = "https://api.telegram.org/bot" + app.config['tgBotToken'] + "/sendMessage?chat_id=" + app.config['tgUserID'] + "&text="

    sendedHashedPassword = hashlib.sha256(request.form.get('password').encode()).hexdigest()
    content = request.form.get('content')
    if not content:
        return render_template("response.html", code=204, legend="No Content"), 204
    if not (sendedHashedPassword == app.config['hashedPassword']):
        return render_template("response.html", code=401, legend="Unauthorized"), 401

    url = baseUrl + str(quote(content))
    r = requests.get(url)
    if r.status_code == 200:
        return render_template("response.html", code=200, legend="Sent"), 200
    else:
        return render_template("response.html", code=500, legend="Internal Error"), 500
