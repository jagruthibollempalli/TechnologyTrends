import requests as r
from pprint import pprint
import json
import time
from requests.exceptions import Timeout
import urllib3
from urllib.parse import urlencode, quote_plus
scraper_api = 'c0fb1abb7b4dc635c3a4e6b9deb5f15a'
max_session_count = 50
retry_count = 0
session_no = 1
max_retry_count = 10

def getProxyUrl(url,session_no):
    """
    Generates a proxy url through Scraper API
    """
    payload = {'api_key': scraper_api , 'url': url, 'country_code': 'us','session_number':str(session_no % max_session_count)}
    return 'http://api.scraperapi.com/?' + urlencode(payload, quote_via=quote_plus)

def getlevel(field,session_no):
    retry_count=0
    leveldic = {}
    try:
        time.sleep(1)
        url = f"https://academic.microsoft.com/api/analytics/topics/hierarchy?topicPath={field}"
        res = r.get(getProxyUrl(url,session_no)).json()
        retry_count=0
        if len(res['ct'])!=0:
            res = res['ct']
            for i in res:
                leveldic[i['n']]=i['id']
    except:
        session_no += 1
        if retry_count > 20:
            retry_count=retry_count+1
            d = getlevel(field,session_no)
            leveldic = d
        else:
            print(Exception)
    return leveldic


p = [{"c": 2554105, "n": "Humanities", "s": 7162, "id": 15708023, "l": 1}]
url = "https://academic.microsoft.com/api/analytics/topics/hierarchy?topicPath="
res = r.get(url).json()
res = res['ct']
d0={}
dest = {}
for i in res:
    d0[i['n']]=i['id']
# pprint(d0)

d1 = {}
url = "https://academic.microsoft.com/api/analytics/topics/hierarchy?topicPath=71924100"
res = r.get(getProxyUrl(url,session_no)).json()
res = res['ct']
for i in res:
    d1[i['n']]=i['id']
dest["Medicine"]=d1
print(dest)

for k1,v1 in d1.items():
    d2 = getlevel(v1,session_no)
    dest["Medicine"][k1]=d2
    print("1")
    if len(d2)!=0:
        for k2,v2 in d2.items():
            d3 = getlevel(v2,session_no)
            dest["Medicine"][k1][k2]= d3
            print("2")
            if len(d3)!=0:
                for k3,v3 in d3.items():
                    d4 = getlevel(v3,session_no)
                    dest["Medicine"][k1][k2][k3]= d4
                    print("3")
                    if len(d4)!=0:
                        for k4,v4 in d4.items():
                            d5 = getlevel(v4,session_no)
                            dest["Medicine"][k1][k2][k3][k4]= d5
                            print("4")
                            with open('Medicine_subfeild_datafile.json', 'w') as f:
                                json.dump(dest, f)
                                            
