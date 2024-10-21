from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos MySQL en Amazon RDS
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<usuario>:<contraseña>@<endpoint>:<puerto>/<nombre_base_datos>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo de base de datos
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f"Item(id={self.id}, name={self.name}, description={self.description})"

# Crear la base de datos
with app.app_context():
    db.create_all()

# Ruta para obtener todos los elementos
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name, 'description': item.description} for item in items])

# Ruta para obtener un solo elemento por su ID
@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify({'id': item.id, 'name': item.name, 'description': item.description})

# Ruta para crear un nuevo elemento
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'], description=data.get('description', ''))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item creado con éxito'}), 201

# Ruta para actualizar un elemento
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    item = Item.query.get_or_404(id)
    
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    
    db.session.commit()
    return jsonify({'message': 'Item actualizado con éxito'})

# Ruta para eliminar un elemento
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item eliminado con éxito'})

if __name__ == '__main__':
    app.run(debug=True)
