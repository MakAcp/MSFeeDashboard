import requests
from requests import Session
import json
import pandas as pd
import ast
#response = requests.post
session = Session()
session.head("https://yocket.in/universities")
#Performs requests to get more universities

def getUniversities():
    i=1
    dataframe = pd.DataFrame()
    for c in range(1,101):
        print(c)
        try:
            data = {'pageCount': c,'curr_url': '"https://yocket.in/universities' }
            header = { 'X-CSRF-Token': '08f03b4c81ca54ff84f81dcca8ca508460ddc80b47d0a925488ab0715f3e713bd77610fdddfb57554286875c0cb850eb968952e4a914ccccaf8aef721e8eab29'}
            response = session.post(url ="https://yocket.in/universities.json", data = data, headers= header )
            y = response.text
            y.replace('\n', '')
            z = json.loads(y)
            if c==1:
                dataframe = pd.DataFrame(z['universities'])
            else:

                dataframe = dataframe.append(z['universities'], ignore_index=True)
        except Exception:
            print(Exception.__name__)
            break
        print(dataframe.tail())

    dataframe.to_excel('universities.xlsx')


#Converts all fees to USD
def forexConverter():
    failed = []
    forex_dict = {'NZD':0.66, 'EUR':1.18, 'SGD':0.73, 'JPY':0.0095, 'AUD':0.72, 'SEK':0.11, 'CAD':0.76, 'CHF':1.10, 'GBP':1.31, 'USD':1}
    df = pd.read_excel('universities.xlsx')
    for idx, i in df.iterrows():
        print(i['id'])
        try:
            country = dict(ast.literal_eval(i['region']))
            currency = country['country']['forex_currency']['id']
            df.loc[idx,'average_annual_fee'] = i['average_annual_fee']*forex_dict[currency]
            country['country']['forex_currency']['id'] = 'USD'
            country['country']['forex_currency']['symbol'] = '$'
            df.loc[idx,'region'] = str(country)


        except Exception as e:
            print(e)
            failed.append(idx)
            print(i)
    print(failed)
    df.to_excel('universities2.xlsx')


#Converts the Coountry JSON to separate State and COuntry COlumns in the DF

def countryExpander():
    df = pd.read_excel('universities2.xlsx')
    df2 = pd.DataFrame()

    for idx, row in df.iterrows():
        row_dict = dict(row)
        region_tuple = ast.literal_eval(row_dict['region'])
        row_dict['state'] = region_tuple['name']
        row_dict['country'] = region_tuple['country']['name']
        del row_dict['logo']
        del row_dict['url_alias']
        del row_dict['bg_image']
        df2 = df2.append(row_dict, ignore_index=True)

    df2.to_excel('unviersities3.xlsx')


#The Program Processes the data in 3 stages
getUniversities()
forexConverter()
countryExpander()









