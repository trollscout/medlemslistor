# -*- coding: utf-8 -*-

'''
Created on 7 apr. 2017

@author: perhk
'''

from django.http import HttpResponse

from .scoutnet import get_memdata
from .dbx import save_file

def go(request):
    memdata = get_memdata()['data']
    mk_listor(memdata)
    resptext = "Loaded "+str(len(memdata))+" records!"
    return HttpResponse(resptext)

# Create lists

avdelningar = ['Sagodjuren', 'Husdjuren', 'Gosedjuren', 'Fabeldjuren', 'Skogsdjuren', 'Urdjuren', 'Rovdjuren', 'Slow Fox', 'Rover']

def mk_listor(memdata):
    epostlistor(memdata)
    kontaktlista(memdata)
    telefonlista(memdata)
    allepost(memdata)

# def epostlistor(memdata):
#     def v(m,f):
#         return memdata[m][f]['value'] if f in memdata[m] else ""
# 
#     for avd in avdelningar:
#         mlist = [m for m in memdata if memdata[m]['unit']['value'] == avd and memdata[m]['date_of_birth']['value'] > "1992-01-01"]
#         elist = []
#         for m in mlist:
#             namn = v(m,'first_name')+" "+v(m,'last_name')
#             if v(m,'email') != "": 
#                 elist.append([namn,"<"+v(m,'email')+">"])
#             if v(m,'contact_email_mum') != "" and v(m,'contact_email_mum') != v(m,'email'):
#                 elist.append([v(m,'contact_mothers_name')+" ("+namn+"s mamma)","<"+v(m,'contact_email_mum')+">"])
#             if v(m,'contact_email_dad') != "" and v(m,'contact_email_dad') != v(m,'email'):
#                 elist.append([v(m,'contact_fathers_name') +" ("+namn+"s pappa)","<"+v(m,'contact_email_dad')+">"])
#             if v(m,'contact_alt_email') != "":
#                 elist.append([namn+" (Extra)","<"+v(m,'contact_alt_email')+">"])
#         f = open("/home/hakan/Temp/listor/"+avd+".txt","w")
#         for l in elist:
#             s = l[0]+"  "+l[1]+";\n"
#             f.write(s)
#         f.close()

def epostlistor(memdata):
    def v(m,f):
        return memdata[m][f]['value'] if f in memdata[m] else ""

    for avd in avdelningar:
        mlist = [m for m in memdata if memdata[m]['unit']['value'] == avd and memdata[m]['date_of_birth']['value'] > "1992-01-01"]
        elista = ""
        for m in mlist:
            namn = v(m,'first_name')+" "+v(m,'last_name')
            if v(m,'email') != "": 
                elista += namn+" <"+v(m,'email')+">" 
            if v(m,'contact_email_mum') != "" and v(m,'contact_email_mum') != v(m,'email'):
                elista += v(m,'contact_mothers_name')+" ("+namn+"s mamma) <"+v(m,'contact_email_mum')+">"
            if v(m,'contact_email_dad') != "" and v(m,'contact_email_dad') != v(m,'email'):
                elista += v(m,'contact_fathers_name')+" ("+namn+"s pappa) <"+v(m,'contact_email_dad')+">"
            if v(m,'contact_alt_email') != "":
                elista += namn+" (Extra) <"+v(m,'contact_alt_email')+">"
        save_file(avd+".txt",elista)
             

def kontaktlista(memdata):
    pass

def telefonlista(memdata):
    pass

def allepost(memdata):
    pass



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

