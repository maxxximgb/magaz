from flask import *

app = Flask('Server')

@app.route('/', methods=["GET"])
def index():
    return render_template('base.html')

app.run(port=8080)