# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 19:37:15 2024

@author: User
"""

import json
import openai
import requests



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

sprawa = input("Opisz sprawe: ")
#sprawa = "chce wziac rozwod stara mnie bije"
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


 

mediatorzy = [['nowak',0.7,'Warszawa',1,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 1, 'BHP': 1, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 1, 'Mobbing': 1, 'Wypadki komunikacyjne': 0}],
['kowalski',0.5,'Warszawa',1,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 1, 'BHP': 0, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 0}],
['kordal',0.2,'Warszawa',1,{'Prawa autorskie i własność intelektualna': 0, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 1, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 1, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 0, 'Nieruchomości': 0, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 1, 'BHP': 0, 'Windykacja': 1, 'Odszkodowania i kary umowne': 1, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 1, 'Mobbing': 1, 'Wypadki komunikacyjne': 0}],
['pogrzeba',0.3,'Kraków',0,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 0, 'Prawo cywilne': 0, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 1, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 1, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 1}],
['miler',0.22,'Warszawa',1,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 1, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 1, 'Spadki i kwestie dziedziczenia': 1, 'Podział majątku przy rozwodzie': 0, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 0, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 1, 'Prawo pracy': 1, 'Prawo gospodarcze - spory przedsiębiorców': 1, 'BHP': 1, 'Windykacja': 1, 'Odszkodowania i kary umowne': 1, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 1, 'Mobbing': 0, 'Wypadki komunikacyjne': 0}],
['nogal',0.65,'Warszawa',1,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 1, 'Podział majątku przy rozwodzie': 0, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 1, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 0, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 0, 'Ochrona wizerunku i dóbr osobistych': 0, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 0, 'Windykacja': 0, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 1, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 1}],
['sornek',0.54,'Warszawa',0,{'Prawa autorskie i własność intelektualna': 0, 'Banki i sprawy finansowe': 1, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 1, 'Spadki i kwestie dziedziczenia': 1, 'Podział majątku przy rozwodzie': 0, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 1, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 0, 'Prawo pracy': 1, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 1, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 1}],
['pawlak',0.74,'Kraków',1,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 1, 'Spadki i kwestie dziedziczenia': 1, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 0, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 1, 'Prawo pracy': 1, 'Prawo gospodarcze - spory przedsiębiorców': 1, 'BHP': 0, 'Windykacja': 1, 'Odszkodowania i kary umowne': 1, 'Reklamacje': 1, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 0, 'Wypadki komunikacyjne': 1}],
['niewiadomski',0.59,'Warszawa',0,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 0, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 1, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 0}],
['weiner',0.71,'Warszawa',1,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 1, 'Podział majątku przy rozwodzie': 0, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 0, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 0, 'Ochrona wizerunku i dóbr osobistych': 0, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 0, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 1, 'Mobbing': 1, 'Wypadki komunikacyjne': 0}],
['kraczla',0.63,'Warszawa',1,{'Prawa autorskie i własność intelektualna': 0, 'Banki i sprawy finansowe': 1, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 1, 'Spadki i kwestie dziedziczenia': 1, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 0, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 0, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 1, 'BHP': 0, 'Windykacja': 0, 'Odszkodowania i kary umowne': 1, 'Reklamacje': 1, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 0, 'Wypadki komunikacyjne': 1}],
['koziol',0.76,'Warszawa',1,{'Prawa autorskie i własność intelektualna': 1, 'Banki i sprawy finansowe': 0, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 1, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 0, 'Ochrona wizerunku i dóbr osobistych': 0, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 1, 'Windykacja': 1, 'Odszkodowania i kary umowne': 1, 'Reklamacje': 0, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 0}],
['mlocek',0.66,'Warszawa',1,{'Prawa autorskie i własność intelektualna': 0, 'Banki i sprawy finansowe': 1, 'Alimenty i sprawy związane z dziećmi przy rozwodach': 0, 'Spadki i kwestie dziedziczenia': 0, 'Podział majątku przy rozwodzie': 1, 'Umowy cywilnoprawne - umowy zlecenie i umowy o dzieło': 0, 'Umowa o pracę': 0, 'Jednoosobowa działalność gospodarcza': 0, 'Kwestie związane z najmem mieszkania i eksmisja': 1, 'Nieruchomości': 1, 'Ochrona wizerunku i dóbr osobistych': 1, 'Prawo cywilne': 1, 'Prawo pracy': 0, 'Prawo gospodarcze - spory przedsiębiorców': 0, 'BHP': 0, 'Windykacja': 1, 'Odszkodowania i kary umowne': 0, 'Reklamacje': 1, 'Zakaz konkurencji i ochrona konsumenta': 0, 'Mobbing': 1, 'Wypadki komunikacyjne': 1}]]
 


score_l= []
for mediator in mediatorzy:
    nazwisko = mediator[0]
    result = 0
    for matching in klient:
        a = mediator[4][matching]
        b = klient[matching]
        c = b - a
        c = abs(c)
        result = (-(result + c))
    result = result/10
    score = [nazwisko, result+mediator[1]]
    score_l.append(score)

        
    