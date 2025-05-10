import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "https://www.rivan.in/careers.html"
soap = BeautifulSoup(requests.get(URL).content, 'lxml')

all_jobs = soap.find_all('section', class_='features12')
for job in all_jobs:
    job_title = job.select('div.card-box h4.card-title')[0].text.strip()
    job_requirements = ' '.join([i.text for i in job.select('div.card-box p') if i.text != ''])

    if 'Experience : ' in job_requirements:
        job_experience = job_requirements.split('Experience : ')[-1].replace('.', '')
    else:
        job_experience = ''

    job_benifits = '\n'.join([i.text.strip() for i in job.select('div.item')])
    # job_perks = [i.text.strip().replace('\n', ' ') for i in soap.find_all('section', class_="features14")]
    job_apply_link = job.select('div.card-box a')[0].text.strip()

    list_to_append = [['Click The Link To Apply For The Job'],
                      ['https://www.rivan.in/careers.html'],
                      [''],
                      [job_title],
                      ['Roles and Responsibilities'],
                      [job_requirements],
                      [''],
                      ['Experience Required'],
                      [job_experience],
                      [''],
                      ['Job Benefits'],
                      [job_benifits],
                      [''],
                      ['Job Perks'],
                      [''],
                      ['Apply Link'],
                      [job_apply_link]]

    file_name = fr'{job_title.replace("/"," - ")}.csv'
    with open(file_name, newline='', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(list_to_append)
    break
