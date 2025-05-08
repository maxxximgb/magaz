import os.path

from flask import session, jsonify, request, redirect
from flask.blueprints import Blueprint

import Database.Engine.Engine as engine
import Misc.Templates as templates
from Database.Classes.Order import Order
from Database.Classes.Product import Product

bpAdminApi = Blueprint('admin_api', __name__)
dbSession = engine.create_session()


@bpAdminApi.route('/admin/getOrders', methods=['GET'])
def getOrders():
    if not session.get('uid'): return 'Unauthorized', 401

    orders = dbSession.query(Order).all()
    if not orders: return 'No Orders', 404

    return jsonify([order.to_json() for order in orders])


@bpAdminApi.route('/admin/getCatalog')
def getCatalog():
    if not session.get('uid'): return 'Unauthorized', 401
    products = dbSession.query(Product).all()
    return jsonify([product.to_json() for product in products])


@bpAdminApi.route('/admin/catalog', methods=['GET'])
def catalog():
    if not session.get('uid'): return 'Unauthorized', 401
    return templates.catalog_edit.render()


@bpAdminApi.route('/admin/newProduct', methods=['GET', 'POST'])
def newProduct():
    if not session.get('uid'): return 'Unauthorized', 401
    if request.method == 'GET':
        return templates.newProduct.render()
    elif request.method == 'POST':
        product = Product(
            name=request.form['name'],
            minWeight=int(request.form['minWeight']),
            pricePerKg=float(int(request.form['price']) / int(request.form['minWeight']) * 1000),
            visible='is_visible' in request.form
        )
        dbSession.add(product)
        dbSession.flush()

        file = request.files['image']
        if file and file.filename != '':
            product_id = product.id
            upload_dir = os.path.join('static', 'img', 'products', str(product_id))
            os.makedirs(upload_dir, exist_ok=True)

            ext = file.filename.split('.')[-1]
            file.save(f'{upload_dir}/image.{ext}')
            product.imageSrc = '/'.join(['', 'static', 'img', 'products', str(product_id),  f'image.{ext}'])

        dbSession.commit()
        return redirect('/admin/catalog')


@bpAdminApi.route('/admin/dashboard', methods=["GET"])
def dashboard():
    if not session.get('uid'): return 'Unauthorized', 401
    return templates.dashboard.render()
