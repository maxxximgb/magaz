from flask import *
import Database.Engine.engine as engine

app = Flask('Server')
engine.global_init()
engine.create_session()

@app.route('/', methods=["GET"])
def index():
    return render_template('base.html')

app.run(port=8080)