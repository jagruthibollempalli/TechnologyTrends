import requests as r
from pprint import pprint
import json
import time
import sys
from requests.exceptions import Timeout
import urllib3
from urllib.parse import urlencode, quote_plus
scraper_api = 'c0fb1abb7b4dc635c3a4e6b9deb5f15a'
max_session_count = 50

def FileSave(filename,content):
    with open(filename, "a") as myfile:
        myfile.write(content)

def getProxyUrl(url,session_no):
    """
    Generates a proxy url through Scraper API
    """
    payload = {'api_key': scraper_api , 'url': url, 'country_code': 'us','session_number':str(session_no % max_session_count)}
    return 'http://api.scraperapi.com/?' + urlencode(payload, quote_via=quote_plus)

def getlevel(field,session_no):
    retry_count=0
    leveldic = {}
    max_retry_count = 20
    while retry_count < max_retry_count:
        try:
            time.sleep(0.23)
            url = f"https://academic.microsoft.com/api/analytics/topics/hierarchy?topicPath={field}"
            res = r.get(getProxyUrl(url,session_no)).json()
            retry_count=0
            if len(res['ct'])!=0:
                res = res['ct']
                for i in res:
                    leveldic[i['n']]=i['id']
            retry_count = max_retry_count + 1
        except Exception as e:
            FileSave("error_test.txt",e)
            FileSave("error_test.txt","\n")
            retry_count += 1
            session_no += 1
    return leveldic


p = [{"c": 2554105, "n": "Humanities", "s": 7162, "id": 15708023, "l": 1}]
dest = {}
d0 = {'Medicine': 71924100, 'Materials science': 192562407,'Chemistry': 185592680, 'Biology': 86803240, 'Engineering': 127413603, 'Physics': 121332964, 'Psychology': 15744967, 'Geology': 127313418, 'Environmental science': 39432304, 'Political science': 17744445, 'Business': 144133560, 'Sociology': 144024400, 'Economics': 162324750, 'Geography': 205649164, 'History': 95457728, 'Philosophy': 138885662,'Computer science': 41008148}
session_no = 120

try:
    for k,v in d0.items():
        d1 = getlevel(v,session_no)
        dest[k]=d1
        FileSave("error_test.txt",k)
        FileSave("error_test.txt","\n")
        if len(d1)!=0:
            for k1,v1 in d1.items():
                d2 = getlevel(v1,session_no)
                dest[k][k1]=d2
                # print("1")
                if len(d2)!=0:
                    for k2,v2 in d2.items():
                        d3 = getlevel(v2,session_no)
                        dest[k][k1][k2]= d3
                        # print("2")
                        if len(d3)!=0:
                            for k3,v3 in d3.items():
                                d4 = getlevel(v3,session_no)
                                dest[k][k1][k2][k3]= d4
                                # print("3")
                                if len(d4)!=0:
                                    for k4,v4 in d4.items():
                                        d5 = getlevel(v4,session_no)
                                        dest[k][k1][k2][k3][k4]= d5
                                        # print("4")
                                        if len(d5)!=0:
                                            for k5,v5 in d5.items():
                                                d6 = getlevel(v5,session_no)
                                                dest[k][k1][k2][k3][k4][k5]= d6
                                                # print("5")
                                        with open(f'{k}_subfeild_datafiless.json', 'w') as f:
                                            json.dump(dest, f)
        with open(f'{k}_subfeild_datafile_ss.json', 'w') as f:
            json.dump(dest, f)
        FileSave("data_done.txt",f"{k} done")  
except Exception as e:
    FileSave("error_test.txt",e)
# sys.stdout.close()            
