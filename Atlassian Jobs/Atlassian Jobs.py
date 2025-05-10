"""Importing all the necessary libraries."""
import os
import time
import logging
import requests
from datetime import date
from threading import Lock
from job_meta_upload_script_v2 import JobsMeta
from unidecode import unidecode
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor

config_rdr = ConfigParser()

config_rdr.read('/root/job_scheduling/db_config.ini')
DEV_MAIL = config_rdr.get('dev_mails', 'dev_mail')
POST_AUTHOR = config_rdr.get('post_author_no', 'chaitanya')


class Atlassian:
    """Creating Atlassian class containing all the methods."""
    def __init__(self, company):
        logging.basicConfig(filename=f'{company}_logs_{date.today().strftime("%d_%m_%Y")}.log',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
        self.company = company
        self.logger_ob = logging.getLogger()
        self.threadlock = Lock()
        self.objct = JobsMeta(self.company, self.logger_ob)
        self.session = requests.Session()
        self.regex = r'\<\s\d{1,2}\s[y,Y][e,E][a,A][r,R][s,S]|\>\s\d{1,2}\s[y,Y][e,E][a,A][r,R][s,S]|\d{1,2}\-\d{1,' \
                     r'2}\s[y,Y][e,E][a,A][r,R][s,S]|\d{1,2}\s\-\s\d{1,2}\s[y,Y][e,E][a,A][r,R][s,S]|\d{1,2}\-\d{1,' \
                     r'2}\s[y,Y][r,R][s,S]|\d{1,2}\s\-\s\d{1,2}\s[y,Y][r,R][s,S]|\d{1,2}\-\d{1,2}\s[m,M][o,O][n,N][t,' \
                     r'T][h,H][s,S]|\d{1,2}\s\-\s\d{1,2}\s[m,M][o,O][n,N][t,T][h,H][s,S]|\<\s\d{1,2}\s[m,M][o,O][n,' \
                     r'N][t,T][h,H][s,S]|\>\s\d{1,2}\s[m,M][o,O][n,N][t,T][h,H][s,S]|\<\s\d{1,2}\s[y,Y][r,R][s,' \
                     r'S]|\>\s\d{1,2}\s[y,Y][r,R][s,S]|\d{1,2}\+\s[y,Y][e,E][a,A][r,R][s,S]|\d{1,2}\+\s[m,M][o,O][n,' \
                     r'N][t,T][h,H][s,S] '
        self.base_url = 'https://www.atlassian.com/.rest/postings'
        self.header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                     'like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

        try:
            response = self.session.get(self.base_url, headers=self.header)
            json_data = response.json()
            self.count = int(len(json_data['postings']))
        except Exception as resp_err:
            self.logger_ob.critical(f'Error while requesting and getting json data from {self.base_url} : {resp_err}')
            self.objct.exit_fun()

    def link_page(self):
        try:
            headers = {
                'authority': 'www.atlassian.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.atlassian.com/company/careers/all-jobs',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/109.0.0.0 Safari/537.36',
            }
            res = self.session.get(self.base_url, headers=headers)
            jobs = res.json()['postings']
            j_url = ''
            for job in jobs:
                j_url = unidecode(job['urls']['showUrl'])
                page_url = f"https://www.atlassian.com/company/careers/all-jobs"
                self.threadlock.acquire()
                self.objct.link_insertion(page_url, j_url)
                self.threadlock.release()
        except Exception as ins_err:
            self.logger_ob.error(f'Error while getting and inserting job url {j_url} from page {page_url} : {ins_err}')

    def new_scraper(self, pj_url):
        try:
            p_url = pj_url[0]
            j_url = pj_url[1]
            search_pg_no = ''
            try:
                headers = {
                    'authority': 'www.atlassian.com',
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-US,en;q=0.9',
                    'referer': 'https://www.atlassian.com/company/careers/all-jobs',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'sec-gpc': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/109.0.0.0 Safari/537.36',
                }
                resp = self.session.get(self.base_url, headers=headers)
                jobs = resp.json()['postings']
            except Exception as scr_err:
                self.logger_ob.error(f'Error while scraping data from {p_url} : {scr_err}')
            else:
                ex_stat = 'Not Existing'
                for job in jobs:
                    if unidecode(job['urls']['showUrl']) == j_url:
                        description = job['content']['description']
                        title = job['text']
                        company_name = "Atlassian"
                        location = job['categories']['location']
                        joburl = job['urls']['showUrl']
                        qualification = ""
                        skills = ""
                        experience = ""
                        imp_info = ""
                        company_website = "https://www.atlassian.com/"
                        company_tagline = "Dream big, work smart, deliver fast"
                        company_video = "NA"
                        company_twitter = "@Atlassian"
                        job_logo = True
                        localFilePath = "./logo/atlassian_logo.png"
                        if "India" in location or "india" in location:
                            try:
                                self.threadlock.acquire()
                            except Exception as th_lock_acq_err:
                                self.logger_ob.error(f'Error while acquiring thread lock : {th_lock_acq_err}')
                            else:
                                self.objct.upload_job_meta_upd(postauth=POST_AUTHOR,
                                                               postcontent=description,
                                                               posttitle=title,
                                                               companyname=company_name,
                                                               location=location,
                                                               search_page_no=search_pg_no,
                                                               job_url=joburl,
                                                               qualification=qualification,
                                                               skills=skills,
                                                               experience=experience,
                                                               imp_info=imp_info,
                                                               company_website=company_website,
                                                               company_tagline=company_tagline,
                                                               company_video=company_video,
                                                               company_twitter=company_twitter,
                                                               job_logo=job_logo,
                                                               localFilePath=localFilePath)
                                print(f'{j_url} Scraped')
                                self.objct.change_status(j_url)
                                self.threadlock.release()
                            ex_stat = 'Existing'
                            break
                if ex_stat == 'Not Existing':
                    self.objct.del_not_existing(j_url)
        except Exception as scr_err:
            self.logger_ob.error(f'Error in scraping for {j_url} : {scr_err}')

    def multi_thread_updated(self):
        """multithreading."""
        # pager = list(range(1, self.count + 1))
        # pager=list(range(1,4))
        'Add Links to company_job_st_tb table with'
        try:
            print(f'Total jobs on portal : {self.count}')
            self.link_page()
            # with ThreadPoolExecutor() as link_adder:
            #     link_adder.map(self.link_page, pager)
        except Exception as st_tb_mul_thd_err:
            self.logger_ob.critical(
                f'Error while inserting links in status table using multithreading : {st_tb_mul_thd_err}')
            print(f'Error while inserting links in status table using multithreading : {st_tb_mul_thd_err}')
            self.objct.exit_fun(DEV_MAIL)
        else:
            try:
                ns_j_links = self.objct.not_scraped_urls()
                # print(ns_j_links)
                print(f'Links remaining to be scraped : {len(ns_j_links)}')
                with ThreadPoolExecutor(max_workers=1) as executor:
                    executor.map(self.new_scraper, ns_j_links)
                self.objct.check_different('Atlassian')
                print(f'Links remaining to be scraped : {len(self.objct.delete_temp_table())}')

            except Exception as job_scp_mt_err:
                self.logger_ob.critical(
                    f'Error while inserting links in trial_job_meta using multithreading : {job_scp_mt_err}')
                self.objct.exit_fun()


if __name__ == '__main__':
    t1 = time.time()
    obj = Atlassian('Atlassian')
    # obj.objct.create_meta_table()
    obj.objct.create_sc_stat_tb()
    obj.multi_thread_updated()
    print(f'Time taken to complete scraping all {obj.count} is : {round(time.time() - t1, 2)}s')
    if os.stat(f'{obj.company}_logs_{date.today().strftime("%d_%m_%Y")}.log').st_size != 0:
        obj.objct.mail_log_file()
        # mail_log_file(obj.company, obj.logger_ob)
        print('Log file mailed')
    else:
        print('Log file is empty')
        logging.shutdown()
        os.remove(f'{obj.company}_logs_{date.today().strftime("%d_%m_%Y")}.log')
        if not os.path.exists(f'{obj.company}_logs_{date.today().strftime("%d_%m_%Y")}.log'):
            print('Log File deleted')
