import pandas as pd
import argparse
import warnings

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--typ')
parser.add_argument('-k','--kwota')
parser.add_argument('-b', '--biegly')

args = parser.parse_args()

TYP = args.typ
KWOTA = int(args.kwota)
BIEGLY = str(args.biegly)

def calc_stats(typ=TYP,KWOTA=KWOTA,BIEGLY = BIEGLY):
    mapka = {'1':'cywilnej','2':'górniczej','3':'gospodarczej','4':'prawa pracy & ubezpieczeń'}
    koszt_bieglego= 1789.42
    koszt = 0
    if KWOTA < 100000 and typ != '4':
        df = pd.read_excel('dane.xlsx',sheet_name='rejon')
        mask = df['RODZAJ'] == int(typ)
        liczba_miesiecy = df[mask]['mean']
        procent = (1 - df[mask]['procent do 12 miesięcy']) * 100
        koszt_sadu = 0
        koszt_adwokata = 0
        if KWOTA <= 500:
            koszt_sadu = 30
            koszt_adwokata = 90
        elif KWOTA > 500 and KWOTA <= 1500:
            koszt_sadu = 100
            koszt_adwokata = 270
        elif KWOTA > 1500 and KWOTA <= 4000:
            koszt_sadu = 200
        elif KWOTA > 4000 and KWOTA <= 7500:
            koszt_sadu = 400
        elif KWOTA > 7500 and KWOTA <= 10000:
            koszt_sadu = 500    
        elif KWOTA > 10000 and KWOTA <= 15000:
            koszt_sadu = 750
        elif KWOTA > 15000 and KWOTA <= 20000:
            koszt_sadu = 1000
        elif KWOTA > 20000:
            koszt_sadu = KWOTA * 0.05
            if koszt_sadu > 20000:
                koszt_sadu = 20000

        if KWOTA > 1500 and KWOTA <= 5000:
            koszt_adwokata = 900
        elif KWOTA > 5000 and KWOTA <= 10000:
            koszt_adwokata = 1800
        elif KWOTA > 10000 and KWOTA <= 50000:
            koszt_adwokata = 3600    
        elif KWOTA > 50000 and KWOTA <= 100000:
            koszt_adwokata = 5400

        
        if BIEGLY == 'True':
            koszt = koszt_sadu + koszt_adwokata + koszt_bieglego
        else:
            koszt = koszt_sadu + koszt_adwokata
        print(f"Średni czas trwania rozprawy typu {mapka[typ]} wynosi {round(liczba_miesiecy,0).to_string(index=False)} miesięcy, a {procent.to_string(index=False)}% spraw trwa dłuzej niz rok, jej minimalny koszt wyniesie {koszt}")
    
    elif KWOTA > 100000:
        df = pd.read_excel('dane.xlsx',sheet_name='okreg')
        mask = df['RODZAJ'] == int(typ)
        liczba_miesiecy = df[mask]['mean']
        procent = (1 - df[mask]['procent do 12 miesięcy']) * 100

        if KWOTA <= 200000:
            koszt_adwokata = 5400
        elif KWOTA > 200000 and KWOTA <= 2000000:
            koszt_adwokata = 10800
        elif KWOTA > 2000000 and KWOTA <= 5000000:
            koszt_adwokata = 15000
        elif KWOTA > 500000:
            koszt_adwokata = 25000
        
        koszt_sadu = KWOTA * 0.05
        if koszt_sadu > 20000:
            koszt_sadu = 20000
        
        if BIEGLY == 'True':
            koszt = koszt_sadu + koszt_adwokata + koszt_bieglego
        else:
            koszt = koszt_sadu + koszt_adwokata

        print(f"Średni czas trwania rozprawy typu {mapka[TYP]} wynosi {round(liczba_miesiecy,0).to_string(index=False)} miesięcy, a {procent.to_string(index=False)}% spraw trwa krócej niz rok, a jej minimalny koszt wynosi {koszt}")

calc_stats()