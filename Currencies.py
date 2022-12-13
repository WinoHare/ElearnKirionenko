import calendar
import datetime
import requests
import xmltodict
import pandas as pd

min_date = datetime.datetime.strptime('01/2003', '%m/%Y')
max_date = datetime.datetime.strptime('08/2022', '%m/%Y')
dicts = {
    'date': [],
    'USD': [],
    'EUR': [],
    'KZT': [],
    'UAH': [],
    'BYR': []
}
while min_date < max_date:
    str_date = datetime.datetime.strftime(min_date, "%m/%Y")
    url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{str_date}=1'
    req = requests.get(url).content
    res = xmltodict.parse(req)['ValCurs']['Valute']
    dicts['date'].append(str_date)
    for cur in res:
        if cur['CharCode'] in dicts.keys():
            dicts[cur['CharCode']].append(float(cur['Value'].replace(',', '.')) / float(cur['Nominal']))
        if cur['CharCode'] == 'BYN':
            dicts['BYR'].append(float(cur['Value'].replace(',', '.')) / float(cur['Nominal']))
    days_in_month = calendar.monthrange(min_date.year, min_date.month)[1]
    min_date += datetime.timedelta(days=days_in_month)

print('')
pd.DataFrame(dicts).to_csv('Data/currencies.csv')




