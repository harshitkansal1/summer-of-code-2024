from flask import jsonify
from . import create_app

app = create_app()

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})