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
    
    result = calc_stats("2", 25000, True)
    print(result)

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


def calc_stats(typ,kwota,biegly):
    mapka = {'1':'cywilnej','2':'górniczej','3':'gospodarczej','4':'prawa pracy & ubezpieczeń'}
    koszt_bieglego= 1789.42
    koszt = 0
    danePath = 'dane.xlsx'
    if kwota < 100000 and typ != '4':
        df = pd.read_excel(danePath,sheet_name='rejon')
        mask = df['RODZAJ'] == int(typ)
        liczba_miesiecy = df[mask]['mean']
        procent = (1 - df[mask]['procent do 12 miesięcy']) * 100
        koszt_sadu = 0
        koszt_adwokata = 0
        if kwota <= 500:
            koszt_sadu = 30
            koszt_adwokata = 90
        elif kwota > 500 and kwota <= 1500:
            koszt_sadu = 100
            koszt_adwokata = 270
        elif kwota > 1500 and kwota <= 4000:
            koszt_sadu = 200
        elif kwota > 4000 and kwota <= 7500:
            koszt_sadu = 400
        elif kwota > 7500 and kwota <= 10000:
            koszt_sadu = 500    
        elif kwota > 10000 and kwota <= 15000:
            koszt_sadu = 750
        elif kwota > 15000 and kwota <= 20000:
            koszt_sadu = 1000
        elif kwota > 20000:
            koszt_sadu = kwota * 0.05
            if koszt_sadu > 20000:
                koszt_sadu = 20000

        if kwota > 1500 and kwota <= 5000:
            koszt_adwokata = 900
        elif kwota > 5000 and kwota <= 10000:
            koszt_adwokata = 1800
        elif kwota > 10000 and kwota <= 50000:
            koszt_adwokata = 3600    
        elif kwota > 50000 and kwota <= 100000:
            koszt_adwokata = 5400

        
        if biegly == 'True':
            koszt = koszt_sadu + koszt_adwokata + koszt_bieglego
        else:
            koszt = koszt_sadu + koszt_adwokata
        print(f"Średni czas trwania rozprawy typu {mapka[typ]} wynosi {round(liczba_miesiecy,0).to_string(index=False)} miesięcy, a {procent.to_string(index=False)}% spraw trwa dłuzej niz rok, jej minimalny koszt wyniesie {koszt}")
    
    elif kwota > 100000:
        df = pd.read_excel(danePath,sheet_name='okreg')
        mask = df['RODZAJ'] == int(typ)
        liczba_miesiecy = df[mask]['mean']
        procent = (1 - df[mask]['procent do 12 miesięcy']) * 100

        if kwota <= 200000:
            koszt_adwokata = 5400
        elif kwota > 200000 and kwota <= 2000000:
            koszt_adwokata = 10800
        elif kwota > 2000000 and kwota <= 5000000:
            koszt_adwokata = 15000
        elif kwota > 500000:
            koszt_adwokata = 25000
        
        koszt_sadu = kwota * 0.05
        if koszt_sadu > 20000:
            koszt_sadu = 20000
        
        if biegly == 'True':
            koszt = koszt_sadu + koszt_adwokata + koszt_bieglego
        else:
            koszt = koszt_sadu + koszt_adwokata

        return_string = f"Średni czas trwania rozprawy typu {mapka[TYP]} wynosi {round(liczba_miesiecy,0).to_string(index=False)} miesięcy, a {procent.to_string(index=False)}% spraw trwa krócej niz rok, a jej minimalny koszt wynosi {koszt}"     
        print(return_string)

        return return_string
if __name__ == '__main__':
    app.run(debug=True)