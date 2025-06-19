#!/usr/bin/env python3

from flask import Flask, jsonify
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

# GET /bakeries - all bakeries
@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in all_bakeries])

# GET /bakeries/<int:id> - bakery by ID, with nested baked_goods
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.to_dict())

# GET /baked_goods/by_price - sorted by price (desc)
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([good.to_dict() for good in goods])

# GET /baked_goods/most_expensive - highest price baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if good:
        return jsonify(good.to_dict())
    return jsonify({})

if __name__ == '__main__':
    app.run(port=5555, debug=True)
