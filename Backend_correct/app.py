from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pathlib
import sys
import pandas as pd
import os
import json
import openai
import requests


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@cross_origin()
@app.route("/", methods=['POST'])
def recommended_mediators():
    print("recommended mediators")
    data = request.get_json()
    input = data.get('request_data', {})
    print(input)
    generic_input = input.get("generic_input")
    kategoria = kategoryzacja(generic_input)
    liczba_miesiecy, koszt = calc_stats(kategoria, input.get("trial_value"), input.get("experts_called"))
    returnSprawa = daj_scoring(generic_input)
    print(returnSprawa)

    top_5 = {
        "response_type": "recommended_mediators",
        "response_data": {"first": {
            "cost_of_trial": koszt,
            "time_of_trial": liczba_miesiecy
            }, "second": [{
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
            }]}
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
        print(koszt)
        returnMiesiace = round(liczba_miesiecy,0).to_string(index=False)
        print(returnMiesiace, koszt)
        return returnMiesiace, koszt


def daj_scoring(sprawa):

    # API endpoint URLs
    api_url = "https://lr-lm-sandbox-ams.azure-api.net/language-model-sandbox-legal-and-regulatory-v2-prod/api/chat-completions"
    models_url = "https://lr-lm-sandbox-ams.azure-api.net/language-model-sandbox-legal-and-regulatory-v2-prod/api/chat-completions/models/get"
    
    # Email and API key
    user_id = "firstname.lastname@wolterskluwer.com"
    api_key = "5a1896285bff4376a1edce815639b8cb"
    
    # Headers
    headers = {
    	"Content-Type": "application/json",
    	"Cache-Control": "no-cache",
    	"Ocp-Apim-Subscription-Key": api_key
    }
    
    
    models_response = requests.get(models_url, headers=headers)
    available_models = models_response.json()
    
    chat_params = {
    	"user_id": user_id,
    	"chat_completions_config": {
        	"model_name": "gpt-4-32k",
        	"model_version": "0613",  
        	"temperature": 0,
        	"max_tokens": 500,
        	"top_p": 1,
        	"frequency_penalty": 0,
        	"presence_penalty": 0
    	},
    	"prompt": [{
        	"role": "system",
        	"content": f"{sprawa} zakwalifikuj powyższą sprawę do podanych kategorii: Prawa autorskie i własność intelektualna, Banki i sprawy finansowe, Alimenty i sprawy związane z dziećmi przy rozwodach, Spadki i kwestie dziedziczenia, Podział majątku przy rozwodzie, Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło, Umowa o pracę, Jednoosobowa działalność gospodarcza, Kwestie związane z najmem mieszkania i eksmisja, Nieruchomości, Ochrona wizerunku i dóbr osobistych, Prawo cywilne, Prawo pracy, Prawo gospodarcze - spory przedsiębiorców, BHP, Windykacja, Odszkodowania i kary umowne, Reklamacje, Zakaz konkurencji i ochrona konsumenta, Mobbing, Wypadki komunikacyjne. Dla każdej kategorii podaj 0 jeśli sprawa się jej nie dotyczy, podaj 1 jeśli dotyczy. Zwróc wynik jako liste elementów w formacie {{'kategoria':'wynik','kategoria':'wynik'}}. Wynik to 0 lub 1. Pamietaj aby otworzyc i zamknac {{}} na poczatku i koncu wyniku"
    	}]
    }
    
    chat_response = requests.post(api_url, headers=headers, json=chat_params)
    chat_result = chat_response.json()
    
    output  = chat_result['openai_response']
    
    klient = eval(output)
    
    
     
    
    mediatorzy = [['Emilia Borek', 'Prawo cywilne',0.7,'Warszawa','ul. Chmielna','Tak',1,35,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 1, 'BHP': 1, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 1, 'Mobbing': 1, 'Wypadki komunikacyjne': 0}],
    ['Karol Maciejewski','Prawo gospodarcze',0.5,'Warszawa','ul. Smoleńska','Tak',2,21,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 1, 'BHP': 0, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 0}],
    ['Witkor Pogrzeba','Prawo cywilne',0.2,'Warszawa','al. Niepodległosci','Tak',3,76,{'Prawa autorskie i własność intelektualna': 0, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 1, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 1, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 0, 'Nieruchomości': 0, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 1, 'BHP': 0, 'Windykacja': 1, 'Odszkodowania i kary umowne': 1, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 1, 'Mobbing': 1, 'Wypadki komunikacyjne': 0}],
    ['Marcin Bąk','Prawo pracy',0.3,'Kraków','al. Jana Pawła','Nie',4,37,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 0, 'Prawo cywilne': 0, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 1, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 1, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 1}],
    ['Leszek Millei','Prawo gospodarcze',0.22,'Warszawa','ul. Powstańców Warszawskich','Tak',4.5,65,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 1, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 1, 'Spadki i kwestie dziedziczenia': 1, 'Podział majątku przy rozwodzie': 0, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 0, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 1, 'Prawo pracy': 1, 'Prawo gospodarcze - spory przedsiębiorców': 1, 'BHP': 1, 'Windykacja': 1, 'Odszkodowania i kary umowne': 1, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 1, 'Mobbing': 0, 'Wypadki komunikacyjne': 0}],
    ['Paweł Piecuch','Prawo cywilne',0.65,'Warszawa','ul. Wiejska','Tak',1,99,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 1, 'Podział majątku przy rozwodzie': 0, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 1, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 0, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 0, 'Ochrona wizerunku i dóbr osobistych': 0, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 0, 'Windykacja': 0, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 1, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 1}],
    ['Marcin Ociepa','Prawo gospodarcze',0.54,'Warszawa','ul. Piękna','Nie',2,8,{'Prawa autorskie i własność intelektualna': 0, 'Banki i sprawy finansowe': 1, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 1, 'Spadki i kwestie dziedziczenia': 1, 'Podział majątku przy rozwodzie': 0, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 1, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 0, 'Prawo pracy': 1, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 1, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 1}],
    ['Eliza Mariot','Prawo pracy',0.74,'Kraków','ul. Puławska','Tak',3,16,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 1, 'Spadki i kwestie dziedziczenia': 1, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 0, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 1, 'Prawo pracy': 1, 'Prawo gospodarcze - spory przedsiębiorców': 1, 'BHP': 0, 'Windykacja': 1, 'Odszkodowania i kary umowne': 1, 'Reklamacje': 1, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 0, 'Wypadki komunikacyjne': 1}],
    ['Michał Jelcyn','Prawo pracy',0.59,'Warszawa','al. Wołoska','Nie',4,32,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 0, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 1, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 0}],
    ['Wojciech Werner','Prawo gospodarcze',0.71,'Warszawa','ul. Bitwy pod Grunwaldem','Tak',5,64,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 1, 'Podział majątku przy rozwodzie': 0, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 0, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 0, 'Ochrona wizerunku i dóbr osobistych': 0, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 0, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 1, 'Mobbing': 1, 'Wypadki komunikacyjne': 0}],
    ['Maciej Kroczek','Prawo cywilne',0.63,'Warszawa','al. Tysiąclecia','Nie',1,128,{'Prawa autorskie i własność intelektualna': 0, 'Banki i sprawy finansowe': 1, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 1, 'Spadki i kwestie dziedziczenia': 1, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 0, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 0, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 1, 'BHP': 0, 'Windykacja': 0, 'Odszkodowania i kary umowne': 1, 'Reklamacje': 1, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 0, 'Wypadki komunikacyjne': 1}],
    ['Jan Kozioł','Prawo gospodarcze',0.76,'Warszawa','ul. Grzybowska','Tak',2,256,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 0, 'Ochrona wizerunku i dóbr osobistych': 0, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 1, 'Windykacja': 1, 'Odszkodowania i kary umowne': 1, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 0}],
    ['Leon Sornek','Prawo gospodarcze',0.66,'Warszawa','ul. Długa', 'Tak',3.5,512,{'Prawa autorskie i własność intelektualna': 0, 'Banki i sprawy finansowe': 1, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 0, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 0, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 1, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 1}]]
     
    
    
    score_l= []
    for mediator in mediatorzy:
        name = mediator[0]
        specialization = mediator[1]
        localization = mediator[3]
        street = mediator[4]
        online = mediator[5]
        user_rating = mediator[6]
        result = 0
        for matching in klient:
            a = mediator[8][matching]
            b = klient[matching]
            c = b - a
            c = abs(c)
            result = (-(result + c))
        result = result/10
        ai_rating = result+mediator[2]
        number_of_opinions = mediator[7]
        score = [name, specialization, localization, street, online, ai_rating, user_rating, number_of_opinions]
        score_l.append(score)
    
    lista = []
    for element in score_l:
        e = element[5]
        lista.append(e)
    
    lista_2 = sorted(lista)
    usun_mniejsze_niz = lista_2[3]
    dobra_lista = []        

    for element in score_l:
        if element[5] < usun_mniejsze_niz:
            dobra_lista.append(element)
        else:
            print('')
            
    list_of_json = [json.dumps({"name": item[0], "specialization": item[1], "localization": item[2], "street": item[3], "online": item[4], "ai_rating": item[5], "user_rating": item[6], "number_of_opinions": item[7]}) for item in dobra_lista]

    return list_of_json

def kategoryzacja(input_użytkownika):
    prompt1 = 'Przedstawiam opis sprawy, którą użytkownik chce zgłosić do sądu: \n'
    prompt2_input = input_użytkownika
    prompt3 = 'Zakwalifikuj opis sprawy do najbardziej odpowiedniej z poniższych kategorii i zwróć właściwą liczbę w formacie [number]. \n'
    prompt4 = 'cywilne (przykłady to: sprawy rodzinne, sprawy na podstawie umowy zlecenie, sprawy na podstawie umowy o dzieło, prawa autorskie, własność intelektualna, naruszenie dóbr osobistych np. zniesławienie, bezprawne wykorzystanie wizerunku, naruszenie własności, niewłaściwe posiadanie) [1] \n cywilne (przykłady: szkody geologiczne i górnicze, pęknięcia budynków, ścian - tylko spowodowane przez górnictwo) [2] \n gospodarcze (wszystkie sprawy między przedsiębiorcami, firmami i spółkami, upadłość, restrukturyzacja) [3] \n prawa pracy i ubezpieczeń (wszystkie sprawy związane z umowami o pracę i roszczeniami pracowniczymi np. niezapłacone wynagrodzenia i spory zbiorowe, kary porządkowe dla pracownika) [4]'
    
    prompt_final = prompt1 + prompt2_input + prompt3 + prompt4
    
    # API endpoint URLs
    api_url = "https://lr-lm-sandbox-ams.azure-api.net/language-model-sandbox-legal-and-regulatory-v2-prod/api/chat-completions"
    models_url = "https://lr-lm-sandbox-ams.azure-api.net/language-model-sandbox-legal-and-regulatory-v2-prod/api/chat-completions/models/get"
    
    # Email and API key
    user_id = "firstname.lastname@wolterskluwer.com"
    api_key = "5a1896285bff4376a1edce815639b8cb"
    
    # Headers
    headers = {
    	"Content-Type": "application/json",
    	"Cache-Control": "no-cache",
    	"Ocp-Apim-Subscription-Key": api_key
    }
    
    # Get available models
    models_response = requests.get(models_url, headers=headers)
    available_models = models_response.json()
    
    
    # Define parameters for the chat
    chat_params = {
    	"user_id": user_id,
    	"chat_completions_config": {
        	"model_name": "gpt-4-32k",  # Example model name, replace with desired model
        	"model_version": "0613",  # Example model version, replace with desired version
        	"temperature": 0,
        	"max_tokens": 150,
        	"top_p": 1,
        	"frequency_penalty": 0,
        	"presence_penalty": 0
    	},
    	"prompt": [{
        	"role": "system",
        	"content": prompt_final
    	}]
    }
    
    # Perform the chat
    chat_response = requests.post(api_url, headers=headers, json=chat_params)
    chat_result = chat_response.json()
    
    # Print chat response
    kategoria_sprawy_num = chat_result['openai_response'].replace('[', '').replace(']', '')
    kategoria_sprawy_num = int(kategoria_sprawy_num)
    return kategoria_sprawy_num

if __name__ == '__main__':
    app.run(debug=True)