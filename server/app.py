#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    # getting bakery data from db
    bakeries = Bakery.query.all()

    # iterate over the list and call to_dict() on each object
    bakery_list = [bakery.to_dict() for bakery in bakeries]

    # turns list to json, make_response is for:
    # customizing headers, setting status codes, or returning non-dict responses.
    response = make_response(jsonify(bakery_list), 200)

    ## not necessary to set headers here ##
    ## flask sets to this as default when you jsonify ##
    # response.headers["Content-Type"] = "application/json"

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    # bakery_dict = bakery.to_dict()
    # response = make_response(jsonify(bakery_dict), 200)
    # return response
    
    # bakery = Bakery.query.get(id)
    if bakery:
        return jsonify(bakery.to_dict())
    else:
        return jsonify({'message': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    # baked_goods_list = [bg.to_dict() for bg in baked_goods]
    # response = make_response(jsonify(baked_goods_list), 200)
    # return response
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]
    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        return jsonify(baked_good.to_dict())
    else:
        return jsonify({'message': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
