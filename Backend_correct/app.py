from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=['GET'])
def recommended_mediators():
    data = request.get_json()

    request_type = data.get('request_data', {})
    print(request_type)

    top_5 = {
        "response_type": "recommended_mediators",
        "response_data": [{
            "cost_of_trial": 5000,
            "time_of_trial": 70
            }, [{
            "name": "Mateusz Szpyruk",
            "specialization": "Prawo podatkowe",
            "location": "Katowice",
            "ai_rating": 99,
            "user_rating": 99,
            "number_of_opinions": 5
            }, {
            "name": "Jan Kowalski",
            "specialization": "Prawo pracy",
            "location": "Katowice",
            "ai_rating": 90,
            "user_rating": 99,
            "number_of_opinions": 5
            }, {
            "name": "Jan Kowalski",
            "specialization": "Prawo pracy",
            "location": "Katowice",
            "ai_rating": 90,
            "user_rating": 99,
            "number_of_opinions": 5
            }]]
        }


    return jsonify(top_5)

if __name__ == '__main__':
    app.run(debug=True)