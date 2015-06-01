# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json

import pickle
import bs4
from OPS2NetUtils2 import ReturnBoolean, Decoupe, UnNest, CleanPatent
import datetime

with open("..//Requete.cql", "r") as fic:
    contenu = fic.readlines()
    for lig in contenu:
        #if not lig.startswith('#'):
            if lig.count('request:')>0:
                requete=lig.split(':')[1].strip()
            if lig.count('DataDirectory:')>0:
                ndf = lig.split(':')[1].strip()
            if lig.count('GatherContent')>0:
                Gather = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherBiblio')>0:
                GatherBiblio = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherPatent')>0:
                GatherPatent = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherFamilly')>0:
                GatherFamilly = ReturnBoolean(lig.split(':')[1].strip())

rep = ndf

#if ndf.count('Families')>0:
#    clesRef = ['label',  'titre', 'date', 'citations','family lenght', 'priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'prior']
#else:
clesRef = ['label', 'citations', 'titre', 'date','priority-active-indicator', 'IPCR11', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'IPCR4', 'IPCR7', "Inventor-Country", "Applicant-Country"] #"citations"


ListBiblioPath = '..//DONNEES//'+rep+'//PatentBiblios'#Biblio'
ListPatentPath = '..//DONNEES//'+rep+'//PatentLists'#List
ResultPathContent = '..//DONNEES//'+rep #+'//PatentContentsHTML'
temporPath = '..//DONNEES//'+rep+'//tempo'



with open(ListBiblioPath+'//'+ndf, 'r') as data:
    LstBrevet = pickle.load(data)
    
with open(ListPatentPath+'//'+ndf, 'r') as data:
    DataBrevet = pickle.load(data)

if isinstance(LstBrevet, dict):
    data = LstBrevet
    LstBrevet = data['brevets']    
    if data.has_key('requete'): 
        DataBrevet['requete'] = data["requete"]
    if data.has_key('number'):
        print "Found ", data["number"], " patents! Formating to HMTL tables"
    
LstExp = [] 
LstExp2 = [] 
for brev in LstBrevet:
    brev = CleanPatent(brev)
    
    
    tempo = dict() # this one for DataTable
    tempo2 = dict() #the one for pitable
    PaysInv= [] #new field
    PaysApp = []
#    tempo = CleanPatent(brev)
#    brevet= SeparateCountryField(tempo)
    #cleaning classification
    for key in clesRef:
        if key =='titre' or key =='inventeur' or key =='applicant':
            if isinstance(brev[key], list):
                tempo[key] = ' '.join(brev[key]).title().strip()
            else:
                tempo[key] = brev[key].capitalize().strip()
        else:
            if isinstance(brev[key], list):
                tempo[key] = ', '.join(brev[key])
            elif 'None' in brev[key]:
                tempo[key] = ''
            else:
                tempo[key] = brev[key]
 
   ##
                
    LstExp.append(tempo)
    
    
#    tfiltering against keys
    tempo2=dict()
    clesRef2 = ['label', 'date',  'priority-active-indicator', 'portee', 'applicant', 'pays', 'inventeur',  'IPCR4', 'IPCR7', "Inventor-Country", "Applicant-Country", 'citations'] #'citations','representative',
    for ket in clesRef2:
        if isinstance(brev[ket], list):
            tempo2[ket] = UnNest(brev[ket])
        else:
            tempo2[ket] = brev[ket]
    tempoBrev = Decoupe(tempo2)
    for nb in tempoBrev:
#        brev2 = CleanPatentOthers(tempoBrev[nb])
        brev2 = tempoBrev[nb]
        
        tempo2 = dict() #the one for pitable
        for cle in clesRef2:
            if brev2[cle] is not None and brev2[cle] != 'N/A' and brev2[cle] != 'UNKNOWN':
                if isinstance(brev2[cle], list) and len(brev2[cle])>1:
                    tempo2[cle] = [bs4.BeautifulSoup(unit).text for unit in brev2[cle] if unit !='N/A']
                    if len(tempo2) == 1:
                        tempo2[cle] = tempo2[cle][0]
                elif isinstance(brev2[cle], list) and len(brev2[cle]) == 1:
                    tempo2[cle] = [bs4.BeautifulSoup(brev2[cle][0]).text.replace('N/A', '')]
                    if len(tempo2) == 1:
                        tempo2[cle] = tempo2[cle][0]
                if cle =='titre':
                    pass # no need of titles
                if cle  ==  'date':
                
                    if isinstance(brev2[cle], datetime.date):
                        tempo2 [cle] = str(brev2.year)
                    elif isinstance(brev2[cle], str) or isinstance(brev2[cle], unicode):
                        if len(brev2[cle])>0:
                            tempo2 [cle] = brev2[cle].split('-')[0]
                    else:
                        tempo2 [cle] = ''
                            
                if cle == 'applicant' or cle == 'inventeur':
                    temp = unicode(brev2[cle]).capitalize()
                    if temp.count('[')>0:
                        tempo2 [cle] = temp.split('[')[0]
                    else:
                        tempo2 [cle] = temp
                elif cle not in ['applicant', 'inventeur', 'date', 'titre']:
                    if isinstance(brev2[cle], list):
                        temp = unicode(' '.join(brev2[cle])).replace('N/A', '').strip()
                    else:
                        temp = unicode(brev2[cle])
                    soup = bs4.BeautifulSoup(temp)
                    temp = soup.text
                    tempo2 [cle] = temp.replace('N/A', '')
                    
            else:
                tempo2[cle] = ''
        if tempo2 not in LstExp2:
            LstExp2.append(tempo2)
    print len(LstExp2),
    
Exclude = []
print "entering formating html process"
dicoRes = dict()
dicoRes['data'] = LstExp
contenu = json.dumps(dicoRes, ensure_ascii=True, indent = 3)
contenu2 = json.dumps(LstExp2, ensure_ascii=True, indent = 3)

import codecs
#if rep != ndf:
#    if ndf.lower() == 'families'+rep.lower():
#        #ndf = 'Families'+ ndf
#        Modele = "ModeleFamille.html"
#else:
#    
Modele = "Modele.html"
with codecs.open(ResultPathContent + '//'  +ndf+'.csv', 'w', 'utf-8') as resFic:
    entete = ''.join([u +';' for u in clesRef]) +'\n'
    resFic.write(entete)
    for brev in LstBrevet:
        ligne = ''
        for cle in clesRef:
            if isinstance(brev[cle], list):
                temp=''
                for k in brev[cle]:
                    temp += unicode(k) + ' '
                try:
                    ligne += unicode(temp, 'utf8', 'replace') +';'
                except:
                    try:
                        ligne += unicode(temp, 'cp1252', 'replace') +';' 
                    except:
                        try:
                            ligne += unicode(temp, 'latin1', 'replace') +';'
                        except:
                            try:
                                ligne += unicode(temp) +';'
                            except:
                                print 'paté'
            else:
                try:
                    ligne += unicode(brev[cle], 'utf8', 'replace') +';'
                except:
                    ligne += unicode(brev[cle]) +';'
                    
        ligne += '\n'
        resFic.write(ligne)

with codecs.open(ResultPathContent + '//'  +ndf+'.bib', 'w', 'utf-8') as resFic:
    cleBib = ['date', 'portee', 'titre', 'inventeur', 'IPCR11', 'label', 'pays']
    for bre in LstBrevet:
        if len(cleBib) == len([cle for cle in cleBib if cle in bre.keys()]):
            Gogo = True #checkin consistency
            for cle in cleBib:
                Gogo = Gogo * (bre[cle] is not None)
                Gogo = Gogo * (u'None' not in bre[cle])
                Gogo = Gogo * ( bre[cle] != u'')
            if Gogo>0:
                if "B" in ' '.join(bre['portee']) or "C" in ' '.join(bre['portee']): #filter patent list again their status... only published
                    if bre['dateDate'] is not None and bre['dateDate'] != u'None' and bre['dateDate'] != u'' and u'None' not in bre['dateDate']:
                        # hum last test prooves that they is a bug in collector for dateDate field
                        if isinstance(bre['dateDate'], list):
                            Date = bre['dateDate'][0] #first publication
                        else:
                            Date = bre['dateDate']
                    else:
                        if isinstance(bre['date'], list):
                            temp= bre['date'][0] #first publication
                            temp = temp.split('-')
                            Date = datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))
                        else:
                            temp = bre['date']
                            temp = temp.split('-')
                            Date = datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))
                            
                    if isinstance(bre['inventeur'], list):
                        entryName=bre['inventeur'][0].split(' ')[0]+'etAl'+str(Date.year)

                        tempolist = [nom.title() for nom in bre['inventeur']]
                        Authors = unicode(' and '.join(tempolist))
                    else:
                        entryName=bre['inventeur'].split(' ')[0]+'etAl'+str(Date.year)
                        Authors = bre['inventeur'].title()
                    resFic.write(u'@Patent{'+entryName+',\n')
                    resFic.write(u'\t author={' + Authors + '},\n')
                    resFic.write(u"\t title = {"+unicode(bre['titre']).capitalize() +"},\n")
                    resFic.write(u"\t year = {" +str(Date.year)+ "},\n")
                    resFic.write(u"\t month = {" +str(Date.month)+ "},\n")
                    resFic.write(u"\t day = {" +str(Date.day)+ "},\n")
                    resFic.write(u"\t number = {" +str(bre['label'])+ "},\n")
                    resFic.write(u"\t location = {" +str(bre['pays'])+ "},\n")
                    if isinstance(bre['IPCR11'], list):
                        resFic.write(u"\t IPC_class = {" + str(', '.join(bre['IPCR11'])) + "},\n")
                    else:
                        resFic.write(u"\t IPC_class = {" + str(bre['IPCR11']) + "},\n")
                    resFic.write(u"\t url = {" +"http://worldwide.espacenet.com/searchResults?compact=false&ST=singleline&query="+str(bre['label'])+"&locale=en_EP&DB=EPODOC" + "},\n")
                    resFic.write(u"}\n \n")
        
#@Patent{EHLINGER:2006:biblatex,
# author = {EHLINGER, JR., Philip Charles},
# title = {Device for the treatment of hiccups},
# year = {2006},
# month = {06},
# day = {13},
# number = {US 7062320},
# type = {Patent},
# version = {},
# location = {US},
# url = {http://www.patentlens.net/patentlens/patent/US_7062320/},
# filing_num = {10684114},
# yearfiled = {2003},
# monthfiled = {10},
# dayfiled = {14},
# pat_refs = {US 408607 A (Aug, 1889) Flint 607/134; US 4210141 A (Jul, 1980) Brockman et al. 604/78},
# IPC_class = {A61N 1/04},
# US_class = {607  2},
# abstract = {A device for the treatment of hiccups, and more specifically, to a method and apparatus for the treatment of hiccups involving galvanic stimulation of the Superficial Phrenetic and Vagus nerves using an electric current.}
#}

with open(ResultPathContent + '//' +ndf+'.json', 'w') as resFic:
    resFic.write(contenu)

with open(ResultPathContent + '//' + ndf+'Pivot.json', 'w') as resFic:
    resFic.write(contenu2)
with open(Modele, "r") as Source:
    html = Source.read()
    html = html.replace('**fichier**', ndf+'.json' )  
    
    html = html.replace('**fichierHtmlFamille**', 'Families'+ndf+'.html' )
    html = html.replace('**fichierPivot**', ndf+'Pivot.html' )

    html = html.replace('**requete**', DataBrevet['requete'].replace('"', ''))
    with open(ResultPathContent + '//' + ndf+'.html', 'w') as resFic:
        resFic.write(html)

FichierHtml=ndf+'.html'
ModelePivot = "Pivot.html"
with open(ModelePivot, "r") as Source:
    html = Source.read()
    html = html.replace('**fichier**', ndf+'Pivot.json' )  
    html = html.replace('**requete**', DataBrevet['requete'].replace('"', ''))
    html = html.replace('**FichierHtml**', FichierHtml)
    html = html.replace('**FichierHtmlFamille**', 'Families'+FichierHtml)
    with open(ResultPathContent + '//' + ndf+'Pivot.html', 'w') as resFic:
        resFic.write(html)

with open("scriptSearch.js", 'r') as Source:
    js = Source.read()
    js = js.replace('***fichierJson***', ndf+'.json')
    js = js.replace('{ "data": "application-ref"},', '') 
    with open(ResultPathContent + '//' + 'scriptSearch.js', 'w') as resFic:
        resFic.write(js)

#os.system('start firefox -url '+ URLs.replace('//','/') )
