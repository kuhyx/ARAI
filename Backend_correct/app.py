from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=['POST'])
def recommended_mediators():
    data = request.get_json()

    request_type = data.get('request_type', {}).get('request_type')
    request_data = data.get('request_data', {}).get('experts_called')
    generic_input = data.get('generic_input', {}).get('generic_input')
    trial_cost = data.get('trial_cost', {}).get('trial_cost')
    localization = data.get('localization', {}).get('localization')
    experts_called = data.get('experts_called', {}).get('experts_called')
    witnesses_called = data.get('witnesses_called', {}).get('witnesses_called')

    top_5 = {
        "response_type": "recommended_mediators",
        "response_data": [{
            "cost_of_trial": 5000,
            "time_of_trial": 70
            }, [{
            "name": "Mateusz Szpyruk",
            "specialization": "Prawo podatkowe",
            "localization": localization,
            "ai_rating": 99,
            "user_rating": 99,
            "number_of_opinions": 5
            }, {
            "name": "Jan Kowalski",
            "specialization": "Prawo pracy",
            "localization": localization,
            "ai_rating": 90,
            "user_rating": 99,
            "number_of_opinions": 5
            }, {
            "name": "Jan Kowalski",
            "specialization": "Prawo pracy",
            "localization": localization,
            "ai_rating": 90,
            "user_rating": 99,
            "number_of_opinions": 5
            }]]
        }


    return jsonify(top_5)

if __name__ == '__main__':
    app.run(debug=True)