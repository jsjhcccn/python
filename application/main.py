import urllib
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, jsonify, render_template, request, g
from toolunit.datereader import datereader
from toolunit.proxyreader import proxyreader
import random
from entity.searchrecoder import dbcall
import datetime
app = Flask(__name__)

#servlst = proxyreader().getProxyClientConfig()


@app.route('/')
def index():
    location = request.args.get('l', "", type=str)
    keywords = request.args.get('k', "", type=str)
    locationva = urllib.parse.unquote(location)
    keywordsva = urllib.parse.unquote(keywords)
    readgadata = ""
    readdata = ""
    outputstrleft = ""
    outputstrright = ""
    leftsite=""
    rightsite=""
    if(locationva == "" and keywordsva == ""):
        readdata = ""
        readgadata = ""
    else:
        proxyrd = datereader(locationva, keywordsva)
        readdata = proxyrd.readdata()
        readgadata = proxyrd.readgadata()
    rdindex = random.randint(0, 1)
    if rdindex == 0:
        outputstrleft = readdata
        outputstrright = readgadata
        leftsite="indeed"
        rightsite="glassdoor"
    else:
        outputstrleft = readgadata
        outputstrright = readdata
        leftsite="glassdoor"
        rightsite="indeed"
    return render_template('index.html', leftcon=outputstrleft, rightcon=outputstrright, location=locationva, keywords=keywordsva,leftsite=leftsite,rightsite=rightsite)

@app.route('/recommend', methods=['POST'])
def recommend():
    keywords= request.form.get('key')
    loc= request.form.get('loc')
    comment= request.form.get('comment')
    sitename= request.form.get('sitename')
    #(reqloc, reqkeywds,remark,recommendsite,addTime):
    searchrd=dbcall(loc,keywords,comment,sitename)
    searchrd.save()
    return sitename


if __name__ == '__main__':

    app.run()
