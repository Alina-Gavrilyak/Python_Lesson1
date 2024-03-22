import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


URL_TEMPLATE = "https://pogoda.unian.net/85486-kiev"
URL_TEMPLATE2 = "https://meteo.ua/34/kiev#2024-03-19--20-00"
URL_TEMPLATE3 = "https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2"
URL_TEMPLATE4 = "https://www.pogodairadar.com/stranitsa-pogodyi/kiev/4868738"
FILE_NAME = "test.csv"


r = requests.get(URL_TEMPLATE)
r2 = requests.get(URL_TEMPLATE2)
r3 = requests.get(URL_TEMPLATE3)
r4 = requests.get(URL_TEMPLATE4)
# print(r3.status_code)
# print(r3.text)


def parse(url=r):
    result_list = {'dates': [], 'max_temps': [], 'min_temps': []}
    soup = bs(url.text, "html.parser")
    dates = soup.find_all('div', class_='forecastCalendar__dayOfWeek')
    max_temps = soup.find_all('div', class_='forecastCalendar__temp')
    min_temps = soup.find_all('div', class_='forecastCalendar__number--small', limit=7)
    for date in dates:
        result_list['dates'].append(date.span.text)
    for max_temp in max_temps:
        result_list['max_temps'].append(max_temp.div.text)
    for min_temp in min_temps:
        result_list['min_temps'].append(min_temp.text)
    print("\nThe information was taken from the site: https://pogoda.unian.net/85486-kiev")
    for keys, values in result_list.items():
        print(keys, " : ", values)
    return result_list


def parse2(url2=r2):
    result_list2 = {'dates': [], 'temps': []}
    soup2 = bs(url2.text, "html.parser")
    dates2 = soup2.find_all('div', class_='menu-basic__day')
    temps2 = soup2.find_all('div', class_='menu-basic__degree')
    for date in dates2:
        result_list2['dates'].append(date.text.replace('\n', ''))
    for temp in temps2:
        result_list2['temps'].append(temp.text)
    print("\nThe information was taken from the site: https://meteo.ua/34/kiev#2024-03-19--20-00")
    for keys, values in result_list2.items():
        print(keys, " : ", values)
    return result_list2


def parse3(url3=r3):
    result_list3 = {'dates': [], 'max_temps': [], 'min_temps': []}
    soup3 = bs(url3.text, "html.parser")
    dates3 = soup3.find_all('p', class_='date')
    max_temps3 = soup3.find_all('div', class_='max')
    min_temps3 = soup3.find_all('div', class_='min')
    for date in dates3:
        result_list3['dates'].append(date.text)
    for max_temp in max_temps3:
        result_list3['max_temps'].append(max_temp.span.text)
    for min_temp in min_temps3:
        result_list3['min_temps'].append(min_temp.span.text)
    print("\nThe information was taken from the site: https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2")
    for keys, values in result_list3.items():
        print(keys, " : ", values)
    return result_list3


def parse4(url4=r4):
    result_list4 = {'dates': [], 'max_temps': [], 'min_temps': []}
    soup4 = bs(url4.text, "html.parser")
    dates4 = soup4.find_all('wo-date-day-and-month', limit=7)
    max_temps4 = soup4.find_all('wo-temperature', class_='max', limit=7)
    min_temps4 = soup4.find_all('wo-temperature', class_='min', limit=7)
    for date in dates4:
        result_list4['dates'].append(date.text)
    for max_temp in max_temps4:
        result_list4['max_temps'].append(max_temp.div.text.replace('\n', '').strip())
    for min_temp in min_temps4:
        result_list4['min_temps'].append(min_temp.div.text.replace('\n', '').strip())
    print("\nThe information was taken from the site: https://www.pogodairadar.com/stranitsa-pogodyi/kiev/4868738")
    for keys, values in result_list4.items():
        print(keys, " : ", values)
    return result_list4


df = pd.DataFrame(data=parse())
df2 = pd.DataFrame(data=parse2())
df3 = pd.DataFrame(data=parse3())
df4 = pd.DataFrame(data=parse4())
df_result = df.join(df2,  lsuffix='_2', rsuffix='_2').join(df3, lsuffix='_3', rsuffix='_3').join(df4, lsuffix='_4', rsuffix='_4')
df_result.to_csv(FILE_NAME, index=False, encoding='utf-8')
input()
