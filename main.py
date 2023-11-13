from flask import Flask, request, jsonify, json
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple_db.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  desc = db.Column(db.String, nullable=False)

  def __init__(self, name, desc):
    self.name = name
    self.desc = desc


class ItemSchema(ma.Schema):

  class Meta:
    fields = ('id', 'name', 'desc')


item_schema_many = ItemSchema(many=True)
item_schema = ItemSchema()


@app.route('/item', methods=['GET', 'POST'])
def add_item():
  name = request.get_json().get('name')
  desc = request.get_json().get('desc')
  item = Item(name, desc)
  db.session.add(item)
  db.session.commit()
  return item_schema.jsonify(item)


@app.route("/items", methods=['GET'])
def items():
  items = Item.query.all()
  return item_schema_many.jsonify(items)


@app.route("/item/<int:id>", methods=['GET'])
def get_single(id):
  items = Item.query.get(id)
  return item_schema.jsonify(items)


@app.route("/item/<int:id>", methods=['PUT'])
def edit_item(id):
  item = Item.query.get(id)
  name = request.get_json().get('name')
  desc = request.get_json().get('desc')
  item.name = name
  item.desc = desc
  db.session.commit()
  return jsonify({'message': "Item edited sucessfully"})


@app.route("/item/<int:id>", methods=["DELETE"])
def delete_item(id):
  item = Item.query.get(id)
  db.session.delete(item)
  db.session.commit()
  return item_schema.jsonify({'message': "Item removed sucessfully"})


if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(host='0.0.0.0', port=5000, debug=False)
