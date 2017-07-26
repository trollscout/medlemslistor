'''
Created on 25 juli 2017

@author: hakan
'''

import os, requests

dataurl = "https://www.scoutnet.se/reports/groups/members/group_id/784/download/true/format/json"
loginurl = "https://www.scoutnet.se/login"
auth = {'signin[username]': os.getenv('SCOUTNET_UID','hakan@violaberg.nu'), 'signin[password]': os.getenv('SCOUTNET_PWD','xxxxx')}

def get_memdata():
    s = requests.Session()
    r = s.get(dataurl)
    if r.status_code != 200:
        r = s.post(loginurl,data=auth)  # Need to login
        if r.status_code != 200:
            raise Exception('Bad Scoutnet credentials')
    return r.json()
