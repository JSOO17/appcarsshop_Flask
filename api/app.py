import datetime
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from flask_bcrypt import Bcrypt
from datetime import datetime as dt
from api.config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_SECRET_KEY'] = 'secretKey'
from api.models import db, User, user_shema, product_shema, Product, \
                        users_shema, products_shema, Order, order_shema, \
                        ProductOrdered, orders_shema

migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET'])
def home():
    return """<h1>Shoping Cart Project</h1>
    <p>Exercise for Web Python and Docker</p>
    """


@app.route('/api/register', methods=['POST'])
def register():
    password = request.json['password']
    username = request.json['username']

    pw_hash = bcrypt.generate_password_hash(password, 10)

    new_user = User(username, pw_hash)
    db.session.add(new_user)
    db.session.commit()
    result = user_shema.dump(new_user)
    return jsonify(result)

@app.route('/api/login',  methods=['GET'])
def login():
    password = request.json['password']
    username = request.json['username']

    user = User.query.filter(User.username == username).first()

    if password and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    else:
        return make_response('Unauthorized', 401, {"hola": "mundoo"})

@app.route('/api/users', methods=['GET'])
@jwt_required
def get_users():
    users = User.query.all()
    result = users_shema.dump(users)
    return jsonify(result)

@app.route('/api/user/<id>', methods=['GET'])
@jwt_required
def get_user(id):
    user = User.query.get(id)
    result = user_shema.dump(user)
    return jsonify(result)

@app.route('/api/user/<id>', methods=['PUT'])
@jwt_required
def update_user(id):
    try:
        user = User.query.get(id)
        user.username = request.json['username']

        db.session.commit()
        result = user_shema.dump(user)
        return jsonify(result)
    except Exception:
        return f'Could not update {user.username}'


@app.route('/api/user/<id>', methods=['DELETE'])
@jwt_required
def delete_user(id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        result = user_shema.dump(user)
        return jsonify(result)
    except Exception:
        return f'Could not delete {user.username}'


#### Products

@app.route('/api/product', methods=['POST'])
def create_product():
    name = request.json['name']
    price = request.json['price']

    new_product = Product(name, price)
    db.session.add(new_product)
    db.session.commit()
    result = product_shema.dump(new_product)
    return jsonify(result)


@app.route('/api/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    result = product_shema.dump(product)
    return jsonify(result)


@app.route('/api/product', methods=['GET'])
def get_products():
    products = Product.query.all()
    result = products_shema.dump(products)
    return jsonify(result)


@app.route('/api/product/<id>', methods=['PUT'])
@jwt_required
def update_product(id):
    try:
        product = Product.query.get(id)
        product.name = request.json['name']
        product.price = request.json['price']

        db.session.commit()
        result = product_shema.dump(product)
        return jsonify(result)
    except Exception:
        return f'Could not update {product.name}'


@app.route('/api/product/<id>', methods=['DELETE'])
@jwt_required
def delete_product(id):
    try:
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
        result = product_shema.dump(product)
        return jsonify(result)
    except Exception:
        return f'Could not delete {product.name}'

@app.route('/api/order', methods=['POST'])
@jwt_required
def create_order():
    current_user = get_jwt_identity()
    direccion = request.json['direccion']
    fecha = dt.utcnow()
    products = request.json['products']
    new_order = Order(direccion, fecha)
    db.session.add(new_order)
    db.session.commit()
    for product in products:
        product_ordered = ProductOrdered(current_user, product, new_order.id)
        db.session.add(product_ordered)
    db.session.commit()
    
    new_order.products_ordered = products

    return jsonify(order_shema.dump(new_order))


@app.route('/api/order', methods=['GET'])
@jwt_required
def get_orders():
    orders = Order.query.all()
    result = orders_shema.dump(orders)
    return jsonify(result)


if __name__ == '__main__':
    if os.environ.get('PORT') is not None:
        app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
    else:
        app.run(debug=True, host='0.0.0.0')
