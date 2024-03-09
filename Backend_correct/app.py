from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pathlib
import sys
import pandas as pd
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@cross_origin()
@app.route("/", methods=['POST'])
def recommended_mediators():
    data = request.get_json()

    input = data.get('request_data', {})
    
    tmp = os.system('python3 ..\statystyki\load_data.py -t 1 -k 25000 -b True')
    print(tmp)

    top_5 = {
        "response_type": "recommended_mediators",
        "response_data": [{
            "cost_of_trial": 5000,
            "time_of_trial": 70
            }, [{
            "name": "Mateusz Szpyruk",
            "specialization": "Prawo podatkowe",
            "location": input.get("location"),
            "ai_rating": 99,
            "user_rating": 99,
            "number_of_opinions": 5
            }, {
            "name": "Jan Kowalski",
            "specialization": "Prawo pracy",
            "location": input.get("location"),
            "ai_rating": 90,
            "user_rating": 99,
            "number_of_opinions": 5
            }, {
            "name": "Jan Kowalski",
            "specialization": "Prawo pracy",
            "location": input.get("location"),
            "ai_rating": 90,
            "user_rating": 99,
            "number_of_opinions": 5
            }], tmp]
        }

    return jsonify(tmp)

if __name__ == '__main__':
    app.run(debug=True)