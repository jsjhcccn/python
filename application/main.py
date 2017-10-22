import urllib
from flask import Flask, jsonify, render_template, request, g
from toolunit.datareader import datareader
from toolunit.proxyreader import proxyreader
import random
from entity.searchrecoder import dbcall
import datetime
app = Flask(__name__)
servlst = proxyreader()
app.add_template_global(servlst, 'servlst')
def get_servlst():#获取全局变量
    return servlst

@app.route('/')
def index():
    servlst=get_servlst()
    tempserver=servlst.getProxyClientConfig()
    location = request.args.get('l', "", type=str)
    keywords = request.args.get('k', "", type=str)
    locationva = str(urllib.parse.unquote(location))
    keywordsva = str(urllib.parse.unquote(keywords))
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
        proxyrd = datareader(locationva, keywordsva,tempserver)
        proxyrd.preget()
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
    return render_template('index.html', leftcon=outputstrleft, rightcon=outputstrright, location=str(locationva), keywords=str(keywordsva),leftsite=leftsite,rightsite=rightsite)

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

@app.route('/sample')    
def sample():
     return render_template('sample.html')

if __name__ == '__main__':

    app.run()
