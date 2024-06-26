from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/tiendaLinea'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición de modelos
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

# Rutas para las vistas y operaciones CRUD
@app.route('/')
def index():
    productos = Producto.query.all()
    clientes = Cliente.query.all()
    pedidos = Pedido.query.all()
    return render_template('index.html', productos=productos, clientes=clientes, pedidos=pedidos)

@app.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

@app.route('/clientes')
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/pedidos')
def pedidos():
    pedidos = Pedido.query.all()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/listado_general')
def listado_general():
    productos = Producto.query.all()
    clientes = Cliente.query.all()
    pedidos = Pedido.query.all()
    return render_template('listado_general.html', productos=productos, clientes=clientes, pedidos=pedidos)

@app.route('/formulario_producto', methods=['GET', 'POST'])
def formulario_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        nuevo_producto = Producto(nombre=nombre, precio=float(precio), stock=int(stock))
        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html')

@app.route('/formulario_cliente', methods=['GET', 'POST'])
def formulario_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        nuevo_cliente = Cliente(nombre=nombre, email=email)
        db.session.add(nuevo_cliente)
        db.session.commit()
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html')

@app.route('/formulario_pedido', methods=['GET', 'POST'])
def formulario_pedido():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        nuevo_pedido = Pedido(cliente_id=int(cliente_id))
        db.session.add(nuevo_pedido)
        db.session.commit()
        return redirect(url_for('pedidos'))
    return render_template('formulario_pedido.html')

@app.route('/producto/delete/<int:id>', methods=['POST'])
def delete_producto(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('productos'))

@app.route('/cliente/delete/<int:id>', methods=['POST'])
def delete_cliente(id):
    cliente = Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('clientes'))

@app.route('/pedido/delete/<int:id>', methods=['POST'])
def delete_pedido(id):
    pedido = Pedido.query.get(id)
    db.session.delete(pedido)
    db.session.commit()
    return redirect(url_for('pedidos'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
