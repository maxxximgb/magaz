from flask import Flask, render_template
import Database.Engine.engine as engine

app = Flask('Server')
engine.global_init()
engine.create_session()

@app.route('/', methods=["GET"])
def index():
    return render_template('base.html')

@app.route('/production', methods=["GET"])
def production():
    return render_template('base.html')

@app.route('/about', methods=["GET"])
def about_us():
    return render_template('base.html')

@app.route('/buy', methods=["GET"])
def buy():
    return render_template('base.html')

app.run(host='0.0.0.0', port=8080)