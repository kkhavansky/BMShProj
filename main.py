import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import sys

data = []

for page_number in range(27):
    print('page: ', page_number)

    #url = f'https://saratov.bestmebelshop.ru/catalog/shkafy-kupe/?PAGEN_1={page_number}'   #все шкафы
    url = f'https://saratov.bestmebelshop.ru/catalog/shkafy-kupe/category-bez-zerkal/?PAGEN_1={page_number}'    #шкафы без зеркал
    r = requests.get(url)
    sleep(3)
    soup = BeautifulSoup(r.text, 'lxml')

    wardrobes = soup.findAll('div', class_='prod_item col-md-4 col-sm-6')

    for every_wardrobe in wardrobes:
        wardrobe_link = 'https://saratov.bestmebelshop.ru' + every_wardrobe.find('div', class_='blockspisok_inner').find('a', class_='seredina').get('href')
        wardrobe_name = every_wardrobe.find('div', class_='blockspisok_inner').find('a', class_='nazvanie').text
        wardrobe_standart_params = every_wardrobe.find('div', class_='blockspisok_inner').find('div', class_='dop_info_cart').get('data-att')
        wardrobe_price = every_wardrobe.find('div', class_='blockspisok_inner').find('div', class_='nizbloka').find('span', class_='catalog-price').text

        params = wardrobe_standart_params.split()
        params_Wdt = int(params[0])
        params_Hgt = int(params[2])
        params_Dbt = int(params[4])

        if (1500 <= params_Wdt <= 1750) and params_Hgt >= 2200 and params_Dbt >= 500:
            data.append([wardrobe_price, wardrobe_standart_params, wardrobe_name, wardrobe_link])

#print(data)

header = ['price', 'standart_params (WxHxD)', 'name', 'link']

#data_file_csv = pd.DataFrame(data, columns=header)
data_file_xls = pd.DataFrame(data, columns=header)
try:
    #data_file_csv.to_csv('D:\Python\PyCharmProj\BMShProj\shkaf.csv', sep='\t', encoding='utf8')
    data_file_xls.to_excel('D:\Python\PyCharmProj\BMShProj\shkaf.xlsx', sheet_name="Sheet1")
except:
    print('Here is an error while saving the file:')
    e = sys.exc_info()[1]
    print(e.args[0])
else:
    print('File saved successfully')
