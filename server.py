from flask import Flask
import Misc.Templates as templates
import Database.Engine.engine as engine

app = Flask('Server')
engine.global_init()
engine.create_session()

@app.route('/', methods=["GET"])
def index():
    return templates.index.render()

@app.route('/production', methods=["GET"])
def production():
    return templates.production.render()

@app.route('/about', methods=["GET"])
def about_us():
    return templates.about.render()

@app.route('/buy', methods=["GET"])
def buy():
    return templates.buy.render()

app.run(host='0.0.0.0', port=8080)