# -*- coding: utf-8 -*-

'''
Created on 7 apr. 2017

@author: perhk
'''

from django.http import HttpResponse

from .scoutnet import get_memdata


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

def epostlistor(memdata):
    def v(m,f):
        return memdata[m][f]['value'] if f in memdata[m] else ""

    for avd in avdelningar:
        mlist = [m for m in memdata if memdata[m]['unit']['value'] == avd and memdata[m]['date_of_birth']['value'] > "1992-01-01"]
        elist = []
        for m in mlist:
            namn = v(m,'first_name')+" "+v(m,'last_name')
            if v(m,'email') != "": 
                elist.append([namn,"<"+v(m,'email')+">"])
            if v(m,'contact_email_mum') != "" and v(m,'contact_email_mum') != v(m,'email'):
                elist.append([v(m,'contact_mothers_name')+" ("+namn+"s mamma)","<"+v(m,'contact_email_mum')+">"])
            if v(m,'contact_email_dad') != "" and v(m,'contact_email_dad') != v(m,'email'):
                elist.append([v(m,'contact_fathers_name') +" ("+namn+"s pappa)","<"+v(m,'contact_email_dad')+">"])
            if v(m,'contact_alt_email') != "":
                elist.append([namn+" (Extra)","<"+v(m,'contact_alt_email')+">"])
        f = open("/home/hakan/Temp/listor/"+avd+".txt","w")
        for l in elist:
            s = l[0]+"  "+l[1]+";\n"
            f.write(s)
        f.close()
        pass
            

def kontaktlista(memdata):
    pass

def telefonlista(memdata):
    pass

def allepost(memdata):
    pass
