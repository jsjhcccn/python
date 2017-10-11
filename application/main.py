import urllib
from flask import Flask, jsonify, render_template, request, g
from toolunit.datereader import datereader
from toolunit.proxyreader import proxyreader
import random

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
    else:
        outputstrleft = readgadata
        outputstrright = readdata
    return render_template('index.html', leftcon=outputstrleft, rightcon=outputstrright, location=locationva, keywords=keywordsva)


if __name__ == '__main__':

    app.run()
