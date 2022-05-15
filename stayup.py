from flask import Flask
from threading import Thread

""" this is the web app the program runs on

the app is pinged every half hour to prevent timeout

it still goes offline every couple weeks
"""

app = Flask('')

@app.route('/')
def home():
    return "Keep rollin', rollin', rollin', rollin'"

def run():
  app.run(host='0.0.0.0',port=8080)

def keepRollin():
    t = Thread(target=run)
    t.start()