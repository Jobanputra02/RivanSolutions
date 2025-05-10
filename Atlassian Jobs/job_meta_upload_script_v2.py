"""Importing all the necessary libraries."""
import os
import time
import smtplib
import hashlib
import requests
from datetime import date
from mysql import connector
from os.path import basename
from email.mime.text import MIMEText
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Get the required credentials to connect to Database
config_rdr = ConfigParser()  # object to read .ini file
config_rdr.read('db_config.ini')

DB_HOST = config_rdr.get('rivan_job_db', 'db_host')
DB_USR = config_rdr.get('rivan_job_db', 'db_usr')
DB_PWD = config_rdr.get('rivan_job_db', 'db_pwd')
DB_NAME = config_rdr.get('rivan_job_db', 'db_name')
DEV_MAIL = config_rdr.get('dev_mails', 'chaitanya')


class JobsMeta:
    """Contains methods for performing database operations"""

    def __init__(self, company, logger_obj):
        """Constructor for initial configuration for database connection"""
        self.logger_objt = logger_obj

        try:
            con_stat = internet_connection()  # wait for 5/10 min
            if not con_stat[0]:
                self.logger_objt.critical(f'Internet Connectivity Issue : {con_stat[1]}')
                self.exit_fun()
            self.con = connector.connect(host=DB_HOST,
                                         user=DB_USR,
                                         password=DB_PWD,
                                         database=DB_NAME)
            self.cur = self.con.cursor(buffered=True)
            print('Connection Created')
        except Exception as con_err:
            self.logger_objt.critical(f'Error in connection to database {DB_NAME} : {con_err}')
            if self.lost_sql_connection(con_err):
                self.logger_objt.info(f'Connection to MySql restablished')
            else:
                self.logger_objt.critical(f'Error while connecting to database {DB_NAME} : {con_err}')
                self.exit_fun()
        else:
            self.company = company
    def create_meta_table(self):
        """Create the job_meta_2 table if it does not exist"""
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()
            meta_query = f'''CREATE TABLE IF NOT EXISTS job_meta_2 
(serial INT NOT NULL AUTO_INCREMENT , md5_chksum VARCHAR(255) NOT NULL ,
postauth INT NOT NULL , postcontent TEXT NOT NULL ,
posttitle VARCHAR(200) NOT NULL , companyname VARCHAR(200) NOT NULL ,
location VARCHAR(200) NOT NULL , jobtype VARCHAR(200) NOT NULL ,
job_url VARCHAR(1000) NOT NULL , search_page_no VARCHAR(10) NOT NULL ,
qualification TEXT NOT NULL , skills TEXT NOT NULL ,
experience TEXT NOT NULL , salary VARCHAR(200) NOT NULL ,
imp_info VARCHAR(1000) NOT NULL , company_website VARCHAR(255) NOT NULL ,
company_tagline VARCHAR(200) NOT NULL , company_video VARCHAR(200) ,
company_twitter VARCHAR(200) NOT NULL , job_logo TINYINT(1) ,
localFilePath VARCHAR(100) , upld_date DATE NOT NULL , PRIMARY KEY (serial))'''
            self.cur.execute(meta_query)
            print('Job Meta 2 table created')
        except Exception as crt_job_meta_err:
            self.logger_objt.error(f'Error while creating table job_meta_2: \
{crt_job_meta_err}')
            if self.lost_sql_connection(crt_job_meta_err):
                self.logger_objt.info(f'Connection to MySql restablished')
                self.create_meta_table()
            else:
                self.logger_objt.critical(f'Error while creating table job_meta_2 : {crt_job_meta_err}')
                self.exit_fun()
    def create_sc_stat_tb(self):
        st_tb = self.company.replace(' ', '_') + '_job_sc_stat'
        '''Creating temporary table for job_url scraping status'''
        query = f'''CREATE TABLE IF NOT EXISTS {st_tb}
        (page_url VARCHAR(1000), job_url VARCHAR(1000), sc_stat VARCHAR(2))'''
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()

            self.cur.execute(query)
            print(f'{self.company}_job_sc_stat Created')
        except Exception as crt_err:
            self.logger_objt.error(f'Error while creating table \
{self.company}_job_sc_stat : {crt_err}')
            if self.lost_sql_connection(crt_err):
                self.logger_objt.info(f'Connection to MySql restablished')
                self.create_sc_stat_tb()
            else:
                self.logger_objt.critical(f'Error while creating table job_meta_2 : {crt_err}')
                self.exit_fun()
    def exit_fun(self):
        """Stops the execution of whole program in case of critical error and sends the log file to respective developer"""
        self.cur.close()
        self.con.close()
        mail_log_file(self.company, self.logger_objt)
        # raise Exception("Check log file")using raise would not stop execution as we are catching exception
        exit()
    def db_reconnection(self):
        """Reconnects to database"""
        try:
            # storing status instead of calling function in if condition as I
            # need error part and for that again calling function would add sleep for 10min more
            con_stat = internet_connection()  # wait for 5/10 min
            if not con_stat[0]:
                self.logger_objt.critical(f'Internet Connectivity Issue : {con_stat[1]}')
                self.exit_fun()
            self.con = connector.connect(host=DB_HOST,
                                         user=DB_USR,
                                         password=DB_PWD,
                                         database=DB_NAME)
            self.cur = self.con.cursor(buffered=True)
        except Exception as rec_err:
            self.logger_objt.critical(f'Error while reconnecting to {DB_NAME} database : {rec_err}')
            return False
        return True
    def lost_sql_connection(self, err_msg):
        """Tries to reconnect to database twice otherwise exit"""
        if "2013 (HY000): Lost connection to MySQL server during query" in str(
                err_msg) or "2003 (HY000): Can't connect to MySQL server" in str(err_msg):
            if not self.con.is_connected():
                if not self.db_reconnection():  # 1
                    if not self.db_reconnection():  # 2 ->try twice for recoonection to database
                        self.exit_fun()
                return True
        return False
    def re_query(self, query):
        """To run the query - (INSERT/UPDATE/DELETE) again in case of lost sql connection
        Never run for the select query as it requires some output in return
        Returns True for successful query execution"""
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    if not self.db_reconnection():
                        self.exit_fun()
            c = self.con.cursor(dictionary=True)
            c.execute(query)
        except Exception as re_qry_err:
            self.logger_objt.error(f"Error while executing query {query} : {re_qry_err}")
            if self.lost_sql_connection(re_qry_err):
                self.logger_objt.info(f'Connection to MySql restablished')
                self.re_query(query)
            else:
                self.logger_objt.critical(f'Query {query} could not be executed successfully \
due to error :{re_qry_err}')
                return False
        return True
    def sel_re_query(self, sel_query):
        """To run the select query - again in case of lost sql connection"""
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    if not self.db_reconnection():
                        self.exit_fun()
            c = self.con.cursor(dictionary=True)
            c.execute(sel_query)
            data = c.fetchall()
        except Exception as sel_re_qry_err:
            self.logger_objt.error(f"Error while executing selection query {sel_query} : {sel_re_qry_err}")
            if self.lost_sql_connection(sel_re_qry_err):
                self.logger_objt.info(f'Connection to MySql restablished')
                data = self.sel_re_query(sel_query)
                if not data[0]:
                    return [False]
                data = data[1:]
            else:
                self.logger_objt.critical(f'Query {sel_query} could not be executed successfully \
due to error :{sel_re_qry_err}')
                return [False]
        return [True, data]
    def not_scraped_urls(self):
        """Returns the list of Not Scraped(NS) job and page urls"""
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()
            s_query = f"SELECT page_url,job_url FROM {self.company}_job_sc_stat WHERE sc_stat='NS'"
            self.cur.execute(s_query)
            ns_rec = self.cur.fetchall()
            ns_rec = [list(i) for i in ns_rec]
            # [[p,j][p,j]...]
        except Exception as ns_err:
            self.logger_objt.error(f'Error while selecting \
Not Scraped URLs from table {self.company}_job_sc_stat : {ns_err}')
            if self.lost_sql_connection(ns_err):
                self.logger_objt.info(f'Connection to MySql restablished')
                ns_rec = self.not_scraped_urls()
            else:
                self.logger_objt.critical(f'Error while selecting \
Not Scraped URLs from table {self.company}_job_sc_stat : {ns_err}')
                self.exit_fun()
        return ns_rec
    def link_insertion(self, page_url, job_url):
        """Inserts page and job url in the Scraping Status Table"""
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()
            query = f"SELECT job_url FROM {self.company}_job_sc_stat WHERE job_url='{job_url}'"
            self.cur.execute(query)
            existing_job = self.cur.fetchall()
        except Exception as fth_err:
            self.logger_objt.error(f'Error while checking \
if the job url {job_url} from page {page_url} already \
exists in status table {self.company}_job_sc_stat : {fth_err}')
            if self.lost_sql_connection(fth_err):
                self.logger_objt.info(f'Connection to MySql restablished')
                self.link_insertion(page_url, job_url)
            else:
                self.logger_objt.error(f'Error while checking \
if the job url {job_url} from page {page_url} already \
exists in status table {self.company}_job_sc_stat : {fth_err}')
        else:
            query = f"INSERT INTO \
{self.company}_job_sc_stat VALUES('{page_url}','{job_url}','NS')"
            if len(existing_job) == 0:  # job_url does not exist in Scraping Status table
                try:
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun()
                    self.cur.execute(query)
                    self.con.commit()
                    # print(f'{self.company}_job_sc_stat inserted new link')
                except Exception as st_ins_err:
                    self.logger_objt.error(f'''Error while inserting
the job url {job_url} from page {page_url} in status table
{self.company}_job_sc_stat : {st_ins_err}''')
                    if self.lost_sql_connection(st_ins_err):
                        self.logger_objt.info(f'Connection to MySql restablished')
                        if not self.re_query(query):
                            self.logger_objt.error(f'''Failed to insert job url {job_url} 
                            from page {page_url} in status table
                            {self.company}_job_sc_stat''')
                    else:
                        self.logger_objt.error(f'''Error while inserting
the job url {job_url} from page {page_url} in status table
{self.company}_job_sc_stat : {st_ins_err}''')
    def change_status(self, j_url):
        """Changes the scraping status of the job url to S(Scraped) in Scraping Status Table"""
        up_qu = f"UPDATE {self.company}_job_sc_stat SET sc_stat='S' WHERE job_url='{j_url}'"
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()

            self.cur.execute(up_qu)
            self.con.commit()
        except Exception as stat_chn_err:
            self.logger_objt.error(f'Error while changing status \
for job url {j_url} in status table {self.company}_job_sc_stat \
: {stat_chn_err}')
            if self.lost_sql_connection(stat_chn_err):
                self.logger_objt.info(f'Connection to MySql restablished')
                if not self.re_query(up_qu):
                    self.logger_objt.error(f'''Failed to update status of job url {j_url} 
in status table {self.company}_job_sc_stat''')
            else:
                self.logger_objt.error(f'Error while changing status \
for job url {j_url} in status table {self.company}_job_sc_stat \
: {stat_chn_err}')
    def upload_job_meta_upd(self, postauth=16, postcontent='Work for Full Time',
                            posttitle='Developer', companyname='XYZ', location='India', jobtype='Full Time',
                            search_page_no='-1', job_url='https://www.xyz.in/apply-for-job/',
                            qualification='Graduation, Post Graduation', skills='Related to Job Title',
                            experience='0-2 years', salary='Not Disclosed',
                            imp_info='Candidate should be passionate about their work',
                            company_website='https://www.xyz.in/', company_tagline='Work Hard & Make History',
                            company_video='https://www.xyz.in/video/', company_twitter='@xyz', job_logo=False,
                            localFilePath='./logo/info.png'):
        """Uploads the passed data in job data table"""

        postcontent = remove_non_ascii(postcontent)
        posttitle = remove_non_ascii(posttitle)
        location = remove_non_ascii(location)
        jobtype = remove_non_ascii(jobtype)
        qualification = remove_non_ascii(qualification)
        skills = remove_non_ascii(skills)
        experience = remove_non_ascii(experience)
        salary = remove_non_ascii(salary)
        imp_info = remove_non_ascii(imp_info)

        md5_chksum = hashlib.md5(
            f"{postauth}, {postcontent}, {posttitle}, {companyname},{location}, {jobtype}, {search_page_no},{job_url}, "
            f"{qualification}, {skills},{experience},{salary}, {imp_info},{company_website}, {company_tagline},"
            f" {company_video}, {company_twitter}, {job_logo}, {localFilePath}".encode("utf-8")).hexdigest()

        if job_logo:
            job_logo = 1
        elif not job_logo:
            job_logo = 0
        query = f"SELECT md5_chksum FROM job_meta_2 WHERE md5_chksum='{md5_chksum}'"  # check wether the job is already present or not
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()

            self.cur.execute(query)
            existing_job = self.cur.fetchall()
        except Exception as slc_err:
            self.logger_objt.error(f'Error while selecting md5 checksum from job_meta_2 table : {slc_err}')
            if self.lost_sql_connection(slc_err):
                self.logger_objt.info(f'Connection to MySql restablished')
                self.upload_job_meta_upd(postauth, postcontent,
                                         posttitle, companyname, location, jobtype,
                                         search_page_no, job_url, qualification, skills,
                                         experience, salary,
                                         imp_info, company_website, company_tagline,
                                         company_video, company_twitter, job_logo,
                                         localFilePath)
            else:
                self.logger_objt.error(f'Error while selecting md5 checksum from job_meta_2 table : {slc_err}')
        else:  # executes only if selection query in above try ran succcessfully
            # since we need to make sure no duplicacy occurs
            if len(existing_job) > 1:  # same job record exists more than once
                if not self.con.is_connected():
                    if not self.db_reconnection():
                        self.exit_fun()
                # Deleting multiple copies of pre-existing jobs.
                query = f"""
                            DELETE FROM job_meta_2 WHERE job_url="{job_url}"
                        """
                try:
                    self.cur.execute(query)
                    self.con.commit()
                    print(f'{job_url} deleted due to duplication')
                except Exception as del_dup_err:
                    self.logger_objt.error(f'Error while deleting duplicate job {job_url} from job_meta_2 : {del_dup_err}')
                    if self.lost_sql_connection(del_dup_err):
                        self.logger_objt.info(f'Connection to MySql restablished')
                        if not self.re_query(query):
                            self.logger_objt.error(f'''Failed to delete job with job url {job_url}
                            from job_meta table''')
                            return False
                    else:
                        self.logger_objt.error(f'Error while deleting duplicate job {job_url} from job_meta_2 : {del_dup_err}')
                        return False

                query = f"""INSERT INTO job_meta_2(md5_chksum, postauth, postcontent, posttitle, companyname, location, jobtype, search_page_no, job_url, qualification, skills, experience, salary, imp_info, company_website, company_tagline, company_video, company_twitter, job_logo, localFilePath,upld_date) VALUES("{md5_chksum}",{postauth}, "{postcontent}", "{posttitle}", "{companyname}", "{location}", "{jobtype}", "{search_page_no}","{job_url}", "{qualification}", "{skills}", "{experience}", "{salary}", "{imp_info}", "{company_website}", "{company_tagline}", "{company_video}", "{company_twitter}", {job_logo}, "{localFilePath}","{str(date.today())}")"""
                try:
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun()

                    self.cur.execute(query)
                    self.con.commit()
                    print(f'{job_url} inserted updated one')
                except Exception as job_ins_err:
                    self.logger_objt.error(f'Error while inserting job {job_url} in job_meta_2 : {job_ins_err}')
                    if self.lost_sql_connection(job_ins_err):
                        self.logger_objt.info(f'Connection to MySql restablished')
                        if not self.re_query(query):
                            self.logger_objt.error(f'''Failed to insert job with job url {job_url}
                            from job_meta table''')
                    else:
                        self.logger_objt.error(f'Error while inserting job {job_url} in job_meta_2 : {job_ins_err}')
            elif len(existing_job) == 0:  # new md5 checksum so either we need to insert or update
                if not self.con.is_connected():
                    if not self.db_reconnection():
                        self.exit_fun()
                try:
                    # Checking whether the job url is already present or
                    # not as md5 checksum is changed
                    sel_qry = f"SELECT job_url FROM job_meta_2 WHERE job_url='{job_url}'"
                    self.cur.execute(sel_qry)
                    exist_job = self.cur.fetchall()
                except Exception as sel_err:
                    self.logger_objt.error(f'Error while selecting apply url {job_url} : {sel_err}')
                    if self.lost_sql_connection(sel_err):
                        self.logger_objt.info(f'Connection to MySql restablished')
                        exist_job = self.sel_re_query(query)
                        if not exist_job[0]:
                            self.logger_objt.error(f'''Failed to insert job with job url {job_url}
                            from job_meta table''')
                            return False
                        exist_job = exist_job[1:]
                    else:
                        self.logger_objt.error(f'Error while inserting job {job_url} in job_meta_2 : {sel_err}')
                        return False

                if len(exist_job) != 0:  # job_url already exists so update the data
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun()
                    up_query = f"""
                            UPDATE job_meta_2 SET md5_chksum="{md5_chksum}",
                            postauth="{postauth}",postcontent="{postcontent}",posttitle="{posttitle}",
                            companyname="{companyname}",location="{location}",jobtype="{jobtype}",
                            search_page_no="{search_page_no}", qualification="{qualification}",skills="{skills}",
                            experience="{experience}",salary="{salary}",imp_info="{imp_info}",
                            company_website="{company_website}",company_tagline="{company_tagline}",
                            company_video="{company_video}",company_twitter="{company_twitter}",
                            job_logo="{job_logo}",localFilePath="{localFilePath}",upld_date="{str(date.today())}" 
                            WHERE job_url="{job_url}"
                        """
                    try:
                        self.cur.execute(up_query)
                        self.con.commit()
                        # print(f"{job_url} updated data")
                    except Exception as up_err:
                        self.logger_objt.error(f'Error while updating in job_meta_2 for job_url {job_url} : {up_err}')
                        if self.lost_sql_connection(sel_err):
                            self.logger_objt.info(f'Connection to MySql restablished')
                            if not self.re_query(query):
                                self.logger_objt.error(f'''Failed to update job with job url {job_url}
                                from job_meta table''')
                        else:
                            self.logger_objt.error(f'Error while updating in job_meta_2 for job_url {job_url} : {up_err}')
                else:  # job_url is new so insert
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun()
                    query = f"""INSERT INTO job_meta_2(md5_chksum, postauth, postcontent, posttitle, companyname, location, jobtype, search_page_no, job_url, qualification, skills, experience, salary, imp_info, company_website, company_tagline, company_video, company_twitter, job_logo, localFilePath,upld_date) VALUES("{md5_chksum}",{postauth}, "{postcontent}", "{posttitle}", "{companyname}", "{location}", "{jobtype}", "{search_page_no}","{job_url}", "{qualification}", "{skills}", "{experience}", "{salary}", "{imp_info}", "{company_website}", "{company_tagline}", "{company_video}", "{company_twitter}", {job_logo}, "{localFilePath}","{str(date.today())}")"""
                    try:
                        self.cur.execute(query)
                        self.con.commit()
                        # print(f'{job_url} inserted new')
                    except Exception as new_ins_err:
                        self.logger_objt.error(f'Error while inserting in job_meta_2 for job_url {job_url} : {new_ins_err}')
                        if self.lost_sql_connection(new_ins_err):
                            self.logger_objt.info(f'Connection to MySql restablished')
                            if not self.re_query(query):
                                self.logger_objt.error(f'''Failed to insert job with job url {job_url}
                                from job_meta table''')
                        else:
                            self.logger_objt.error(f'Error while inserting in job_meta_2 for job_url {job_url} : {new_ins_err}')
    def del_not_existing(self, j_url):
        '''Deletes the job url from Scraping status table that are
        not existing while scraping'''
        del_query = f"DELETE FROM {self.company}_job_sc_stat WHERE job_url='{j_url}'"
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()

            self.cur.execute(del_query)
            self.con.commit()
            self.cur.close()
            self.con.close()
        except Exception as del_st_err:
            self.logger_objt.error(f'Error while deleting \
not existing link from status table for {j_url} : {del_st_err}')
            if self.lost_sql_connection(del_st_err):
                self.logger_objt.info(f'Connection to MySql restablished')
                if not self.re_query(del_query):
                    self.logger_objt.error(f'''Failed to delete job with job url {j_url}''')
            else:
                self.logger_objt.error(f'Error while deleting \
not existing link from status table for {j_url} : {del_st_err}')
    def check_different(self, companyname):
        '''Deleting jobs from job_meta_table that are also deleted
        from job site itself of same company.'''
        if not self.con.is_connected():
            if not self.db_reconnection():
                self.exit_fun()
        query = f"""
                    DELETE FROM job_meta_2
                    WHERE job_meta_2.job_url IN
                    (SELECT j_url FROM
                    (SELECT job_meta_2.job_url as j_url FROM job_meta_2
                    LEFT OUTER JOIN {self.company}_job_sc_stat
                    ON job_meta_2.job_url={self.company}_job_sc_stat.job_url
                    WHERE {self.company}_job_sc_stat.job_url IS NULL AND
                    job_meta_2.companyname='{companyname}') AS c)
                """
        try:
            self.cur.execute(query)
            self.con.commit()
        except Exception as del_err:
            self.logger_objt.error(f'Error while deleting jobs deleted from the site : {del_err}')
            if self.lost_sql_connection(del_err):
                self.logger_objt.info(f'Connection to MySql restablished')
                if not self.re_query(query):
                    self.logger_objt.error(f'''Failed to run check different function''')
            else:
                self.logger_objt.error(f'Error while deleting jobs deleted from the site : {del_err}')
    def delete_temp_table(self):
        '''Drops the scraping status table once all job links
        have S as scraping status'''
        query = f"SELECT page_url,job_url FROM {self.company}_job_sc_stat WHERE sc_stat='NS'"
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()
            self.cur.execute(query)
        except Exception as ns_err:
            self.logger_objt.error(f'Error while selecting Not Scraped URLs from table {self.company}_job_sc_stat : {ns_err}')
            if self.lost_sql_connection(ns_err):
                self.logger_objt.info(f'Connection to MySql restablished')
                self.delete_temp_table()
            else:
                self.logger_objt.critical(f'Error while selecting \
Not Scraped URLs from table {self.company}_job_sc_stat \
: {ns_err}')
                self.exit_fun()
        else:
            ns_link = []
            if len(self.cur.fetchall()) == 0:
                del_query = f"DROP TABLE IF EXISTS {self.company}_job_sc_stat"
                try:
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun()
                    self.cur.execute(del_query)
                    self.con.commit()
                except Exception as del_st_tb_err:
                    self.logger_objt.critical(f'Error while deleting status table {self.company}_job_sc_stat : {del_st_tb_err}')
                    if self.lost_sql_connection(del_st_tb_err):
                        self.logger_objt.info(f'Connection to MySql restablished')
                        if not self.re_query(del_query):
                            self.logger_objt.error(f'''Failed to delete {self.company}_job_sc_stat table''')
                            self.exit_fun()
                    else:
                        self.logger_objt.critical(f'Error while \
deleting status table {self.company}_job_sc_stat : {del_st_tb_err}')
                        self.exit_fun()
            else:
                try:
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun()
                    self.cur.execute(query)
                    ns_link = self.cur.fetchall()
                    ns_link = [list(i) for i in ns_link]
                except Exception as fth_err:
                    self.logger_objt.error(f'Error while fetching Not Scraped URLs from table {self.company}_job_sc_stat : {fth_err}')
                    if self.lost_sql_connection(fth_err):
                        self.logger_objt.info(f'Connection to MySql restablished')
                        self.delete_temp_table()
                    else:
                        self.logger_objt.critical(f'Error while selecting Not Scraped URLs from table {self.company}_job_sc_stat : {fth_err}')
                        self.exit_fun()
        return ns_link

def mail_log_file(companyname, logger_ob):
    """To mail the log file to respective developer"""
    # Close all connections to database as
    # mail will be sent only if execution is completed
    # or in case of critical error

    from_addr = '190020116012ait@gmail.com'
    password = 'jlebzmvyyafrglsa'
    # from_addr = os.environ.get('RIV_EMAIL')
    # password = os.environ.get('RIV_PWD')
    to_addr = DEV_MAIL
    subject = f'Log File for {companyname} Job Portal'
    content = f'Please see the attached Log File for {companyname} Job Portal'

    con_stat = internet_connection()  # wait for 2/10 min
    if not con_stat[0]:
        logger_ob.critical(f'Internet Connectivity Issue : {con_stat[1]}')
        exit()
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    body = MIMEText(content, 'plain')
    msg.attach(body)
    print(msg)

    filename = f'{companyname}_logs_{date.today().strftime("%d_%m_%Y")}.log'

    try:
        with open(filename, 'r', encoding="utf-8") as l_f:
            part = MIMEApplication(l_f.read(), Name=basename(filename))
            part['Content-Disposition'] = f'attachment; filename="{basename(filename)}"'
        msg.attach(part)
        l_f.close()
    except Exception as log_open_err:
        print(f'Error while reading log file {filename}: {log_open_err}')
        logger_ob.error(f'Error while reading log file {filename}: {log_open_err}')
    else:
        try:
            con_stat = internet_connection()  # wait for 2/10 min
            if not con_stat[0]:
                logger_ob.critical(f'Internet Connectivity Issue : {con_stat[1]}')
                exit()
            server = smtplib.SMTP('smtp.dreamhost.com', 587)
            server.login(from_addr, password)
            server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])
        except Exception as em_log_err:
            print(f'Error while logging in to server and sending mail : {em_log_err}')
            logger_ob.error(f'Error while logging in and sending mail : {em_log_err}')
        else:
            server.quit()
def internet_connection():
    '''Check for internet connection and waits for
    minimum 2min and 10min max in case of connectivity issue'''
    trial = 0
    int_cnct_err = ''
    url = "https://www.google.com"
    time_out = 10
    while trial != 5:  # checks connection for maximum 5 times
        try:
            trial_req = requests.get(url, timeout=time_out)
            return [True]
        except (requests.ConnectionError, requests.Timeout) as int_con_err:
            time.sleep(120)  # sleep for 2min and check again
            trial += 1
            int_cnct_err = int_con_err
    return [False, int_cnct_err]
def remove_non_ascii(string):
    """Used to remove all non ascii characters that are not accepeted while inserting in sql"""
    non_ascii_str = ''.join(i for i in string if ord(i) < 128)
    return non_ascii_str.replace('"', "'")
