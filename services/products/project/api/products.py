# services/products/project/api/products.py


from flask import Blueprint, jsonify, request, render_template
from project.api.models import Product
from project import db
from sqlalchemy import exc


products_blueprint = Blueprint(
    'products', __name__, template_folder='./templates')


@products_blueprint.route('/products/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'satisfactorio',
        'mensaje': 'Conectado exitosamente!'
    })


@products_blueprint.route('/products', methods=['POST'])
def add_product():
    post_data = request.get_json()
    response_object = {
        'estado': 'falló',
        'mensaje': 'Carga inválida.'
    }
    if not post_data:
        return jsonify(response_object), 400
    nombre = post_data.get('nombre')
    cantidad = post_data.get('cantidad')
    serie = post_data.get('serie')
    modelo = post_data.get('modelo')
    marca = post_data.get('marca')
    try:
        product = Product.query.filter_by(nombre=nombre).first()
        if not product:
            db.session.add(Product(
                nombre=nombre,
                cantidad=cantidad,
                serie=serie,
                modelo=modelo,
                marca=marca,
                ))
            db.session.commit()
            response_object['estado'] = 'perfecto'
            response_object['mensaje'] = f'{nombre} se ha agregado!!!'
            return jsonify(response_object), 201
        else:
            response_object['estado'] = 'falló'
            response_object['mensaje'] = 'El nombre ya existe.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@products_blueprint.route('/products/<product_id>', methods=['GET'])
def get_single_product(product_id):
    """Obteniendo detalles del producto único"""
    response_object = {
        'estado': 'falló',
        'mensaje': 'El producto no existe'
    }
    try:
        product = Product.query.filter_by(id=int(product_id)).first()
        if not product:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactorio',
                'data': {
                    'id': product.id,
                    'nombre': product.nombre,
                    'cantidad': product.cantidad,
                    'serie': product.serie,
                    'modelo': product.modelo,
                    'marca': product.marca
                    }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@products_blueprint.route('/products', methods=['GET'])
def get_all_products():
    """Obteniendo todos los productos"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'products': [product.to_json() for product in Product.query.all()]
        }
    }
    return jsonify(response_object), 200


@products_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        serie = request .form['serie']
        modelo = request.form['modelo']
        marca = request.form['marca']
        db.session.add(Product(
            nombre=nombre,
            cantidad=cantidad,
            serie=serie,
            modelo=modelo,
            marca=marca))
        db.session.commit()
    products = Product.query.all()
    return render_template('index.html', products=products)
