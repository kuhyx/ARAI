import requests
import json
import pandas as pd
import argparse
import warnings

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument('-i','--instancja')
parser.add_argument('-t', '--typ')
parser.add_argument('-r', '--rodzaj')

args = parser.parse_args()

TYP = args.typ
RODZAJ = args.rodzaj
INSTANCJA = args.instancja

def load_api(LINK):
    response_API = requests.get(LINK)
    data = response_API.text
    parse_json = json.loads(data)

df = pd.read_excel('dane.xlsx',sheet_name=INSTANCJA)


mask = df['TYP'] == TYP
mask2 = df['RODZAJ'] == RODZAJ
liczba_miesiecy = df[mask][mask2]['mean']
procent = df[mask2]['procent do 3 lat'] * 100

print(f"Średni czas trwania rozprawy typu {TYP}, rodzaju {RODZAJ} wynosi {round(liczba_miesiecy,0).to_string(index=False)} miesięcy, a {procent.to_string(index=False)}% spraw kończy się przed 3 latami")
