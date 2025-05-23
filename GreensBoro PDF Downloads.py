import re
import datetime
import requests
import urllib.parse
from bs4 import BeautifulSoup


def download_pdf(case_id):
    pdf_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'ASP.NET_SessionId=ciwj1hkloekjki5vf2li1z4a',
        'Referer': 'http://p2c.greensboro-nc.gov/Summary.aspx',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    pdf_params = {'id': case_id}
    pdf_response = requests.get('http://p2c.greensboro-nc.gov/viewreport.aspx', headers=pdf_headers, params=pdf_params, verify=False)
    with open(f'{case_id}.pdf', 'wb') as pdf_data:
        pdf_data.write(pdf_response.content)


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'ASP.NET_SessionId=2g2bswkgsekjwxtt5i3wxzkf',
    'Origin': 'http://p2c.greensboro-nc.gov',
    'Referer': 'http://p2c.greensboro-nc.gov/Summary.aspx',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}
date_from = datetime.date(year=2023, month=3, day=21)
date_to = datetime.date(year=2023, month=3, day=24)

date_from_str = urllib.parse.quote(date_from.strftime('%m/%d/%Y'), safe='')
date_to_str = urllib.parse.quote(date_to.strftime('%m/%d/%Y'), safe='')
all_case_ids = []

page = 1
session = requests.session()
run_loop = True
while run_loop:
    if page == 1:
        event_target = 'cmdSubmit2'
        event_argument = ''
    else:
        event_target = 'gvSummary'
        event_argument = f'Page%24{page}'
    data = '__EVENTTARGET=MasterPage%24mainContent%24' + event_target + '&__EVENTARGUMENT=' + event_argument + '&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwULLTEyNzkxNTQzMDcPFgIeCHN0ck9yZGVyBQRkYXRlFgJmD2QWBmYPZBYCAgUPZBYEZg8WAh4EVGV4dAVFPHNjcmlwdCBzcmM9ImpzL2pxdWVyeS0xLjguMy5taW4uanMiIHR5cGU9InRleHQvamF2YXNjcmlwdCI%2BPC9zY3JpcHQ%2BZAIBDxYCHwEF%2FwE8c2NyaXB0IHNyYz0ianF1aS8xLjExLjQvanF1ZXJ5LXVpLTEuMTEuNC5jdXN0b20ubWluLmpzIiB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiPjwvc2NyaXB0PjxsaW5rIGhyZWY9ImpxdWkvMS4xMS40L2N1cGVydGluby9qcXVlcnktdWkuY3NzIiByZWw9IlN0eWxlc2hlZXQiIGNsYXNzPSJ1aS10aGVtZSIgLz48bGluayBocmVmPSJqcXVpLzEuMTEuNC9jdXBlcnRpbm8vdGhlbWUuY3NzIiByZWw9IlN0eWxlc2hlZXQiIGNsYXNzPSJ1aS10aGVtZSIgLz5kAgEPZBYEAgMPFgIeBWFsaWduBQZjZW50ZXIWBgIBDxYCHgNzcmMFF34vaW1hZ2VzL0FnZW5jeU5hbWUuZ2lmZAIDDxYCHghkaXNhYmxlZGQWAmYPZBYEZg9kFgICAQ8PFgIfAQU8ICA8YSBjbGFzcz0iTWVudVRleHQgcDJjLW5vd3JhcCIgaHJlZj0iLi9tYWluLmFzcHgiPkhPTUU8L2E%2BZGQCAQ9kFgICAQ9kFgJmDxAPFgYeDURhdGFUZXh0RmllbGQFBHRleHQeDkRhdGFWYWx1ZUZpZWxkBQRsaW5rHgtfIURhdGFCb3VuZGdkEBULEC0gUXVpY2sgTGlua3MgLSAESG9tZQxFdmVudCBTZWFyY2gPUmVwb3J0IEluY2lkZW50D01pc3NpbmcgUGVyc29ucwdBcnJlc3RzDkRhaWx5IEJ1bGxldGluDUNyYXNoIFJlcG9ydHMKQ29udGFjdCBVcwNGQVERQmlrZSBSZWdpc3RyYXRpb24VCwN%2BLzALfi9tYWluLmFzcHgOfi9zdW1tYXJ5LmFzcHgofi9yZXBvcnRpbmNpZGVudC9pbmNpZGVudGVudHJ5aW50cm8uYXNweA5%2BL21pc3NpbmcuYXNweA5%2BL2FycmVzdHMuYXNweBR%2BL2RhaWx5YnVsbGV0aW4uYXNweBV%2BL2FjY2lkZW50ZGV0YWlsLmFzcHgOfi9jb250YWN0LmFzcHgKfi9mYXEuYXNweBd%2BL2Jpa2VyZWdpc3RyYXRpb24uYXNweBQrAwtnZ2dnZ2dnZ2dnZxYBZmQCBw9kFgJmD2QWAgIDDw8WAh8BBSpUaGVyZSBhcmUgY3VycmVudGx5IG5vIGl0ZW1zIGluIHlvdXIgY2FydC5kZAIHD2QWLgIJDxBkZBYBZmQCCg8QZGQWAWZkAhIPD2QWAh4Fc3R5bGUFGVRFWFQtVFJBTlNGT1JNOnVwcGVyY2FzZTtkAhQPEA8WBh8FBQlkZXNjcmlwdG4fBgUJY29kZV9hZ2N5HwdnZBAVIAAPQUxBTUFOQ0UgQ09VTlRZCEFSQ0hEQUxFDUJST1dOUyBTVU1NSVQKQlVSTElOR1RPTgZDTElNQVgGQ09MRkFYD0RBVklEU09OIENPVU5UWQRFREVOBEVMT04ORk9SU1lUSCBDT1VOVFkLR0lCU09OVklMTEUKR1JFRU5TQk9STw9HVUlMRk9SRCBDT1VOVFkKSElHSCBQT0lOVAlKQU1FU1RPV04GSlVMSUFODEtFUk5FUlNWSUxMRQdMSUJFUlRZDE1DTEVBTlNWSUxMRQlPQUsgUklER0UPUExFQVNBTlQgR0FSREVOCVJBTkRMRU1BTg9SQU5ET0xQSCBDT1VOVFkKUkVJRFNWSUxMRRFST0NLSU5HSEFNIENPVU5UWQdTRURBTElBClNUT0tFU0RBTEULU1VNTUVSRklFTEQLVEhPTUFTVklMTEUMVU5JREVOVElGSUVECFdISVRTRVRUFSAABEFMQU0BQQFCA0JVUgNDTEkDQ09MBERBVkkERURFTgFFBEZPUlMCR0kBRwRHVUlMAUgBSgJKVQFLAUwBTQNPQUsBUANSQU4EUkFORANSRUkEUk9DSwJTRQJTVAJTVQFUAVgBVxQrAyBnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZxYBZmQCFg8PZBYCHghvbmNoYW5nZQUuaWYoVmFsaWRhdGVJbnRlZ2VyKHRoaXMpPT1mYWxzZSkgcmV0dXJuIGZhbHNlO2QCGA8QDxYGHwUFCWNvZGVfdGV4dB8GBQpjb2RlX3ZhbHVlHwdnZBAVBwAJQ0lUWSBXSURFCkRJVklTSU9OIDEKRElWSVNJT04gMgpESVZJU0lPTiAzCkRJVklTSU9OIDQESFBQRBUHAARDSVRZBEdQRDEER1BEMgRHUEQzBEdQRDQESFBQRBQrAwdnZ2dnZ2dnFgFmZAIbDxYCHgdWaXNpYmxlaGQCHA8WAh8KaBYCAgEPEA8WAh4HQ2hlY2tlZGhkZGRkAiMPD2QWAh8JBS5pZihWYWxpZGF0ZUludGVnZXIodGhpcyk9PWZhbHNlKSByZXR1cm4gZmFsc2U7ZAIkDxBkZBYBZmQCJQ8QZGQWAQIEZAImDw8WAh8KZ2RkAicPDxYCHwpnZGQCLA8PZBYCHwgFGVRFWFQtVFJBTlNGT1JNOnVwcGVyY2FzZTtkAi4PEA8WBh8FBQlkZXNjcmlwdG4fBgUJY29kZV9hZ2N5HwdnZBAVIAAPQUxBTUFOQ0UgQ09VTlRZCEFSQ0hEQUxFDUJST1dOUyBTVU1NSVQKQlVSTElOR1RPTgZDTElNQVgGQ09MRkFYD0RBVklEU09OIENPVU5UWQRFREVOBEVMT04ORk9SU1lUSCBDT1VOVFkLR0lCU09OVklMTEUKR1JFRU5TQk9STw9HVUlMRk9SRCBDT1VOVFkKSElHSCBQT0lOVAlKQU1FU1RPV04GSlVMSUFODEtFUk5FUlNWSUxMRQdMSUJFUlRZDE1DTEVBTlNWSUxMRQlPQUsgUklER0UPUExFQVNBTlQgR0FSREVOCVJBTkRMRU1BTg9SQU5ET0xQSCBDT1VOVFkKUkVJRFNWSUxMRRFST0NLSU5HSEFNIENPVU5UWQdTRURBTElBClNUT0tFU0RBTEULU1VNTUVSRklFTEQLVEhPTUFTVklMTEUMVU5JREVOVElGSUVECFdISVRTRVRUFSAABEFMQU0BQQFCA0JVUgNDTEkDQ09MBERBVkkERURFTgFFBEZPUlMCR0kBRwRHVUlMAUgBSgJKVQFLAUwBTQNPQUsBUANSQU4EUkFORANSRUkEUk9DSwJTRQJTVAJTVQFUAVgBVxQrAyBnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZxYBZmQCLw8PFgIfCmhkZAIxDxAPFgIfCmhkZBYAZAIzDw9kFgIeB29uY2xpY2sFRV9XYWl0Q29udHJvbE1lc3NhZ2VJRC5pbm5lckhUTUw9J1JlcXVlc3QgaW4gcHJvY2VzcywgcGxlYXNlIHdhaXQuLi4nO2QCNg8PFgIfCmhkZAI4DzwrABEDAA8WBh8HZx4LXyFJdGVtQ291bnQCKx8KZ2QBEBYAFgAWAAwUKwAAFgJmD2QWFAIBD2QWDGYPZBYEZg8PFgQeCEltYWdlVXJsBRZpbWFnZXMvUGluSW5jaWRlbnQucG5nHg1BbHRlcm5hdGVUZXh0ZWRkAgEPDxYCHwpoZGQCAQ8PFgIfAQUQMDMvMjEvMjAyMyAwMTo1OGRkAgIPDxYCHwEFCEluY2lkZW50ZGQCAw9kFgICAQ8WAh8NAgIWBGYPZBYCZg8VAgZDYXNlICMLMjAyMzAzMjEwNzNkAgIPZBYCZg8VAg9QcmltYXJ5IE9mZmVuc2UoQlVSR0xBUlkgLSBGT1JDSUJMRSBFTlRSWSAtIE5PTlJFU0lERU5DRWQCBA8PFgIfAQUaMjQwMyAgICAgICAgTEFLRSBCUkFORFQgUExkZAIFD2QWAgIBDw8WBB8BBW88ZGl2IHN0eWxlPSJ2YWxpZ246bWlkZGxlOyI%2BPGltZyBzcmM9ImltYWdlcy9yZXBvcnRfbWluaS5naWYiIHN0eWxlPSJib3JkZXI6bm9uZTsgbWFyZ2luOjA7IHBhZGRpbmc6MDsiLz48L2Rpdj4eD0NvbW1hbmRBcmd1bWVudAUSSW5jaWRlbnQ8LT4yMjc0NDA3ZGQCAg9kFgxmD2QWBGYPDxYEHw4FFmltYWdlcy9QaW5JbmNpZGVudC5wbmcfD2VkZAIBDw8WAh8KaGRkAgEPDxYCHwEFEDAzLzIxLzIwMjMgMDM6NTdkZAICDw8WAh8BBQhJbmNpZGVudGRkAgMPZBYCAgEPFgIfDQICFgRmD2QWAmYPFQIGQ2FzZSAjCzIwMjMwMzIxMDMzZAICD2QWAmYPFQIPUHJpbWFyeSBPZmZlbnNlKEJVUkdMQVJZIC0gRk9SQ0lCTEUgRU5UUlkgLSBOT05SRVNJREVOQ0VkAgQPDxYCHwEFGDExMyAgICAgICAgIFRBTEwgT0FLUyBEUmRkAgUPZBYCAgEPDxYEHwEFbzxkaXYgc3R5bGU9InZhbGlnbjptaWRkbGU7Ij48aW1nIHNyYz0iaW1hZ2VzL3JlcG9ydF9taW5pLmdpZiIgc3R5bGU9ImJvcmRlcjpub25lOyBtYXJnaW46MDsgcGFkZGluZzowOyIvPjwvZGl2Ph8QBRJJbmNpZGVudDwtPjIyNzQzMzdkZAIDD2QWDGYPZBYEZg8PFgQfDgUWaW1hZ2VzL1BpbkluY2lkZW50LnBuZx8PZWRkAgEPDxYCHwpoZGQCAQ8PFgIfAQUQMDMvMjEvMjAyMyAwNTowMGRkAgIPDxYCHwEFCEluY2lkZW50ZGQCAw9kFgICAQ8WAh8NAgIWBGYPZBYCZg8VAgZDYXNlICMLMjAyMzAzMjEwNTBkAgIPZBYCZg8VAg9QcmltYXJ5IE9mZmVuc2UTTEFSQ0VOWSAtIEFMTCBPVEhFUmQCBA8PFgIfAQUUMTkwMCAgICAgICAgQU1CRVIgTE5kZAIFD2QWAgIBDw8WBB8BBW88ZGl2IHN0eWxlPSJ2YWxpZ246bWlkZGxlOyI%2BPGltZyBzcmM9ImltYWdlcy9yZXBvcnRfbWluaS5naWYiIHN0eWxlPSJib3JkZXI6bm9uZTsgbWFyZ2luOjA7IHBhZGRpbmc6MDsiLz48L2Rpdj4fEAUSSW5jaWRlbnQ8LT4yMjc0MzU4ZGQCBA9kFgxmD2QWBGYPDxYEHw4FFmltYWdlcy9QaW5JbmNpZGVudC5wbmcfD2VkZAIBDw8WAh8KaGRkAgEPDxYCHwEFEDAzLzIxLzIwMjMgMDg6MzBkZAICDw8WAh8BBQhJbmNpZGVudGRkAgMPZBYCAgEPFgIfDQICFgRmD2QWAmYPFQIGQ2FzZSAjCzIwMjMwMzIyMDM5ZAICD2QWAmYPFQIPUHJpbWFyeSBPZmZlbnNlFVRSQUZGSUMgLSBISVQgQU5EIFJVTmQCBA8PFgIfAQUXMjIwICAgICAgICAgTiBHUkVFTkUgU1RkZAIFD2QWAgIBDw8WBB8BBW88ZGl2IHN0eWxlPSJ2YWxpZ246bWlkZGxlOyI%2BPGltZyBzcmM9ImltYWdlcy9yZXBvcnRfbWluaS5naWYiIHN0eWxlPSJib3JkZXI6bm9uZTsgbWFyZ2luOjA7IHBhZGRpbmc6MDsiLz48L2Rpdj4fEAUSSW5jaWRlbnQ8LT4yMjc0NjAwZGQCBQ9kFgxmD2QWBGYPDxYEHw4FFmltYWdlcy9QaW5JbmNpZGVudC5wbmcfD2VkZAIBDw8WAh8KaGRkAgEPDxYCHwEFEDAzLzIxLzIwMjMgMDk6NDNkZAICDw8WAh8BBQhJbmNpZGVudGRkAgMPZBYCAgEPFgIfDQICFgRmD2QWAmYPFQIGQ2FzZSAjCzIwMjMwMzIxMDgzZAICD2QWAmYPFQIPUHJpbWFyeSBPZmZlbnNlFUxBUkNFTlkgLSBTSE9QTElGVElOR2QCBA8PFgIfAQUbMjkxMiAgICAgICAgUyBFTE0tRVVHRU5FIFNUZGQCBQ9kFgICAQ8PFgQfAQVvPGRpdiBzdHlsZT0idmFsaWduOm1pZGRsZTsiPjxpbWcgc3JjPSJpbWFnZXMvcmVwb3J0X21pbmkuZ2lmIiBzdHlsZT0iYm9yZGVyOm5vbmU7IG1hcmdpbjowOyBwYWRkaW5nOjA7Ii8%2BPC9kaXY%2BHxAFEkluY2lkZW50PC0%2BMjI3NDM5OGRkAgYPZBYMZg9kFgRmDw8WBB8OBRZpbWFnZXMvUGluSW5jaWRlbnQucG5nHw9lZGQCAQ8PFgIfCmhkZAIBDw8WAh8BBRAwMy8yMS8yMDIzIDEwOjAwZGQCAg8PFgIfAQUISW5jaWRlbnRkZAIDD2QWAgIBDxYCHw0CAhYEZg9kFgJmDxUCBkNhc2UgIwsyMDIzMDMyMTA3NGQCAg9kFgJmDxUCD1ByaW1hcnkgT2ZmZW5zZRVUUkFGRklDIC0gSElUIEFORCBSVU5kAgQPDxYCHwEFFTc0NCAgICAgICAgIEZVTFRPTiBTVGRkAgUPZBYCAgEPDxYEHwEFbzxkaXYgc3R5bGU9InZhbGlnbjptaWRkbGU7Ij48aW1nIHNyYz0iaW1hZ2VzL3JlcG9ydF9taW5pLmdpZiIgc3R5bGU9ImJvcmRlcjpub25lOyBtYXJnaW46MDsgcGFkZGluZzowOyIvPjwvZGl2Ph8QBRJJbmNpZGVudDwtPjIyNzQzODNkZAIHD2QWDGYPZBYEZg8PFgQfDgUWaW1hZ2VzL1BpbkluY2lkZW50LnBuZx8PZWRkAgEPDxYCHwpoZGQCAQ8PFgIfAQUQMDMvMjEvMjAyMyAxMDowMGRkAgIPDxYCHwEFCEluY2lkZW50ZGQCAw9kFgICAQ8WAh8NAgIWBGYPZBYCZg8VAgZDYXNlICMLMjAyMzAzMjEyMzNkAgIPZBYCZg8VAg9QcmltYXJ5IE9mZmVuc2UQVkFOREFMSVNNIC0gQVVUT2QCBA8PFgIfAQUYMzAwNyAgICAgICAgRVhFQ1VUSVZFIERSZGQCBQ9kFgICAQ8PFgQfAQVvPGRpdiBzdHlsZT0idmFsaWduOm1pZGRsZTsiPjxpbWcgc3JjPSJpbWFnZXMvcmVwb3J0X21pbmkuZ2lmIiBzdHlsZT0iYm9yZGVyOm5vbmU7IG1hcmdpbjowOyBwYWRkaW5nOjA7Ii8%2BPC9kaXY%2BHxAFEkluY2lkZW50PC0%2BMjI3NDUzN2RkAggPZBYMZg9kFgRmDw8WBB8OBRZpbWFnZXMvUGluSW5jaWRlbnQucG5nHw9lZGQCAQ8PFgIfCmhkZAIBDw8WAh8BBRAwMy8yMS8yMDIzIDEwOjQwZGQCAg8PFgIfAQUISW5jaWRlbnRkZAIDD2QWAgIBDxYCHw0CAhYEZg9kFgJmDxUCBkNhc2UgIwsyMDIzMDMyMTA3OGQCAg9kFgJmDxUCD1ByaW1hcnkgT2ZmZW5zZRVMQVJDRU5ZIC0gU0hPUExJRlRJTkdkAgQPDxYCHwEFGjMxMDkgICAgICAgIFlBTkNFWVZJTExFIFNUZGQCBQ9kFgICAQ8PFgQfAQVvPGRpdiBzdHlsZT0idmFsaWduOm1pZGRsZTsiPjxpbWcgc3JjPSJpbWFnZXMvcmVwb3J0X21pbmkuZ2lmIiBzdHlsZT0iYm9yZGVyOm5vbmU7IG1hcmdpbjowOyBwYWRkaW5nOjA7Ii8%2BPC9kaXY%2BHxAFEkluY2lkZW50PC0%2BMjI3NDQwMGRkAgkPZBYMZg9kFgRmDw8WBB8OBRZpbWFnZXMvUGluSW5jaWRlbnQucG5nHw9lZGQCAQ8PFgIfCmhkZAIBDw8WAh8BBRAwMy8yMS8yMDIzIDEzOjQ1ZGQCAg8PFgIfAQUISW5jaWRlbnRkZAIDD2QWAgIBDxYCHw0CAhYEZg9kFgJmDxUCBkNhc2UgIwsyMDIzMDMyMTE5OWQCAg9kFgJmDxUCD1ByaW1hcnkgT2ZmZW5zZSVCVVJHTEFSWSAtIEZPUkNJQkxFIEVOVFJZIC0gUkVTSURFTkNFZAIEDw8WAh8BBRk1ODAwICAgICAgICBXIEZSSUVORExZIEFWZGQCBQ9kFgICAQ8PFgQfAQVvPGRpdiBzdHlsZT0idmFsaWduOm1pZGRsZTsiPjxpbWcgc3JjPSJpbWFnZXMvcmVwb3J0X21pbmkuZ2lmIiBzdHlsZT0iYm9yZGVyOm5vbmU7IG1hcmdpbjowOyBwYWRkaW5nOjA7Ii8%2BPC9kaXY%2BHxAFEkluY2lkZW50PC0%2BMjI3NDQ5OGRkAgoPDxYCHwpoZGQCOQ8PFgQfAQUSUGFnZSA8Yj4xPC9iPiBvZiA1HwpnZGQCOg8PFgQfAQUTNDMgcmVjb3JkcyByZXR1cm5lZB8KZ2RkAjsPFgIfCmcWAgIBDw8WAh8KaGRkAgIPFgIfAWVkGAIFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYHBRxNYXN0ZXJQYWdlJG1haW5Db250ZW50JGNoa1RBBRxNYXN0ZXJQYWdlJG1haW5Db250ZW50JGNoa0FSBRxNYXN0ZXJQYWdlJG1haW5Db250ZW50JGNoa0xXBRxNYXN0ZXJQYWdlJG1haW5Db250ZW50JGNoa09SBR1NYXN0ZXJQYWdlJG1haW5Db250ZW50JGNoa0FSMgUdTWFzdGVyUGFnZSRtYWluQ29udGVudCRjaGtMVzIFHU1hc3RlclBhZ2UkbWFpbkNvbnRlbnQkY2hrT1IyBSBNYXN0ZXJQYWdlJG1haW5Db250ZW50JGd2U3VtbWFyeQ88KwAMAQgCBWQX9jNBUAQVLAQ4735fGwng%2BN8DwCNDQ%2Fo6IoJjUnEbug%3D%3D&__VIEWSTATEGENERATOR=BCFEF455' \
           '&__EVENTVALIDATION=%2FwEdAGWmj3m%2FanLNuld%2Fd7xOlDjwcFUbOU3rxKzeurvlsKRfibiN4h7lxJgVqn7o6%2F376c8q72HzkCuZc77Iow12nsfdfJFrpYCGhwS8NapPfMAnJLodHuoFHsnbwwr41Nmw2R%2F4YnBNSzwIz%2FccQn2Z0oY8SaAn1U7jhdMTKWin8Ab9bfHIBiJiv0sPtJ3O895G1Ysu8VvaiNxo4J4a03FnhaHVody6FifT283s0oDe3ZJ0depBhrp6boqD0hjyRyk7ndFqxH3yN1YnJrqd%2FjCEVKDqde1fiaQN9Evfcjhb2N9qCNfmdHjViWrJAJLVyo%2BmEisHlWEx2s06MhzAKOb2%2BCX%2BNqrkIPE6qOl1sBUYZpX2Nj7SIBx1M76oMLXok7asezJJnIYE8wRdLLM1pfIAJ%2FZJdPh6r98vFts1Fd7Ye2SIh3is4xOAhTQmdCCYZKKoOJORDRghN3CxRlUq0Nxv0fwLb7USt2CvEsNTKOt0aADNxhJ1VYOymrITkRbqfm9EOtpAOtzrp4GBaWHFepWqeHngr3P5ttP3qDi6CWvpZsrDI1yOm1vPNFZKyln2%2Bo3PAsQ%2B%2BPEf%2FAsP2nB84vyw1sVe7jAKDyNnkXiR5oAzdB5h2eRI95jUpEEv8kzIu2jqn9FIgkrP59j80bAzd9AXA0B%2FWCwtTq%2BJCiYcO6up6yiIbK85Yncy7XQHcpC6Ddqy44XfkKmDvAxaAMrNcAUG%2Fv98felp5Y9S2kP7iv3aOqg6X6oxtN7rFZE6N%2BkHQQfx%2FgTzLwK4ywATI6rql3uA3Tk5OTmLrSdxcZY8ka%2BXok3jttyHghGrPnb262mkU94Hcnp5T2fzURgwwjn3VY63bx0BzJFW2%2Ba1YPw8zQmuSLHddCHTtX4GubthpC%2BGgKUHuY4g9kYV%2FcZNu%2FsXluzH4lf8JeCDgsFwCLsdixIE55iGECS3FAV9zoOrJwqxT%2Fxw%2FC4etx0Lyi%2FJv7XkRbqVDfNodYL0DJzBWvHwq2karL%2F4NIJLHSNruLgkwNXHwmMcHPZVCU2n56nMgzrqSmZ8mV8PoaI%2Bef%2F4DdK9eiNUx%2BuiXSMwKaRXjkEoIgDWmc00AxOTAJ9p0vBwYFWJ%2FFrh%2B96qNGxTDWBxZpCISryuxbU2VDPeKuwprDpWyqKGx9oksDjMMSAUxmIJcnk8WHzb7WKWymhzhzQxy7%2FBc65HH3wB9ZuQk7qtYcEC7yRxIbSfh3MXzEd29dsthI6EwWqU%2Be%2F87K1IL%2Fhumkt0XFk3RrEMKwQkXaeNQq%2BgOLf9aylqGo9pifchJoyCuN43dCLXvG7x0yYBI2zaMcd8lGl2%2BqRJJZm4RYE8MMWTeSv2EPFLyLErnmVN5KolD2g9YYb1edba%2BNQKvqdUW6xQyVw0OpMK50%2BtK5d4odxIwcr9eO7B6%2FwR0%2BUmgVGAtBVH6oDCwrF9y47ieJMQmFxFxvGKM2oOjUpdWWz4JaHbH0qJo7FsX0IIwF2oiMMMpOQdKEkJRA1VqmuX23UM3Vavp%2B3F%2BEFqgOdXf2gL%2Br%2FE7QtX5aTAh1hyicr6HYBa4z51YZG4JyMmYdTht3eIZ4WMmPaLjKOfXz%2F%2B0Iawj%2BdtxLpuE3FF8eYmTaDyqsu8%2FTQXgAtlN0Wi4TYg6rNBaMYF5VZzBSS29w1yQFvY31IWM8%2BpC7AmvFKQWLS9wdsxt4PcncDY%2B%2B8O83TiqFyRu5KC5Isjnws3RPiQPj%2B%2FKznyYgssc2B2QpgOjMplLMCS%2F1HsAQxxEoAldSF9sq38%2F%2B3HObYuzGgJpLmXzwnAQ2yrFnF0KF%2FF037roKXS1vlQTvhTjMqKRAJl6mFmX6dWUmH6FIFjwJWPAzoo7AKKE6u2sBhT4KOZoERl1xLKhG2X5uruVD3KueuhC6XYGRwS57kCfBi36tWPKYUp%2BlzGi9AyExJBG3FsDe9wYdeQgOCRTk7stJ%2Bl%2B34Jr5sR2kwAd4gPoVs2vJf35I4Smrf4xNRwknGUafh4TSQO4%2FnNPdryw5K%2F8KIMgmTt7s3mi6BWlWv2JKguozhaQ5aiBZLoGdRglZq6iRT3szy5Me2nFy533847YYmS5Q9f4UIFJuI9DPylG3gmVKH899jk1%2BpM2l4FZ%2BmTi3qOO5vq3TRELHqqJVMFA9sddK7%2BGflpkaznnAAcSGIxV9aN%2BSK8rN0kcqdtDmx3L2MdiK5AusY5Av8sJJ7N%2FcF3NZE8&MasterPage%24DDLSiteMap1%24ddlQuickLinks=%7E%2F0' \
           '&MasterPage%24mainContent%24chkLW2=on' \
           '&MasterPage%24mainContent%24chkOR2=on' \
           '&MasterPage%24mainContent%24txtCase2=' \
           '&MasterPage%24mainContent%24rblSearchDateToUse2=Date+Occurred' \
           '&MasterPage%24mainContent%24ddlDates2=Specify+Date' \
           '&MasterPage%24mainContent%24txtDateFrom2=' + date_from_str + '&MasterPage%24mainContent%24txtDateTo2=' + date_to_str + '&MasterPage%24mainContent%24txtLName2=' \
           '&MasterPage%24mainContent%24txtFName2=' \
           '&MasterPage%24mainContent%24txtMName2=' \
           '&MasterPage%24mainContent%24txtStreetNo2=' \
           '&MasterPage%24mainContent%24txtStreetName2=' \
           '&MasterPage%24mainContent%24CGeoCityDDL12=' \
           '&MasterPage%24mainContent%24ddlRange2=' \
           '&MasterPage%24mainContent%24addresslat=' \
           '&MasterPage%24mainContent%24addresslng='
    response = session.post('http://p2c.greensboro-nc.gov/Summary.aspx', headers=headers, data=data, verify=False)
    cookies = response.cookies
    soup = BeautifulSoup(response.text, 'html.parser')
    all_cases = soup.find_all('tr', class_="EventSearchGridRow")
    if all_cases:
        for case in all_cases:
            case_id_regex = "[0-9]{11}+"
            case_id = re.findall(case_id_regex, case.find_all('td')[3].text)
            all_case_ids += case_id
    else:
        run_loop = False
    page += 1
print(len(all_case_ids))
