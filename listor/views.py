# -*- coding: utf-8 -*-

'''
Created on 7 apr. 2017

@author: perhk
'''

import os

# My only view

from django.http import HttpResponse

def go(request):
    memdata = get_memdata()['data']
    mk_listor(memdata)
    resptext = "Loaded "+str(len(memdata))+" records!"
    return HttpResponse(resptext)

# Create lists

avdelningar = ['Sagodjuren', 'Husdjuren', 'Gosedjuren', 'Fabeldjuren', 'Skogsdjuren', 'Urdjuren', 'Rovdjuren', 'Slow Fox', 'Rover']

def mk_listor(memdata):
    avdelningslistor(memdata)
    allepost(memdata)
    kontaktlista(memdata)
    telefonlista(memdata)

def avdelningslistor(memdata):
    def v(m,f):
        return memdata[m][f]['value'] if f in memdata[m] else ""

    for avd in avdelningar:
        mlist = [m for m in memdata if memdata[m]['unit']['value'] == avd and memdata[m]['date_of_birth']['value'] > "1992-01-01"]
        elista = ""
        for m in mlist:
            namn = v(m,'first_name')+" "+v(m,'last_name')
            if v(m,'email') != "": 
                elista += namn+" <"+v(m,'email')+">;\n"
            if v(m,'contact_email_mum') != "" and v(m,'contact_email_mum') != v(m,'email'):
                elista += v(m,'contact_mothers_name')+" ("+namn+"s mamma) <"+v(m,'contact_email_mum')+">;\n"
            if v(m,'contact_email_dad') != "" and v(m,'contact_email_dad') != v(m,'email'):
                elista += v(m,'contact_fathers_name')+" ("+namn+"s pappa) <"+v(m,'contact_email_dad')+">;\n"
            if v(m,'contact_alt_email') != "":
                elista += namn+" (Extra) <"+v(m,'contact_alt_email')+">;\n"
        save_file(avd+".txt",elista.encode(encoding="utf-8", errors="strict"))


def allepost(memdata):
    def v(m,f):
        return memdata[m][f]['value'] if f in memdata[m] else ""

    mlist = [m for m in memdata if memdata[m]['unit']['value'] != "Under avveckling" and memdata[m]['unit']['value'] != "bara_för_Jamboree17"]
    elist = set()
    for m in mlist:
        if v(m,'email') != "": 
            elist.add(v(m,'email'))
        if v(m,'contact_email_mum') != "" :
            elist.add(v(m,'contact_email_mum'))
        if v(m,'contact_email_dad') != "":
            elist.add(v(m,'contact_email_dad'))
        if v(m,'contact_alt_email') != "":
            elist.add(v(m,'contact_alt_email'))
    data = ""
    for l in elist:
        data += l+";\n"
    save_file("Alla.txt",data.encode(encoding="utf-8", errors="strict"))

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.writer.excel import save_virtual_workbook

def kontaktlista(memdata):
    def v(m,f):
        return memdata[m][f]['value'] if f in memdata[m] else ""

    wb = Workbook()
    ws = wb.active
    a = avdelningar
    a.append('Ledare')
    for avd in a:
        if avd != 'Ledare':
            mlist = [m for m in memdata if memdata[m]['unit']['value'] == avd and memdata[m]['date_of_birth']['value'] > "1992-01-01"]
        else:
            mlist = [m for m in memdata if memdata[m]['date_of_birth']['value'] < "1992-01-01" and memdata[m]['unit']['value'] != "Under avveckling" and memdata[m]['unit']['value'] != "bara_för_Jamboree17"]
        mlist = sorted(mlist,key=lambda m: v(m,'first_name')+" "+v(m,'last_name'))
        ws.title = avd
        if avd != "Ledare":
            header = ["Namn", "Född", "Adress", "Hemtelefon", "Mobiltelefon", "E-post", "Mamma namn", "Mamma mobil", "Mamma e-post", "Pappa namn", "Pappa mobil", "Pappa e-post", "Extra e-epost"]   
            colsizes = [30,8,40,14,14,35,30,14,35,30,14,35,35]
        else:
            header = ["Namn", "Avdelning", "Adress", "Hemtelefon", "Mobiltelefon", "E-post", "Extra e-epost"]   
            colsizes = [30,20,40,14,14,35,35]
        for col in range(len(header)):
            ws.cell(row=1,column=col+1).value = header[col]
            ws.cell(row=1,column=col+1).font = Font(bold=True)
            ws.cell(row=1,column=col+1).fill = PatternFill("solid", fgColor="FFFF00")
            ws.column_dimensions[chr(65+col)].width = colsizes[col]
    
        if avd != "Ledare":
            r = 2
            for m in mlist:
                ws.cell(row=r,column= 1).value = v(m,'first_name')+" "+v(m,'last_name')
                fodd = v(m,'date_of_birth')
                ws.cell(row=r,column= 2).value = fodd[2:4]+fodd[5:7]+fodd[8:10]
                ws.cell(row=r,column= 3).value = v(m,'address_1')+", "+v(m,'postcode')+" "+v(m,'town')
                ws.cell(row=r,column= 4).value = v(m,'contact_home_phone')
                ws.cell(row=r,column= 5).value = v(m,'contact_mobile_phone')
                ws.cell(row=r,column= 6).value = v(m,'email')
                ws.cell(row=r,column= 7).value = v(m,'contact_mothers_name')
                ws.cell(row=r,column= 8).value = v(m,'contact_mobile_mum')
                ws.cell(row=r,column= 9).value = v(m,'contact_email_mum')
                ws.cell(row=r,column=10).value = v(m,'contact_fathers_name')
                ws.cell(row=r,column=11).value = v(m,'contact_mobile_dad')
                ws.cell(row=r,column=12).value = v(m,'contact_email_dad')
                ws.cell(row=r,column=13).value = v(m,'contact_alt_email')
                r += 1
        else:
            r = 2
            for m in mlist:
                ws.cell(row=r,column= 1).value = v(m,'first_name')+" "+v(m,'last_name')
                ws.cell(row=r,column= 2).value = v(m,'unit')
                ws.cell(row=r,column= 3).value = v(m,'address_1')+", "+v(m,'postcode')+" "+v(m,'town')
                ws.cell(row=r,column= 4).value = v(m,'contact_home_phone')
                ws.cell(row=r,column= 5).value = v(m,'contact_mobile_phone')
                ws.cell(row=r,column= 6).value = v(m,'email')
                ws.cell(row=r,column= 7).value = v(m,'contact_alt_email')
                r += 1
        ws = wb.create_sheet()
    wb.remove_sheet(ws)     # Remove empty sheet
    save_file("Kontaktlista.xlsx",save_virtual_workbook(wb))

def telefonlista(memdata):
    def v(m,f):
        return memdata[m][f]['value'] if f in memdata[m] else ""

    wb = Workbook()
    ws = wb.active
    ws.title = "Telefonlista"
    memdata = sorted(memdata,key=lambda m: v(m,'first_name')+" "+v(m,'last_name'))
    header = ["Namn", "Avdelning", "Hemtelefon", "Mobiltelefon", "Mamma mobil", "Pappa mobil"]
    colsizes = [30,20,14,14,14,14]
    for col in range(len(header)):
        ws.cell(row=1,column=col+1).value = header[col]
        ws.cell(row=1,column=col+1).font = Font(bold=True)
        ws.cell(row=1,column=col+1).fill = PatternFill("solid", fgColor="FFFF00")
        ws.column_dimensions[chr(65+col)].width = colsizes[col]
    r = 2
    for m in memdata:
        ws.cell(row=r,column=1).value = v(m,'first_name')+" "+v(m,'last_name')
        ws.cell(row=r,column=2).value = v(m,'unit')
        ws.cell(row=r,column=3).value = v(m,'contact_home_phone')
        ws.cell(row=r,column=4).value = v(m,'contact_mobile_phone')
        ws.cell(row=r,column=5).value = v(m,'contact_mobile_mum')
        ws.cell(row=r,column=6).value = v(m,'contact_email_dad')
        r += 1
    save_file("Telefonlista.xlsx",save_virtual_workbook(wb))

# Droxbox upload function

import dropbox

DBX_OAUTHKEY = os.getenv('DBX_OAUTHKEY', 'P_f0hApputAAAAAAAAABxl2HC2JCkUP6lkYH3btQxjlhXT-Cve8xg-IRzNB4qJaq')
DBX_BASEDIR = "/Aktuella kontakt- och e-postlistor/"

def save_file(fname, data):
        dbx = dropbox.Dropbox(DBX_OAUTHKEY)
        dbx.files_upload(data, DBX_BASEDIR+fname, dropbox.files.WriteMode.overwrite, mute=True)

# Scoutnet download function

import requests

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

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# import json
# def get_memdataX():
#     return json.load(open(BASE_DIR+"/alla.json","r"))



# contact_home_phone {'value': '087763327'}
# prev_term_due_date {'value': '2016-10-31'}
# contact_mobile_mum {'value': '0722333777'}
# first_name {'value': 'Veronica'}
# prev_term {'value': 'Betalt', 'raw_value': 'paid'}
# contact_fathers_name {'value': 'Håkan Persson'}
# unit {'value': 'Slow Fox', 'raw_value': '8907'}
# current_term {'value': 'Betalt', 'raw_value': 'paid'}
# created_at {'value': '2011-11-05'}
# email {'value': 'veronica@violaberg.nu'}
# date_of_birth {'value': '2002-01-02'}
# contact_mobile_dad {'value': '0702178177'}
# country {'value': 'Sverige'}
# last_name {'value': 'Ekenberg'}
# ssno {'value': '20020102-1904'}
# sex {'value': 'Kvinna', 'raw_value': '2'}
# member_no {'value': '3230994'}
# contact_mobile_phone {'value': '0767994483'}
# address_1 {'value': 'Violabergsvägen 4'}
# group {'value': 'Trollbäckens scoutkår', 'raw_value': '784'}
# status {'value': 'Aktiv', 'raw_value': '2'}
# confirmed_at {'value': '2014-08-20'}
# current_term_due_date {'value': '2017-03-31'}
# postcode {'value': '13668'}
# contact_email_mum {'value': 'eva@violaberg.nu'}
# contact_mothers_name {'value': 'Eva Ekenberg'}
# contact_email_dad {'value': 'hakan@violaberg.nu'}
# town {'value': 'Vendelsö'}

