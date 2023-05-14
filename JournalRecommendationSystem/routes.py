from flask import render_template,url_for,flash,redirect,request
from JournalRecommendationSystem import app
from JournalRecommendationSystem.forms import AddArticlesManuallyForm, SearchForm

import os
from rank_bm25 import BM25Okapi
import pandas as pd

from whoosh.qparser import QueryParser
from whoosh.query import *
from whoosh import index 
import os

from whoosh.qparser import MultifieldParser,OrGroup
from whoosh.fields import *
import time


class search_query_BM25():
    def __init__(self,title_new='',abstract_new='',keywords_new=''):
        
        self.title_new = title_new
        self.abstract_new = abstract_new
        self.keywords_new = keywords_new
    
        self.tokenized_query = self.title_new+self.abstract_new+self.keywords_new

    def Search(self):
        a=time.time()
        ix = index.open_dir(os.getcwd()+"\\JournalRecommendationSystem\\indexdir")
        searcher = ix.searcher()
        lst = []
        new_lst = []
        check =[]
        with ix.searcher() as searcher:
            query = MultifieldParser(["Title","Abstract"], ix.schema, group=OrGroup).parse(u(self.tokenized_query))
            results = searcher.search(query, terms=True, limit=24)
            #print(len(results))
            
            for r in results:
                lst.append([r["Source_title"], r['Publisher'],r['Queue_Ranking'], r.score])
        #print(len(lst))
        for i in range(len(lst)):
            if lst[i][0] not in check:
                if lst[i][1] not in check:
                    new_lst.append(lst[i])
                    check.append(lst[i][0])
                    check.append(lst[i][1])

        b= time.time()
        c = b-a
        #print(len(new_lst))
        new_lst.append(round(c,3))
        return new_lst


@app.route("/", methods=['GET', 'POST'])
@app.route("/home/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        bm25 = search_query_BM25(form.Search.data)
        data=bm25.Search()
        if len(data)==1:
            flash('In valid Input', 'danger')
            return redirect(url_for('home'))
        return render_template('Recommendation.html',data=data)
    return render_template('home.html',form=form)



@app.route("/AddArticlesManually/", methods=['GET', 'POST'])
def AddArticlesManually():
    form = AddArticlesManuallyForm()
    if form.validate_on_submit():
        bm25 = search_query_BM25(str(form.Papertitle.data),str(form.Abstract.data),str(form.Keywords.data))
        data=bm25.Search()
        if len(data)==1:
            flash('In valid Input', 'danger')
            return redirect(url_for('AddArticlesManually'))
        #print(data)
        return render_template('Recommendation.html',data=data)
    return render_template('AddArticlesManually.html',form=form)
    

@app.route("/Recommendation/")
def Recommendation():
    return render_template('Recommendation.html')