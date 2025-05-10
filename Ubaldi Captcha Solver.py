import os
import sys
import requests
from twocaptcha import TwoCaptcha
from bs4 import BeautifulSoup


def recaptcha_solver(siteurl):
    sitekey = '276ec3d6-88c8-4601-9cf8-ef59d10b6376'
    apikey = '014fed7631a883958753afbeee0aa267'
    solver = TwoCaptcha(apikey)
    try:
        result = solver.recaptcha(sitekey=sitekey, url=siteurl)
    except Exception as e:
        print(e)
        sys.exit(e)
    else:
        answer = result.get('code')
        print(answer)
        # headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #            'referer': 'https://www.99acres.com//load/verifycaptcha'}
        # payload = 'g-recaptcha-response={}'
        # session = requests.session()
        # captcha = session.post(siteurl, params=payload.format(answer), headers=headers)
        # print(captcha)  # this part is working properly, getting 200 response for that
        # time.sleep(30)


site_url = 'https://www.ubaldi.com/electromenager/lavage/lave-linge/candy/lave-linge-frontal-candy--css1410twmre-47--40412978.php'
recaptcha_solver(site_url)

# response = requests.post('https://www.ubaldi.com/electromenager/lavage/lave-linge/candy/lave-linge-frontal-candy'
#                          '--css1410twmre-47--40412978.php')
# soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)
