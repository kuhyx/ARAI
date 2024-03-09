# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 19:09:18 2024

@author: User
"""

# -*- coding: utf-8 -*-


import openai
import os
import pandas as pd
import requests
import json
import time


def kategoryzacja(uzytkownik_input):
	prompt1 = 'Przedstawiam opis sprawy, którą użytkownik chce zgłosić do sądu: \n'
	prompt2_input = uzytkownik_input
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
	print(kategoria_sprawy_num)
