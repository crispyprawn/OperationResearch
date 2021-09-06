from flask import Flask, request
from chapter3 import simplex_fractional
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        matrix = json.loads(request.form.get('matrix'))
        return simplex_fractional.handle_request(matrix)

    return 'hello'
