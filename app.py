from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.before_request
def init_session():
    if 'products' not in session:
        session['products'] = []

@app.route('/')
def index():
    return render_template('index.html', products=session['products'])

@app.route('/add', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        new_id = len(session['products']) + 1
        new_product = {
            'id': new_id,
            'nombre': request.form['nombre'],
            'cantidad': request.form['cantidad'],
            'precio': request.form['precio'],
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        session['products'].append(new_product)
        session.modified = True
        return redirect(url_for('index'))
    return render_template('nuevo_producto.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def editar(id):
    product = next((prod for prod in session['products'] if prod['id'] == id), None)
    if request.method == 'POST':
        product['nombre'] = request.form['nombre']
        product['cantidad'] = request.form['cantidad']
        product['precio'] = request.form['precio']
        product['fecha_vencimiento'] = request.form['fecha_vencimiento']
        product['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    return render_template('editar.html', product=product)

@app.route('/delete/<int:id>')
def delete_product(id):
    session['products'] = [prod for prod in session['products'] if prod['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
