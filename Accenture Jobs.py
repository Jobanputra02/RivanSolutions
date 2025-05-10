import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

df = pd.DataFrame(columns=["Job ID", "Title", "Location", "Posted Date", "Skills", "Role", "Qualification", "Job URL", "Job Description", "Country", "Experience Level"])
counter = 1

# for i in range(1, 688):
for i in range(1, 2):
    headers = {
        'authority': 'www.accenture.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.7',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryChUkBIM3EiByBXsR',
        'csrf-token': '',
        'origin': 'https://www.accenture.com',
        'referer': f'https://www.accenture.com/in-en/careers/jobsearch?jk=&sb=1&vw=0&is_rj=0&pg={i}',
        'sec-ch-ua': '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36',
    }
    data = '------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="f"\r\n\r\n' + str(counter) + '\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="s"\r\n\r\n9\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="k"\r\n\r\n\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="lang"\r\n\r\nen\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="cs"\r\n\r\nin-en\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="df"\r\n\r\n[{"metadatafieldname":"skill","items":[]},{"metadatafieldname":"location","items":[]},{"metadatafieldname":"postedDate","items":[]},{"metadatafieldname":"travelPercentage","items":[]},{"metadatafieldname":"jobTypeDescription","items":[]},{"metadatafieldname":"businessArea","items":[]},{"metadatafieldname":"specialization","items":[]},{"metadatafieldname":"workforceEntity","items":[]},{"metadatafieldname":"yearsOfExperience","items":[]}]\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="c"\r\n\r\nIndia\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="sf"\r\n\r\n1\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="syn"\r\n\r\nfalse\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="isPk"\r\n\r\nfalse\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="wordDistance"\r\n\r\n0\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="userId"\r\n\r\n\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR\r\nContent-Disposition: form-data; name="componentId"\r\n\r\ncareerjobsearchresults-6e7bb92edd\r\n------WebKitFormBoundaryChUkBIM3EiByBXsR--\r\n'
    response = requests.post(url="https://www.accenture.com/api/accenture/jobsearch/result", headers=headers, data=data)
    json = response.json()

    if json:
        json_data = response.json()["documents"]

        for job in json_data:
            dict_to_add = {"Job ID": [], "Title": [], "Location": [], "Posted Date": [], "Skills": [], "Role": [],
                           "Qualification": [], "Job URL": [], "Job Description": [], "Country": [],
                           "Experience Level": []}

            job_id = job['id']
            title = job['title']
            location = job['location'][0]
            posted_date = datetime.utcfromtimestamp(job['postedDate']/1000).strftime('%Y-%m-%d %H:%M:%S')
            skills = job['skill']
            role = job['role']

            try:
                for li in BeautifulSoup(job['jobDescription'], "lxml").select('li'):
                    if li.find('strong'):
                        if 'Qualification' in li.find('strong').text.split():
                            qualification = ':'.join(li.text.split(':')[1:])
                        else:
                            qualification = ""
            except NameError:
                qualification = ""

            job_url = job['jobDetailUrl']
            job_description = job['jobDescription']
            country = job['country']
            experience_level = f"'{job['feedExperienceLevel']}"

            dict_to_add['Job ID'].append(job_id)
            dict_to_add['Title'].append(title)
            dict_to_add['Location'].append(location)
            dict_to_add['Posted Date'].append(posted_date)
            dict_to_add['Skills'].append(skills)
            dict_to_add['Role'].append(role)
            dict_to_add['Qualification'].append(qualification)
            dict_to_add['Job URL'].append(job_url)
            dict_to_add['Job Description'].append(job_description)
            dict_to_add['Country'].append(country)
            dict_to_add['Experience Level'].append(experience_level)

            df_to_add = pd.DataFrame(dict_to_add)
            df = pd.concat([df, df_to_add], ignore_index=True)
    else:
        print("JSON Not found")

    counter += 9

df.to_csv("Accenture Jobs.csv")
