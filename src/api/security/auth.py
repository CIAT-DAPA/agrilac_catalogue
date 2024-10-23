from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from datetime import timedelta

app = Flask(__name__)

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Cambiar en producción
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)  # El token expira en 30 minutos
jwt = JWTManager(app)

# Simulación de usuarios
users = {
    "testuser": "testpassword"
}

# Ruta para hacer login y obtener el token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Validar credenciales
    if username not in users or users[username] != password:
        return jsonify({"msg": "Credenciales inválidas"}), 401

    # Crear token de acceso
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Ruta protegida, necesita el Bearer Token
@app.route('/protected', methods=['GET'])
@jwt_required()  # Decorador para validar que hay un token válido
def protected():
    # Obtener la identidad del usuario a partir del token JWT
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Manejo de errores - Token caducado
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "msg": "El token ha expirado",
        "error": "token_expired"
    }), 401

# Manejo de errores - Token inválido (firma incorrecta, manipulado, etc.)
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "msg": "Token inválido",
        "error": "invalid_token"
    }), 422

# Manejo de errores - Token ausente
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "msg": "El token de acceso es necesario",
        "error": "authorization_required"
    }), 401

# Manejo de errores - Token no fresco (si usas fresh tokens)
@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "msg": "El token no es fresco",
        "error": "fresh_token_required"
    }), 401

# Manejo de errores - Token revocado (si se usa revocación de tokens)
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "msg": "El token ha sido revocado",
        "error": "token_revoked"
    }), 401

if __name__ == '__main__':
    app.run(debug=True)
