import requests
import pandas as pd

headers = {
    'authority': 'www.atlassian.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.atlassian.com/company/careers/all-jobs?team=&location=&search=',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
                  'Safari/537.36',
}
response = requests.get('https://www.atlassian.com/.rest/postings', headers=headers)
json_data = response.json()['postings']

job_dict = {
    'ID': [],
    'Title': [],
    'Type': [],
    'Location': [],
    'URL': [],
    'Team': [],
    'Company Name': [],
    'Company Website': [],
    'Company Tagline': [],
    'Company video': [],
    'Job Logo': [],
    'Local File Path': [],
    'Description': [],
    'Qualification': [],
    'Skills': [],
    'Experience': [],
    'Important Information': [],
}

for job in json_data:
    job_id = job['id']
    title = job['text']
    job_type = job['categories']['commitment']
    job_location = job['categories']['location']
    url = job['urls']['showUrl']
    job_team = job['categories']['team']
    company_name = "Atlassian"
    company_website = "https://www.atlassian.com/"
    company_tagline = "Dream big, work smart, deliver fast"
    company_video = "NA"
    company_twitter = "@Atlassian"
    job_logo = True
    localFilePath = "./logo/atlassian_logo.png"
    description = job['content']['description']
    qualification = ""
    skills = ""
    experience = ""
    imp_info = ""

    job_dict['ID'].append(job_id)
    job_dict['Title'].append(title)
    job_dict['Type'].append(job_type)
    job_dict['Location'].append(job_location)
    job_dict['URL'].append(url)
    job_dict['Team'].append(job_team)
    job_dict['Company Name'].append(company_name)
    job_dict['Company Website'].append(company_website)
    job_dict['Company Tagline'].append(company_tagline)
    job_dict['Company video'].append(company_video)
    job_dict['Job Logo'].append(job_logo)
    job_dict['Local File Path'].append(localFilePath)
    job_dict['Description'].append(description)
    job_dict['Qualification'].append(qualification)
    job_dict['Skills'].append(skills)
    job_dict['Experience'].append(experience)
    job_dict['Important Information'].append(imp_info)

df = pd.DataFrame(job_dict).sort_values('Team')
df.to_csv('Atlassian Jobs.csv', index=False)
