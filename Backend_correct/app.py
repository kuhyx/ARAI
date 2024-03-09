from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=['POST'])
def statistics_output():
    data = request.get_json()
    cost_of_trial = data.get('response_data', {}).get('cost_of_trial')
    time_of_trial = data.get('response_data', {}).get('time_of_trial')
    
    response = {
        "response_type": "statics_output",
        "response_data": {
            "cost_of_trial": cost_of_trial, # cena w PLN (integer)
            "time_of_trial": time_of_trial # czas w formacie UTC (unix time stamp)
        }
    }

    return jsonify(response)

def recommended_mediators():
    data = request.get_json()
    request_type = data.get('request_type', {}).get('request_type')
    request_data = data.get('request_data', {}).get('experts_called')
    generic_input = data.get('generic_input', {}).get('generic_input')
    trial_cost = data.get('trial_cost', {}).get('trial_cost')
    localization = data.get('localization', {}).get('localization')
    experts_called = data.get('experts_called', {}).get('experts_called')
    witnesses_called = data.get('witnesses_called', {}).get('witnesses_called')

    top_5 = {}
    list_of_mediators = []

    for i in range(5):
        mediator = {}
        top_5.add(mediator)
    
    response = {
        "response_type": "recommended_mediators",
        "response_data": {
            "name": name,
            "specialization": specialization,
            "localization": localization,
            "score": score,
            "number_of_opinions": number_of_opinions
        }
    }

    return jsonify(top_5)

if __name__ == '__main__':
    app.run(debug=True)