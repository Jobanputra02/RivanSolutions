import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common import by, keys, action_chains

soap = BeautifulSoup(requests.get('https://stfrancismedicalcenter.com/find-a-provider/').content, "lxml")

driver = webdriver.Chrome(service=Service("../../venv/chromedriver.exe"))
driver.maximize_window()
driver.get(soap.find('iframe').get_attribute_list('src')[0])
time.sleep(2)

# For loading all the datas in GUI thread.
for i in range(50):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)

# Extracting all doctor's profile link.
all_links = [i.get_attribute('href') for i in driver.find_elements(by.By.CLASS_NAME, value="btnsWrapper a")]

full_name_list = []
speciality_list = []
full_address_list = []
practice_list = []
city_list = []
state_list = []
zip_code_list = []
phone_number_list = []
fax_number_list = []

for link in all_links:
    link_soap = BeautifulSoup(requests.get(link).content, "lxml")

    try:
        full_name = link_soap.find('b').text
    except AttributeError:
        full_name = ""
    full_name_list.append(full_name)

    try:
        speciality = link_soap.select('div.speciality span')[0].text
    except IndexError or AttributeError:
        speciality = ""
    speciality_list.append(speciality)

    try:
        full_address = link_soap.select('div.locations span')[0].text
    except IndexError or AttributeError:
        full_address = ""
    full_address_list.append(full_address)

    try:
        practice = link_soap.select('div.locations h5')[0].text
    except IndexError or AttributeError:
        practice = ""
    practice_list.append(practice)

    try:
        city = link_soap.select('div.hideMobile span')[0].text.split(', ')[0]
    except IndexError or AttributeError:
        city = ""
    city_list.append(city)

    try:
        state = link_soap.select('div.hideMobile span')[0].text.split(', ')[1]
    except IndexError or AttributeError:
        state = ""
    state_list.append(state)

    try:
        zip_code = full_address.split(',')[-2].split(" ")[-1]
    except IndexError or AttributeError:
        zip_code = ""
    zip_code_list.append(zip_code)

    try:
        phone_number = link_soap.select('div.item span')[1].text
    except IndexError or AttributeError:
        phone_number = ""
    phone_number_list.append(phone_number)

    try:
        fax_number = link_soap.select('div.item span')[2].text
    except IndexError or AttributeError:
        fax_number = ""
    fax_number_list.append(fax_number)

# Integrating all links into JSON.
data = {"Full Name": full_name_list,
        "Speciality": speciality_list,
        "Full Address": full_address_list,
        "Practice": practice_list,
        "City": city_list,
        "State": state_list,
        "ZIP Code": zip_code_list,
        "Phone Number": phone_number_list,
        "Fax Number": fax_number_list}

df = pd.DataFrame(data)
df.to_csv('doctor-search.csv',)
