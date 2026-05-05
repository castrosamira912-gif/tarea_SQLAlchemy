from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# =========================
# CONFIGURACIÓN DB
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# MODELO (Product)
# =========================
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)          # ID (PK)
    name = db.Column(db.String(100), nullable=False)      # Nombre (no nulo)
    price = db.Column(db.Float, nullable=False)           # Precio (no nulo)
    stock = db.Column(db.Integer, default=0)              # Stock (default 0)

# =========================
# CREAR BASE DE DATOS (FLASK 3)
# =========================
with app.app_context():
    db.create_all()

# =========================
# READ ALL (listar productos)
# =========================
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# =========================
# CREATE (crear producto)
# =========================
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form.get('stock', 0) or 0)  # evita error si está vacío

        new_product = Product(name=name, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')

# =========================
# READ ONE (detalle)
# =========================
@app.route('/product/<int:id>')
def detail(id):
    product = Product.query.get_or_404(id)
    return render_template('detail.html', product=product)

# =========================
# UPDATE (editar)
# =========================
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.stock = int(request.form.get('stock', 0) or 0)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', product=product)

# =========================
# DELETE (eliminar)
# =========================
@app.route('/delete/<int:id>')
def delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)