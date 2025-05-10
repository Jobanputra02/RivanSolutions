import requests
from bs4 import BeautifulSoup
import pandas as pd

master_json = {
    "Title": [],
    "Link": [],
}

for page in range(1, 21):
    headers = {
        'authority': 'www.capitalautoauction.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'referer': f'https://www.capitalautoauction.com/inventory?per_page=100&sort=make&sort_direction=&page={page}',
        'sec-ch-ua': '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    params = {
        'per_page': '100',
        'sort': 'make',
        'sort_direction': '',
        'page': f'{page}',
    }
    response = requests.get('https://www.capitalautoauction.com/inventory', params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_cards = soup.find_all('div', class_='catalog__card')
    for card in all_cards:
        try:
            card_title = card.select('h3.card__title')[0].text.strip().replace(' ', '').replace('\n', ' ')
        except:
            card_title = ""
        master_json['Title'].append(card_title)
        try:
            card_link = card.select('div.card__buttons a.card__button-detailes')[0].get('href')
        except:
            card_link = ""
        master_json['Link'].append(card_link)

df = pd.DataFrame(master_json)
df.to_csv("Capital Auto Auction Links.csv", index=False)
