# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 23:56:15 2016

@author: wangd_000
"""

import sqlite3
from nltk.tokenize import sent_tokenize
from nltk.tokenize import TreebankWordTokenizer
#from nltk.tokenize import PunktWordTokenizer
from nltk.corpus import stopwords
import re
from collections import Counter

from datetime import datetime

#update stopset
stopset = set(stopwords.words('english'))
stopset.update(['ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii','xiii',
                'xiv','xv','xvi','xvii','xviii','xix','xx'])
stopset.update(['','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
                'q','r','s','t','u','v','w','x','y','z'])

#database infor
db_file='SEC_db.db'
table1='sec_infor'
out_put_file='SEC_out_put.db'
table2='words_date'
table3='words_value'


#connect to database and execute sql scheme
def sql_execute(db_name,sql_scheme):
    conn=sqlite3.connect(db_name)
    cursor = conn.cursor()
    r=cursor.execute(sql_scheme)
    conn.commit()
    conn.close()
    return r
    
#select all from database by year
def select_by_year(db_name,table_name,year):
    sql_base="SELECT * FROM {} WHERE date LIKE '%{}'"
    sql=sql_base.format(table_name, year)
    try:
        conn=sqlite3.connect(db_name)
        cursor = conn.cursor()
        r=cursor.execute(sql).fetchall()
        return r
    except Exception as e:
        print('something wrong:',e)
        
#insert to database
def insert_data(out_put_db, out_put_table, words_list):
    try:    
        words_len=len(words_list)        
        con = sqlite3.connect(out_put_db)
        cursor = con.cursor()
        sql_base="""INSERT INTO {} (date, word, source, times)
            VALUES
                (:date, :word, :source, :times)""".format(out_put_table)
        cursor.executemany(sql_base, words_list)
        con.commit()
        cursor.close()        
        con.close()
        e= words_len + "words inserted"
        return e 
    except Exception as e:
        return e

#get the title list from data base by year
def get_title_list(db_name, table_name, year):
    raw_r=select_by_year(db_name, table_name, year)
    title_l=[]
    i=0
    while i <=(len(raw_r)-1):
        title_dict={}
        title_dict['date']=raw_r[i][0]
        title_dict['title']=raw_r[i][2]
        title_l.append(title_dict)
        i+=1
#    for t in raw_r:
#        title_dict={}
#        title_dict['date']=t[0]
#        title_dict['title']=t[2]
#        title_l.append(title_dict)
    return title_l
    
#get the article list from data base by year
def get_article_list(db_name, table_name, year):
    raw_r=select_by_year(db_name, table_name, year)
    article_l=[]
    i=0
    while i <=(len(raw_r)-1):
        article_dict={}
        article_dict['date']=raw_r[i][0]
        article_dict['article']=raw_r[i][6]
        article_l.append(article_dict)
        i+=1
    return article_l


#create none repeated dict from target list
#return including the repeate times and date
def create_none_repeate(target_list):
    counts = Counter(target_list)
    result_d={}
    for w in counts:
        item={w:{'word':w, 'times':str(counts[w])}}
        result_d.update(item)
    return result_d
#    i=0
#    while i < len(counts):
#        word=target_list[i]
#        if word in check_l:
#            result_d[word].update(result_d[word]+=1)
#        else:
#            item={word:1}
#            result_d.update(item)
#            check_l.update(word)
            
#        if not word in check_l:
#            item={word:{'word':word, 'times':1}}
#            result_d.update(item)
#            check_l.update(word)
#        else:
#            print('word:',word,' repeated')
#            result_d[word]['times']+=1
#        i+=1
#    return result_d

#Change date format form 'Apr 1, 2011' or 'Apr.1, 2011' to '4/1/2011'
def date_format(date):
    if 'March' in date:
        date1=date.replace('March','Mar')
    elif 'April' in date:
        date1=date.replace('April','Apr')
    elif 'June' in date:
        date1=date.replace('June','Jun')
    elif 'July' in date:
        date1=date.replace('July','Jul')
    elif 'Sept' in date:
        date1=date.replace('Sept','Sep')
    else:
        date1=date
        
    if '.' in date1:
        date_object = datetime.strptime(date1, '%b. %d, %Y')   
    else:
        date_object = datetime.strptime(date1, '%b %d, %Y')
    newformat = date_object.strftime('%m/%d/%Y')
    return newformat
    
       
#title after tokenizer, low(),remove non-letters, stopwords, 
def title_words(title_text):
    words1=TreebankWordTokenizer().tokenize(title_text)
    words2=[]
    for w in words1:
        w2=re.sub("[^a-zA-Z]", "", w)
        words2.append(w2.lower())
    words3=[x for x in words2 if not x in stopset]
    
    return words3

# main funciton of title
def title_main(year):  
    titles=get_title_list(db_file,table1, year)
    for t in titles:
        date=date_format(t['date'])
        words_in_title=title_words(t['title'])
        none_repeate_words_d=create_none_repeate(words_in_title)
        words_l=[]
        for w in none_repeate_words_d:
            w_dict={'date':date,
                    'word':none_repeate_words_d[w]['word'],
                    'source':'Title',
                    'times':none_repeate_words_d[w]['times']}
            words_l.append(w_dict)
        result=insert_data(out_put_file, table2, words_l)
        print(result)
        #return words_l

#article after tokenizer, low(),remove non-letters, stopwords, 
def article_words(article_text):
    sents=sent_tokenize(article_text)
    http_head=set(['http','https','html','htm','www','.gov'])
    i=0
    words4=[]
    while i < len(sents):
        sent=sents[i]
        flag=True
        for ht in http_head:
            if ht in sent:
                flag=False                
                break
            else:
                flag=True
        if flag:
            words1=TreebankWordTokenizer().tokenize(sent)
            words2=[]
            for w in words1:
                w2=re.sub("[^a-zA-Z]", "", w)
                words2.append(w2.lower())
            words3=[x for x in words2 if not x in stopset]
            words4+=words3
        else:
            pass
        i+=1
    return words4
    
# main funciton of article
def article_main(year):  
    articles=get_article_list(db_file,table1, year)
    for t in articles:
        date=date_format(t['date'])
        if t['article']:
            words_in_article=article_words(t['article'])
            none_repeate_words_d=create_none_repeate(words_in_article)
            words_l=[]
            for w in none_repeate_words_d:
                w_dict={'date':date,
                        'word':none_repeate_words_d[w]['word'],
                        'source':'Content',
                        'times':none_repeate_words_d[w]['times']}
                words_l.append(w_dict)
            result=insert_data(out_put_file, table2, words_l)
            print(result)
        else:
            pass


        
            
    
    
    
    
