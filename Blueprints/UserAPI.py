from flask import session, jsonify, make_response
from flask.blueprints import Blueprint

import Database.Engine.Engine as engine
import Misc.Templates as templates
from Database.Classes.Product import Product

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
    return jsonify(dbSession.query(Product).filter(Product.id == id).first().to_json())


@bpUserApi.route('/user/about', methods=['GET'])
def buy():
    return templates.about_product.render(isAdmin=bool('uid' in session))
