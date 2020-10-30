from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.app import app

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    products_ordered = db.relationship('ProductOrdered', backref='user')

    def __init__(self, username, password=None):
        self.username = username
        if password is not None:
            self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    products_ordered = db.relationship('ProductOrdered', backref='product')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return '<Product {}>'.format(self.name)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    direccion = db.Column(db.String(128))
    fecha = db.Column(db.DateTime)
    products_ordered = db.relationship('ProductOrdered', backref='order')

    def __init__(self, direccion, fecha):
        self.direccion = direccion
        self.fecha = fecha

    def __repr__(self):
        return '<Order >'

class ProductOrdered(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
    order_id = db.Column('order_id', db.Integer, db.ForeignKey('order.id'))

    def __init__(self, user_id, product_id, order_id):
        self.user_id = user_id
        self.product_id = product_id
        self.order_id = order_id

    def __repr__(self):
        return '<ProductOrdered >'

ma = Marshmallow(app)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True

class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_relationships = True

class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        include_relationships = True


# Para cuando quiera interactuar con un solo registro
user_shema = UserSchema()
product_shema = ProductSchema()
order_shema = OrderSchema()


# Para cuando quiera interactuar con varios registros
users_shema = UserSchema(many=True)
products_shema = ProductSchema(many=True)
orders_shema = OrderSchema(many=True)
