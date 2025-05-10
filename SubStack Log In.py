import json
import requests
from bs4 import BeautifulSoup

URL = 'https://substack.com/api/v1/login'
cookies = {
    'ab_testing_id': '%22fcbd74f7-31ba-4220-a520-2df6d52a9de1%22',
    'ajs_anonymous_id': '%220660357df30240b2a2dfa45b64fe1deb%22',
    'visit_id': '%7B%22id%22%3A%2222eb6592-8495-4902-aed4-4cbb1f618dcb%22%2C%22timestamp%22%3A%222023-02-03T09%3A32%3A09.823Z%22%2C%22utm_source%22%3A%22user-menu%22%7D',
    '__cf_bm': 'jHOcL5yxwxFrxCclhuZWXJVIkyZnC0B4KgCjD.IYAyc-1675417558-0-AZzdwgRu23Gs9oV+x1FgbK0WhRF7XSdepiaFvgv/j8rk0fhQMPEWFBfSW6OFbvBTpj078rCN5qhO9BI4lepPYYE=',
    'substack.lli': '0',
    'AWSALBTG': 'lTCI23nhkOp734iHBPq5tK2dcbJCXpx5H74ckE7idpvFhsxp/VAfPsy25IS4KeoY/F8McEQgRXWIRsG3sY9pH0sPVsQkXM7jz/Iw57Rk1NWL3qItfqi+xSNUJTMGZcQe9NViMbxQNkxgOcXPZSEYdEZYNem6I5ypoVQN95xTgsZc',
    'AWSALBTGCORS': 'lTCI23nhkOp734iHBPq5tK2dcbJCXpx5H74ckE7idpvFhsxp/VAfPsy25IS4KeoY/F8McEQgRXWIRsG3sY9pH0sPVsQkXM7jz/Iw57Rk1NWL3qItfqi+xSNUJTMGZcQe9NViMbxQNkxgOcXPZSEYdEZYNem6I5ypoVQN95xTgsZc',
    'substack.sid': 's%3AQeN9eMgs9GVuRIULMI7MWRdS_gce2fZF.KBjVgY50jMeilRv779Vd9LqrivSK8iSvn%2FBYtpBMSB0',
}
headers = {
    'authority': 'substack.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.8',
    'content-type': 'application/json',
    # 'cookie': 'ab_testing_id=%22fcbd74f7-31ba-4220-a520-2df6d52a9de1%22; ajs_anonymous_id=%220660357df30240b2a2dfa45b64fe1deb%22; visit_id=%7B%22id%22%3A%2222eb6592-8495-4902-aed4-4cbb1f618dcb%22%2C%22timestamp%22%3A%222023-02-03T09%3A32%3A09.823Z%22%2C%22utm_source%22%3A%22user-menu%22%7D; __cf_bm=jHOcL5yxwxFrxCclhuZWXJVIkyZnC0B4KgCjD.IYAyc-1675417558-0-AZzdwgRu23Gs9oV+x1FgbK0WhRF7XSdepiaFvgv/j8rk0fhQMPEWFBfSW6OFbvBTpj078rCN5qhO9BI4lepPYYE=; substack.lli=0; AWSALBTG=lTCI23nhkOp734iHBPq5tK2dcbJCXpx5H74ckE7idpvFhsxp/VAfPsy25IS4KeoY/F8McEQgRXWIRsG3sY9pH0sPVsQkXM7jz/Iw57Rk1NWL3qItfqi+xSNUJTMGZcQe9NViMbxQNkxgOcXPZSEYdEZYNem6I5ypoVQN95xTgsZc; AWSALBTGCORS=lTCI23nhkOp734iHBPq5tK2dcbJCXpx5H74ckE7idpvFhsxp/VAfPsy25IS4KeoY/F8McEQgRXWIRsG3sY9pH0sPVsQkXM7jz/Iw57Rk1NWL3qItfqi+xSNUJTMGZcQe9NViMbxQNkxgOcXPZSEYdEZYNem6I5ypoVQN95xTgsZc; substack.sid=s%3AQeN9eMgs9GVuRIULMI7MWRdS_gce2fZF.KBjVgY50jMeilRv779Vd9LqrivSK8iSvn%2FBYtpBMSB0',
    'origin': 'https://substack.com',
    'referer': 'https://substack.com/sign-in?redirect=%2F',
    'sec-ch-ua': '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
data = '{"redirect":"/","for_pub":"","email":"hidden","password":"hidden","captcha_response":null}'

with requests.Session() as session:
    response = session.post(url=URL, cookies=cookies, headers=headers)
    page = session.get(URL)
    soap = BeautifulSoup(page.content, 'lxml')

json_data = json.loads(soap.select('script')[2].text.split(' = ')[1])
user_name = json_data['user']['name']
print(user_name)

