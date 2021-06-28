# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 20:34:39 2020

@author: Yepeng Jin

"""
#This is the major script that contains the functions to crawl the journal author guideline web pages [submissionlink.csv, instruction text.csv] and to construct the datasets for plot purpose [word count and journal count_comm.csv, final_plot.csv].
import numpy as np
from magic_google import MagicGoogle
import pprint
import time
from os import listdir
from os.path import isfile,join
import pandas as pd
import math
from selenium import webdriver
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import urllib
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="ticks")
import numpy as np

pattern=r"/"
# Or PROXIES = None
PROXIES = [{
    'http': 'http://192.168.2.207:1080',
    'https': 'http://192.168.2.207:1080'
}]


fake_header = {  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2"
        }


# Or MagicGoogle()
mg = MagicGoogle()



# Some instrumental functions
def check_interdis(x,y):
    if(x=='interdisciplinary'):
        return 'Interdisciplinary'
    else:
        return y

def change_interdis(x): 
    if(type(x)==str):
        return 'Interdisciplinary'
    else:
        return 'Not Interdisciplinary'

def add_inter(x,y):
    if(type(x)==str):
        return 'Interdisciplinary'
    else:
        return y

def check_rep_word():
    rep_word='reporting.?standard'
    z=pd.read_csv('instruction text.csv')
    for i in range(len(z)):
        text=z['text'].iloc[i]
        if(len(re.findall(rep_word,text,re.I))>0):
            print (z['submission link'].iloc[i])

def replace_qualitative (x):
    if(x==True):
        return 'Qualitative Journals'
    if(x==False):
        return 'Non Qualitative Journals'





# Get the link
def get_submission_link():
    j_name_list=[]
    j_field_list=[]
    j_link_list=[]
    j_pdf_list=[]
    j_note_list=[]
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path
    for f in listdir('.\journal'):
        j_df=pd.read_csv('.\journal\\'+f)
        j_col=j_df[j_df.columns[1]]
    
        for i in range(1,len(j_col)):
            j_name=j_col[i]
            if(j_name in j_name_list):
                continue
            else:
                if(isinstance(j_name,str)):
                    query_text=j_name+', author instructions'
                    t=0
                    for j_url in mg.search_url(query=query_text):
                        if(t>0):
                            continue
                        else:
                            j_pdf_indicator=False
                            j_note=math.nan
        
                            #Some publications are tandfonline
                            if(j_url[:28]=='https://www.tandfonline.com/' and (not 'instructions' in j_url)):
                                j_abbr=re.split(pattern,j_url)[4]
                                j_url='https://www.tandfonline.com/action/authorSubmission?show=instructions&journalCode='+j_abbr
                            #Some publications are Wiley
                            if(j_url[:40]=='https://onlinelibrary.wiley.com/journal/' and (not 'forauthors' in j_url)):
                                
                                j_abbr=re.split(pattern,j_url)[4]
                                j_url='https://onlinelibrary.wiley.com/page/journal/'+j_abbr+'/homepage/forauthors.html'
                            
                            if(j_url[:21]=='https://benjamins.com' and (not 'guidelines' in j_url)):
                                j_url=j_url+'/guidelines'
                            if(j_url[:33]=='https://journals.sagepub.com/home' and (not 'instructions' in j_url)):
                                j_abbr=re.split(pattern,j_url)[4]
                                j_url='https://journals.sagepub.com/author-instructions/'+j_abbr
                            if(j_url[:23]=='https://uk.sagepub.com/' and (not 'submission' in j_url)):
                                j_url=j_url+'#submission-guidelines'
                            if(j_url[:23]=='https://us.sagepub.com/'and (not 'submission' in j_url)):
                                j_url=j_url+'#submission-guidelines'
                                
                            if(j_url[:46]=='https://www.emeraldgrouppublishing.com/journal' and (not 'guidelines' in j_url)):
                                j_url=j_url+'#author-guidelines'
                            #apa use some anti-crawling techonology
                            if(j_url[:33]=='https://www.apa.org/pubs/journals' ):
                                j_url=j_url+'?tab=4'
    
                            if(j_url[:28]=='https://www.inderscience.com' and (not 'inauthors' in j_url)):
                                j_url='https://www.inderscience.com/mobile/inauthors/index.php?pid=71'
                            if(j_url[:45]=='https://spssi.onlinelibrary.wiley.com/journal' and (not 'guidelines' in j_url)):
                                j_abbr=re.split(pattern,j_url)[4]
                                j_url='https://spssi.onlinelibrary.wiley.com/hub/journal/'+j_abbr+'/about/author-guidelines'
                            
                            if(j_url[:30]=='https://www.cogitatiopress.com' and (not 'forauthors' in j_url)):
                                j_url=j_url+'/pages/view/forauthors'
                            if(j_url[:25]=='https://procomm.ieee.org/' and (not 'guidelines' in j_url)):
                                j_url=j_url+'for-prospective-authors/guidelines-to-follow/'
                            if((j_url[:25]=='https://www.springer.com/') and (not 'submission-guidelines' in j_url)):   
                                j_url=j_url+'/submission-guidelines'
                            if((j_url[:29]=='https://www.nowpublishers.com') and (not 'nstructions' in j_url)):
                                j_abbr=re.split(pattern,j_url)[3]
                                j_url='https://www.nowpublishers.com/Journal/AuthorInstructions/'+j_abbr
                            #Mitpress
                            if(j_url[:33]=='https://www.mitpressjournals.org/'):
                                j_abbr=re.split(pattern,j_url)[4]
                                j_url='https://www.mitpressjournals.org/journals/'+j_abbr+'/sub'           
                            #Oxford Academic
                            if(j_url[:25]=='https://academic.oup.com/' and (not 'nstructions' in j_url) and (j_name!='JOURNALS OF GERONTOLOGY SERIES B-PSYCHOLOGICAL SCIENCES AND SOCIAL SCIENCES')): #There are both instructions and Instructions
                                j_url=j_url+'/pages/Instructions_To_Authors'
                            if(j_name=='JOURNALS OF GERONTOLOGY SERIES B-PSYCHOLOGICAL SCIENCES AND SOCIAL SCIENCES'):
                                j_note='Two instuctions, second is https://academic.oup.com/psychsocgerontology/pages/General_Instruction_2'
                                j_url='https://academic.oup.com/psychsocgerontology/pages/General_Instruction_1'
                            #Cambridge University Press
                            if(j_url[:40]=='https://www.cambridge.org/core/journals/' and (not 'nstructions' in j_url)):
                                j_url=j_url+'/information/instructions-contributors'
                            #palgrave
                            if(j_url[:35]=='https://www.palgrave.com/gp/journal'):
                                j_url=j_url+'/authors/submission'                    
                            #brill
                            if(j_url[:17]=='https://brill.com' and (not 'structions' in j_url)):
                                j_abbr=re.split(pattern,j_url)[3]
                                j_pdf_indicator=True
                                j_url='https://brill.com/fileasset/downloads_products/Author_Instructions/'+j_abbr.upper()+'.pdf'
                           #ucpress
                            if(j_url[:26]=='https://online.ucpress.edu' and (not 'submit' in j_url)):
                                j_url=j_url+'/pages/submit'        
                                
                           #Human kinetics
                            if(j_url[:34]=='https://journals.humankinetics.com'):
                                j_url=j_url+'?tab_body=null-6934'
                                
                            if(j_name=='HUMAN COMMUNICATION RESEARCH'):
                                j_url='https://academic.oup.com/hcr/pages/General_Instructions'
                            if(j_name=='Comunicar'):
                                j_pdf_indicator=True
                                j_url='https://www.revistacomunicar.com/normas/01-normativa-comunicar-en.pdf'
                            if(j_name=='JOURNAL OF ADVERTISING RESEARCH'):
                                j_pdf_indicator=True
                                j_url='http://www.journalofadvertisingresearch.com/sites/default/files/Additional_assets/JAR%20Guidelines.pdf'
                            if(j_name=='Cyberpsychology-Journal of Psychosocial Research on Cyberspace'):
                                j_url=j_url+'about/submissions?navItem=1'
                            
                            #The hogrefe series
                            if(j_name=='Journal of Media Psychology-Theories Methods and Applications'):
                                j_pdf_indicator=True
                                j_url='https://us.hogrefe.com/fileadmin/user_upload/global/journals/Hogrefe_Publishing/Journal_of_Media_Psychology/zmp_author_instructions_current_01.pdf'
                            if(j_name=='Social Psychology'):
                                j_pdf_indicator=True
                                j_url='https://us.hogrefe.com/fileadmin/user_upload/global/journals/Hogrefe_Publishing/Social_Psychology/zsp_author_instructions_current.pdf'
                            if(j_name=='Journal of Individual Differences'):
                                j_pdf_indicator=True
                                j_url='https://us.hogrefe.com/fileadmin/user_upload/global/journals/Hogrefe_Publishing/Journal_of_Individual_Differences/jid_author_instructions_general_01.pdf'
                            if(j_name=='Zeitschrift fur Neuropsychologie'):
                                j_pdf_indicator=True
                                j_note='language: German'
                                j_url='https://www.hogrefe.de/fileadmin/user_upload/hogrefe_ch/Downloads/Autorenrichtlinien/AutorenR_ZNP.pdf'
                            #The pdf guidelines
                            
                            if(j_name=='Revista Argentina de Clinica Psicologica'):
                                j_pdf_indicator=True
                                j_url='https://revistaclinicapsicologica.com/Author-GuidelinesRACP.pdf'
                            if(j_name=='Pratiques Psychologiques'):
                                j_pdf_indicator=True
                                j_url='http://www.em-consulte.com/getInfoProduit/PRPS/instructionsAuteurs/PRPS.pdf'
                            if(j_name=='ANNALES MEDICO-PSYCHOLOGIQUES'):
                                j_pdf_indicator=True
                                j_url='http://www.em-consulte.com/getInfoProduit/AMEPSY/instructionsAuteurs/AMEPSY.pdf'
                            if(j_name=='Communications-European Journal of Communication Research'):
                                j_note='link not work'
                            if(j_name=='Tijdschrift voor Communicatiewetenschap'):
                                j_note='language: Dutch'
                                j_pdf_indicator=True
                                j_url='https://www.tijdschriftvoorcommunicatiewetenschap.nl/documenten/auteursintructie_2017.pdf'
                            if(j_name=='Gedrag & Organisatie'):
                                j_note='word'
                                j_pdf_indicator=True
                                j_url='http://www.editorialmanager.com/homepage/docs/Author_Tutorial.doc'                        
                            
                            
                            if(j_name=='COMMUNIST AND POST-COMMUNIST STUDIES'):
                                j_note='google_doc'
                                j_pdf_indicator=True
                                j_url='https://docs.google.com/document/d/1ljB5IiuGtbug0Zb_gGJMY_CVUGGE7MVxlMDF-kkKuy8/edit'
                            
                            
                            if(j_name=='JOURNAL OF SOCIAL ISSUES'):
                                j_note='coming soon'
                            if(j_name=='International Review of Social Psychology'):
                                j_url=j_url+'about/submissions/'
                            if(j_name=='Advances in Experimental Social Psychology'):
                                j_note='No guidelines found'
                            #Annual Review
                            if(j_name in ['Annual Review of Political Science','Annual Review of Psychology','Annual Review of Clinical Psychology']):
                                j_pdf_indicator=True
                                j_url='https://www.annualreviews.org/pb-assets/Authors%20Assets/AuthorHandbook-Harvard-1582569075420.pdf'
        
                            if(j_name=='Nebraska Symposium on Motivation'):
                                j_pdf_indicator=True
                                j_note='Five documents'
                                j_url='https://www.nebraskapress.unl.edu/authors/manuscript-preparation/'
                            #apsanet
                            if(j_name=='Perspectives on Politics'):
                                j_url='https://www.apsanet.org/perspectivessubmissions'
                            
                            if(j_name=='PS-POLITICAL SCIENCE & POLITICS'):
                                j_url='https://www.apsanet.org/pssubmissions'
                            
                            #Wiley
                            if(j_name=='EUROPEAN JOURNAL OF POLITICAL RESEARCH'):
                                j_url='https://ejpr.onlinelibrary.wiley.com/hub/journal/14756765/homepage/forauthors.html'
                            if(j_name=='Clinical Psychologist'):
                                j_url='https://aps.onlinelibrary.wiley.com/hub/journal/17429552/forauthors.html'
    
                            #some palgrave
                            if(j_name=='Comparative European Politics'):
                                j_url='https://www.palgrave.com/gp/journal/41295/authors/submission'
                            
                            
                            #Elesvier
                            if(j_name=='European Journal of Political Economy'):
                                j_url='https://www.elsevier.com/journals/european-journal-of-political-economy/0176-2680/guide-for-authors'
                            if(j_name=='JOURNAL OF MEMORY AND LANGUAGE'):
                                j_url='https://www.elsevier.com/journals/journal-of-memory-and-language/0749-596x/guide-for-authors'
                            #Some springer
                            if(j_name=='STUDIES IN COMPARATIVE INTERNATIONAL DEVELOPMENT'):
                                j_pdf_indicator=True
                                j_url='http://www.springer.com/cda/content/document/cda_downloaddocument/12116_SCID_Instructions+for+Authors_20190606.pdf?SGWID=0-0-45-1517779-p173732520'
                            if(j_name=='Journal of Chinese Political Science'):
                                j_pdf_indicator=True
                                j_url='http://www.springer.com/cda/content/document/cda_downloaddocument/Instructions+for+Authors.pdf?SGWID=0-0-45-1441102-p37235898'
                            #Tandfonline
                            if(j_name=='Journal of Media Ethics'):
                                j_url='https://www.tandfonline.com/action/authorSubmission?show=instructions&journalCode=hmme21'                      
                            #cambride:
                            if(j_name=='CANADIAN JOURNAL OF POLITICAL SCIENCE-REVUE CANADIENNE DE SCIENCE POLITIQUE'):
                                j_url='https://www.cambridge.org/core/journals/canadian-journal-of-political-science-revue-canadienne-de-science-politique/information/instructions-for-contributors-directives-aux-auteurs-es'
                            
                            if(j_name=='International Journal of Conflict and Violence'):
                                j_url='https://www.ijcv.org/index.php/ijcv/about/submissions'
                            #scielo
                            if(j_name=='Revista de Ciencia Politica'):
                                j_url='https://scielo.conicyt.cl/revistas/revcipol/iinstruc.htm'
                            if(j_name=='Revista de Estudios Politicos'):
                                j_url='http://www.scielo.org.co/revistas/espo/iinstruc.htm'
                                
                            if(j_name=='Contemporary Southeast Asia'):
                                j_url='https://bookshop.iseas.edu.sg/journal-details/cs#submissions'
                            if(j_name=='Romanian Journal of Political Science'):
                                j_url='http://www.sar.org.ro/polsci/?page_id=841'
                            #Differnt language
                            if(j_name=='POLITICA Y GOBIERNO'):
                                j_url='http://www.politicaygobierno.cide.edu/index.php/pyg/directrices' #spanish
                                j_note='language: Spanish'
                            if(j_name=='Austrian Journal of Political Science'):
                                j_url='https://webapp.uibk.ac.at/ojs/index.php/OEZP/about/submissions#authorGuidelines'
                                j_note='language: Germany'
                            if(j_name=='Revista del CLAD Reforma y Democracia'):
                                j_url='https://clad.org/acerca-de/publicaciones/revista-clad/bases-colaboraciones-revista'
                                j_note='language: Spanish'
                            if(j_name=='INTERNASJONAL POLITIKK'):
                                j_url='https://tidsskriftet-ip.no/index.php/intpol/guidelines'
                                j_note='language:norewegian'
                            if(j_name=='Historia y Politica'):
                                j_url='https://recyt.fecyt.es/index.php/Hyp/about/submissions'
                                j_note='language: Spanish'
                            if(j_name=='OSTEUROPA'):
                                j_url='https://www.bwv-verlag.de/hinweisezurmanuskripterstellung'
                                j_note='language:German'
                            if(j_name=='ZEITSCHRIFT FUR PSYCHOSOMATISCHE MEDIZIN UND PSYCHOTHERAPIE'):
                                j_url='https://www.vandenhoeck-ruprecht-verlage.com/service/autorinnen-und-autoren/'
                                j_note='language: German'
                            if(j_name=='Geriatrie et Psychologie Neuropsychiatrie de Vieillissement'):
                                j_note='language:German'
                                j_url='https://www.jle.com/en/revues/gpn/espace_auteur'                    
                            #Some notes
                            if(j_name=='MONTHLY REVIEW-AN INDEPENDENT SOCIALIST MAGAZINE'):
                                j_url='https://monthlyreview.org/submissions/'
                                j_note='You need to select something'
                            if(j_name=='NEW REPUBLIC'):
                                j_url='https://newrepublic.com/pages/contact'
                                j_note='more like a media rather than journal'
                            
                            #Degruyter
                            if(j_name=='Forum-A Journal of Applied Research in Contemporary Politics'):
                                j_url='https://www.degruyter.com/view/journals/for/for-overview.xml?tab_body=editorialContent-78050'
                                
                            if(j_name=='Lex Localis-Journal of Local Self-Government'):
                                j_url='http://pub.lex-localis.info/index.php/LexLocalis/about/submissions'    
                            if(j_name=='Journal of Australian Political Economy'):
                                j_url='https://www.ppesydney.net/jape-submission-guidelines/'
                            if(j_name=='PSYCHOSOMATIC MEDICINE'):
                                j_url='https://journals.lww.com/psychosomaticmedicine/pages/instructionsforauthors.aspx'
                            if(j_name=='Frontiers in Human Neuroscience'):
                                j_url='https://www.frontiersin.org/about/author-guidelines'
                            if(j_name=='JOURNAL OF SPORT & EXERCISE PSYCHOLOGY'):
                                j_url='https://journals.humankinetics.com/view/journals/jsep/jsep-overview.xml?tab_body=null-6934'
                            if(j_name=='CLINICAL NEUROPSYCHOLOGIST'):
                                j_url='https://www.tandfonline.com/doi/full/10.1080/13854046.2011.639495'
                            if(j_name=='Applied Neuropsychology-Adult'):
                                j_url='https://www.tandfonline.com/action/authorSubmission?show=instructions&journalCode=hapn21'
                            if(j_name=='INTERNATIONAL JOURNAL OF SPORT PSYCHOLOGY'):
                                j_url='http://www.ijsp-online.com/manuscript/guidelines'
                            #cairn use some anti-crawling techonology either
                            if(j_name=='TRAVAIL HUMAIN'): 
                                j_url='https://www.cairn-int.info/journal-le-travail-humain.htm?contenu=about'
        
                                
                            
                            pprint.pprint(j_url)
                            driver.get(j_url)
                            time.sleep(3)
                            
                            j_name_list.append(j_name)
                            j_field_list.append(f[:-4])
                            j_link_list.append(j_url)
                            j_pdf_list.append(j_pdf_indicator)
                            j_note_list.append(j_note)
                            
                            t=t+1
                else:
                    continue


    z=pd.DataFrame({'journal name':j_name_list,'journal_field':j_field_list,'submission link':j_link_list,'pdf or word':j_pdf_list,'note':j_note_list})
    z.to_csv('submissionlink.csv')

# Get the text for each submission website   
def get_text():
    

    Whole_data=pd.read_csv('submissionlink.csv')  
    Whole_data=Whole_data[Whole_data['note'].apply(lambda x:type(x)!=str)]
    #Sub_df are those with no hyperlink
    sub_df1=Whole_data[Whole_data['pdf or word']==False]
    sub_df2=Whole_data[Whole_data['pdf or word']==True]
    text_list=[]
    for i in range(len(sub_df1)):
        link=sub_df1['submission link'].iloc[i]
        response=requests.get(link,headers=fake_header)
        soup=BeautifulSoup(response.text,"html.parser")
        text=soup.get_text()
        text_list.append(text)
        print(text)
        time.sleep(5)
    sub_df1['text']=text_list
    
    text_list=[]
    for i in range(len(sub_df2)):
       journal=sub_df2['journal name'].iloc[i]
       
       with open ('.\guide txt\\'+journal+'.txt' ,encoding='unicode_escape') as f:
           text=(f.read())
           text_list.append(text)
    sub_df2['text']=text_list
    z=pd.concat([sub_df1,sub_df2])
    z.to_csv('instruction text.csv',index=False)









def get_word_count_and_journal_count(field="comm") : #1016 Update preregistr - > pre.?regist
    rep_word_ser=['reproduc','data.?avail','data.?shar','publication eth','replic',
                  'data.?deposit','reporting.?guidelin','data.?repositori','hack',
                  'raw.?data','open.?sci','reporting.?standard','availability of data',
                  'pre.?regist','open.?data','code.?avail','publicly accessible data','publication.?bia','archiving of data']

    rep_word_dict={}
    rep_jour_dict={}
    for i in range(len(rep_word_ser)):
        rep_pattern=rep_word_ser[i]    
        rep_word_dict[rep_pattern]=0    
        rep_jour_dict[rep_pattern]=0

    z=pd.read_csv('instruction text.csv')  
    # 11.2 Only select the communication field journals
    if(field=="comm"):
        z=z[z['journal_field']=='communication']
    elif(field=="all"):
        pass
    
    rep_word_count_list=[]
    reduced_form=["(colou?r|figure|copyright).{1,50}reproduc","reproduc.{1,50}(colou?r|figure|copyright)",
                  "\\\'view-replication-datasets\'\n\t","menu-name\':\'Replication Datasets\'",
                  "(colou?r|figure|copyright).{1,50}reproduc.{1,50}(colou?r|figure|copyright)"
                  ]
    for i in range(len(z)):
        text=z['text'].iloc[i]
        rep_word_count=0
        qual_word_count=0
        # Count how many 'replication' words 


        for pattern in rep_word_dict.keys():
            num_word=len(re.findall(pattern,text,re.I))           
            # Remove some misleading words
            
            
       
            # Remove some misleading words
            if(pattern=='reproduc'):
                for j in [0,1]:
                    num_word-=len(re.findall(reduced_form[j],text,re.I))
                for j in [4]:
                    num_word+=len(re.findall(reduced_form[j],text,re.I))
           
            elif(pattern=='replic'):
                for j in [2,3]:
                    num_word-=len(re.findall(reduced_form[j],text,re.I))

            
            rep_word_dict[pattern]+=num_word
            rep_word_count+=num_word  
            if(num_word>0):
                rep_jour_dict[pattern]+=1      


    S1=pd.Series(rep_word_dict)
    S2=pd.Series(rep_jour_dict)
    Word_df=pd.concat([S1,S2],axis=1,names=['word count','journal count'])
    Word_df=Word_df.rename(columns={0:'word count',1:'journal count'})
    '''
    in case you need to change the format
    Word_df=pd.read_csv('word count and journal count_comm.csv',index_col=0,encoding='utf-8-sig')   
    '''
    MEDIUM_SIZE=12
    fig=plt.figure()
    ax=fig.add_subplot(111)
    Word_df.sort_values(by='journal count',ascending=False).plot(kind='barh',figsize=[10,10],ax=ax)
                    #   title='Number of word mentions across all included journals (word count) and number of journals containing the word (journal count)')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
    plt.rc('font',size=MEDIUM_SIZE)
    plt.rc('xtick',labelsize=MEDIUM_SIZE)
    plt.rc('ytick',labelsize=MEDIUM_SIZE)
    #ax.set_title('Number of word mentions across all included journals (word count) and number of journals containing the word (journal count)',fontsize=16)
    if(field=="comm"):
    #plt.savefig('word count and journal count_comm.png')
        Word_df.to_csv('word count and journal count_comm.csv')
    elif(field=="all"):
        Word_df.to_csv('word count and journal count_allfields.csv')
def get_single_rep_word(count_number=True):
    pattern_list=['reproduc','replic','pre.?regist','data.?deposit']
    reduced_form=["(colou?r|figure|copyright).{1,50}reproduc","reproduc.{1,50}(colou?r|figure|copyright)",
                  "\\\'view-replication-datasets\'\n\t","menu-name\':\'Replication Datasets\'",
                  "(colou?r|figure|copyright).{1,50}reproduc.{1,50}(colou?r|figure|copyright)"
                  ]


    qual_word_list=['qualitative', 'interview', 'ethnography']
    z=pd.read_csv('instruction text.csv')
    plot_df={}
    plot_df_2={}
    for k in range(4):
        pattern=pattern_list[k]
        rep_word_count_list=[]
        qual_word_count_list=[]
        for i in range(len(z)):
            
            text=z['text'].iloc[i]
            rep_word_count=0
            qual_word_count=0
            
            num_word=len(re.findall(pattern,text,re.I))           
            # Remove some misleading words
            if(pattern=='reproduc'):
                for j in [0,1]:
                    num_word-=len(re.findall(reduced_form[j],text,re.I))
                for j in [4]:
                    num_word+=len(re.findall(reduced_form[j],text,re.I))
           
            elif(pattern=='replic'):
                for j in [2,3]:
                    num_word-=len(re.findall(reduced_form[j],text,re.I))
         
            rep_word_count+=num_word             
            rep_word_count_list.append(rep_word_count)
            
            
            
            for q_word in qual_word_list:           
                num_q_word=len(re.findall(q_word,text,re.I))
                qual_word_count+=num_q_word
            qual_word_count_list.append(qual_word_count)
            
            
        z[pattern+'_word_count']=rep_word_count_list  
        z['Q_word_count']=qual_word_count_list
        Opensci=z.drop(['text'],axis=1)
        Opensci['journal_field']=Opensci['journal_field'].apply(lambda x: re.sub('social ','',x))
    
        Opensci['Rep_word']=Opensci[pattern+'_word_count']>0
        Opensci['Qual_word']=Opensci['Q_word_count']>0
        
        g_b_field=Opensci.groupby(by='journal_field')
        Opensci_mean=g_b_field.mean()
        Opensci_std=g_b_field.std()

        R_word_perc=Opensci_mean[pattern+'_word_count']
        Q_word_perc=Opensci_mean['Qual_word']
        plot_df[k]=R_word_perc.drop('interdisciplinary')

        Opensci['qualitative']=Opensci['Q_word_count']>0
        g_b_qual=Opensci.groupby(by='qualitative')
        plot_df_2[k]=g_b_qual.mean()[pattern+'_word_count']
    




    plot_df_11={}
    for k in range(4):
        plot_df_11[k]=plot_df[k].to_frame()
        plot_df_11[k]['word']=pattern_list[k]
        plot_df_11[k]=plot_df_11[k].rename(columns={(pattern_list[k]+'_word_count'):'average number of times this phrase appeared in the journal'})
        plot_df_11[k]=plot_df_11[k].reset_index()
    
    final_plot_df=pd.concat([plot_df_11[2],plot_df_11[3]],ignore_index=True)
    final_plot_df=final_plot_df.rename(columns={'journal_field':'field'})
    final_plot_df.to_csv('final_plot.csv',encoding='utf-8-sig',index=False)

