from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Review, Item, Customer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Flask SQLAlchemy Lab 2</h1>'

@app.route('/reviews')
def all_reviews():
    q = Review.query.all()
    return jsonify([r.to_dict() for r in q]), 200

@app.route('/items')
def all_items():
    q = Item.query.all()
    return jsonify([i.to_dict(rules=('-reviews.item_id', '-reviews.customer_id')) for i in q]), 200

@app.route('/customers')
def all_customers():
    q = Customer.query.all()
    return jsonify([c.to_dict() for c in q]), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
