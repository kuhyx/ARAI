from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def recommended_mediators():
    data = request.get_json()

    input = data.get('request_data', {})
    # print(input.get("location"))

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
            }]]
        }


    return jsonify(top_5)

if __name__ == '__main__':
    app.run(debug=True)