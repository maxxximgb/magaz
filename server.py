from Misc import Setup
from threading import Thread
import werkzeug.security
from flask import Flask, request, session, redirect, make_response, jsonify
from Misc.Console import ConsoleWorker, setHook
import Misc.Templates as templates
from Blueprints.AdminAPI import bpAdminApi
from Blueprints.UserAPI import bpUserApi
from Database.Classes.Admin import Admin
import Database.Engine.Engine as engine
import hashlib

app = Flask('Server')
app.secret_key = hashlib.sha256(
    'Пожуйлиста ни варуйти этат ключь патаму шо если вы иво сваруете то пользавателей патом взламают!'.encode(
        'UTF-8') + b'P.S postavbte 100 ballov proekty\xec*rx\rs#4+.', usedforsecurity=True).digest()
engine.global_init()
dbSession = engine.create_session()


@app.before_request
def before_request():
    app.requests += 1
    if app.shutting_down:
        return jsonify({
            "error": "Запрос не завершен. Удаленный сервер завершает свою работу."
        }), 503


@app.after_request
def after_request(response):
    app.requests -= 1
    return response


@app.route('/', methods=["GET"])
def index():
    return templates.index.render(isAdmin=bool('uid' in session))


@app.route('/production', methods=["GET"])
def production():
    return templates.production.render(isAdmin=bool('uid' in session))


@app.route('/about', methods=["GET"])
def about_us():
    return templates.about.render(isAdmin=bool('uid' in session))


@app.route('/catalog', methods=["GET"])
def buy():
    return templates.catalog.render(isAdmin=bool('uid' in session))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not request.form.items():
            return make_response('Нет данных для входа', 403)

        admin = dbSession.query(Admin).filter(Admin.login == request.form.get('login')).first()
        if not admin:
            return make_response('Пользователь не найден в системе', 403)

        if not werkzeug.security.check_password_hash(admin.hashed_password, request.form.get('password')):
            return make_response('Неверный пароль', 403)

        session.new = True
        session['uid'] = admin.id
        session.permanent = True
        return redirect('/admin/dashboard')

    elif request.method == "GET":
        return templates.login.render()


@app.route('/cart', methods=['GET'])
def cart():
    return templates.cart.render(isAdmin=bool('uid' in session))


@app.route('/logout', methods=["GET"])
def logout():
    if 'uid' in session:
        session.clear()
    return redirect('/')


setHook(app)
app.register_blueprint(bpAdminApi)
app.register_blueprint(bpUserApi)
Thread(target=ConsoleWorker).start()

app.run('0.0.0.0', 8080)
