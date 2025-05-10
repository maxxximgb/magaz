import json

from flask import session, jsonify, make_response, request, redirect, url_for
from flask.blueprints import Blueprint
import Database.Engine.Engine as engine
import Misc.Templates as templates
from Database.Classes.Order import Order
from Database.Classes.Product import Product
from Database.Classes.OrderedProduct import OrderedProduct

bpUserApi = Blueprint('user_api', __name__)
dbSession = engine.create_session()


@bpUserApi.route('/user/getCatalog', methods=['GET'])
def getCatalog():
    products = dbSession.query(Product).filter(Product.visible == True).all()
    if not products:
        return make_response('Not found', 404)

    return jsonify([product.to_json() for product in products])


@bpUserApi.route('/user/getProduct/<id>', methods=['GET'])
def getProduct(id):
    product = dbSession.query(Product).filter(Product.id == id).first()
    if not product: return make_response('Not found', 404)
    return jsonify(product.to_json())


@bpUserApi.route('/user/about', methods=['GET'])
def about():
    return templates.about_product.render(isAdmin=bool('uid' in session))


@bpUserApi.route('/user/make_order', methods=['GET', 'POST'])
def makeOrder():
    if request.method == 'GET':
        return templates.make_order.render(isAdmin=bool('uid' in session))

    elif request.method == 'POST':
        data = request.form
        fullname = data.get('fullname')
        phone = data.get('phone')
        products_json = data.get('products', '{}')
        products_data = json.loads(products_json)
        if not products_data: return make_response('Invalid request', 400)

        for details in products_data.values():
            product_id = int(details.get('id'))

            product = dbSession.get(Product, product_id)

            if not product: return make_response('Invalid request', 400)

        new_order = Order(
            customer_name=fullname,
            customer_phone=phone
        )
        dbSession.add(new_order)
        dbSession.flush()

        for details in products_data.values():
            product_id = int(details['id'])
            ordered_product = OrderedProduct(
                product_id=product_id,
                weight=float(details.get('weight', 0)),
                quantity=int(details.get('quantity', 1)),
                order_id=new_order.id
            )
            dbSession.add(ordered_product)

        dbSession.commit()
        return redirect('/user/order_success')