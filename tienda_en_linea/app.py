from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configurar la aplicación Flask y la base de datos
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tu_usuario:tu_contraseña@localhost/tienda_en_linea'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir los modelos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock
        }

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email
        }

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow)

    cliente = db.relationship('Cliente', backref=db.backref('pedidos', lazy=True))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'fecha_pedido': self.fecha_pedido.isoformat(),
            'cliente': self.cliente.serialize
        }

# Definir las rutas de la API
@app.route('/')
def index():
    return "Bienvenido a la Tienda en Línea"

# Rutas para productos
@app.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    return jsonify([p.serialize for p in productos])

@app.route('/producto', methods=['POST'])
def add_producto():
    data = request.get_json()
    nuevo_producto = Producto(nombre=data['nombre'], precio=data['precio'], stock=data['stock'])
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify(nuevo_producto.serialize)

# Rutas para clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.serialize for c in clientes])

@app.route('/cliente', methods=['POST'])
def add_cliente():
    data = request.get_json()
    nuevo_cliente = Cliente(nombre=data['nombre'], email=data['email'])
    db.session.add(nuevo_cliente)
    db.session.commit()
    return jsonify(nuevo_cliente.serialize)

# Rutas para pedidos
@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([p.serialize for p in pedidos])

@app.route('/pedido', methods=['POST'])
def add_pedido():
    data = request.get_json()
    nuevo_pedido = Pedido(cliente_id=data['cliente_id'])
    db.session.add(nuevo_pedido)
    db.session.commit()
    return jsonify(nuevo_pedido.serialize)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
