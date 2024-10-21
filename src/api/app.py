from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_cors import CORS, cross_origin
from datetime import timedelta
from services.filesmanager import *
import json


app = Flask(__name__)
# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Cambiar en producción
jwt = JWTManager(app)
revoked_tokens = set()

# Simulación de usuarios
users = {
    "testuser": "testpassword"
}

CORS(app)
@cross_origin
# Ruta para hacer login y obtener el token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    expiration_minutes = request.json.get('expiration', 30)  # Obtener tiempo de expiración, por defecto 30 minutos

    # Validar credenciales
    if username not in users or users[username] != password:
        return jsonify({"msg": "Credenciales inválidas"}), 401

    # Crear el token de acceso con un tiempo de expiración dinámico
    expires = timedelta(minutes=expiration_minutes)
    access_token = create_access_token(identity=username, expires_delta=expires)

    return jsonify(access_token=access_token), 200

# Ruta para revocar token (cerrar sesión)
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']  # Obtener el ID del token (jti)
    revoked_tokens.add(jti)  # Marcar el token como revocado
    return jsonify({"msg": "Token revocado con éxito"}), 200

# Verificar si el token ha sido revocado
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']  # Obtener el ID del token
    return jti in revoked_tokens  # Verificar si el token está revocado


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
    app.run(debug=True,host='0.0.0.0',port=5001)
