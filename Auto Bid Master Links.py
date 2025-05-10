import requests
import pandas as pd


def get_data(page):
    headers = {
        'authority': 'www.autobidmaster.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.8',
        'referer': 'https://www.autobidmaster.com/en/search/',
        'sec-ch-ua': '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    params = {
        'fixedCriteria': '{"pt":"70.7932,22.2916"}',
        'size': '100',
        'page': f'{page}',
        'sort': 'location_distance',
        'order': 'asc',
    }
    response = requests.get(
        'https://www.autobidmaster.com/en/data/v2/inventory/search',
        params=params,
        headers=headers,
    )
    lots = response.json()['lots']
    for lot in lots:
        try:
            description = lot['description']
        except:
            description = ""
        json_data['Title'].append(description)

        try:
            link = f"https://www.autobidmaster.com/en/search/lot/{lot['id']}/{lot['slug']}"
        except:
            link = ""
        json_data['Link'].append(link)


json_data = {"Title": [], "Link": []}
total_pages = requests.get('https://www.autobidmaster.com/en/data/v2/inventory/search', params={
    'fixedCriteria': '{"pt":"70.7932,22.2916"}',
    'size': '100',
    'page': '1',
    'sort': 'location_distance',
    'order': 'asc',
}, headers={
    'authority': 'www.autobidmaster.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.8',
    'referer': 'https://www.autobidmaster.com/en/search/',
    'sec-ch-ua': '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}).json()['query']['maxNumberOfPages']

for page_no in range(1, total_pages+1):
    get_data(page=page_no)


df = pd.DataFrame(json_data)
df.to_csv("Auto Bid Master.csv", index=False)
