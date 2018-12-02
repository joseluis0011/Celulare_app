from flask import Blueprint, jsonify, request, render_template
from project.api.models import Cliente
from project import db
from sqlalchemy import exc


cliente_blueprint = Blueprint(
    'cliente', __name__, template_folder='./templates')


@cliente_blueprint.route('/cliente/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'satisfactorio',
        'mensaje': 'Conectado exitosamente!'
    })

@cliente_blueprint.route('/cliente', methods=['POST'])
def add_cliente():
    post_data = request.get_json()
    response_object = {
        'estado': 'falló',
        'mensaje': 'Carga inválida.'
    }
    if not post_data:
        return jsonify(response_object), 400
    nombre = post_data.get('nombre')
    apellido = post_data.get('apellido') 
    try:
        cliente = cliente.query.filter_by(nombre=nombre).first()
        if not cliente:
            db.session.add(cliente(
                nombre=nombre,
                apellido=apellido,
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


@cliente_blueprint.route('/cliente/<cliente_id>', methods=['GET'])
def get_single_cliente(cliente_id):
    """Obteniendo detalles del cliente único"""
    response_object = {
        'estado': 'falló',
        'mensaje': 'El cliente no existe'
    }
    try:
        cliente = Cliente.query.filter_by(id=int(cliente_id)).first()
        if not cliente:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactorio',
                'data': {
                    'id': cliente.id,
                    'nombre': cliente.nombre,
                    'apellido': cliente.apellido
                    }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@cliente_blueprint.route('/cliente', methods=['GET'])
def get_all_cliente():
    """Obteniendo todos los cliente"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'cliente': [cliente.to_json() for cliente in cliente.query.all()]
        }
    }
    return jsonify(response_object), 200


@cliente_blueprint.route('/cliente', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request .form['apellido'] 
        db.session.add(Cliente(
            nombre=nombre,
            apellido=apellido))
        db.session.commit()
    cliente = cliente.query.all()
    return render_template('cliente.html', cliente=cliente)
