import urllib
import zlib
import json
from bs4 import BeautifulSoup
import logging

class datereader():
    def __init__(self, loctaion, keywords):
        self.loctaion = loctaion
        self.keywords = keywords
        self.__lista = []
        self.__listb = []
        self.proxy_handler = urllib.request.ProxyHandler({})

    # 获取indeed数据
    def readdata(self):
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')
        """"" if servlst["host"] != "":
            self.proxy_handler = urllib.request.ProxyHandler(
                {"http": "http://%(user)s:%(pass)s@%(host)s:%(port)d" % servlst})"""
        opener = urllib.request.build_opener(self.proxy_handler)
        urllib.request.install_opener(opener)
        my_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'BIGipServerjob_sjc=!EelkXEM53tKwzt6UCC+AfECqWukOeaaTnt4JPYghwnZroBUoHebecC51s9PXJHwfokhfyvrSaiZVx6A=; CTK=1bsnc9c0a1d780pp; ctkgen=1; JSESSIONID=86B901361B3274A1E0B927295FC99BD7.jasxA_sjc-job10; INDEED_CSRF_TOKEN=yu3dTBpMZaN94jfEyLRJg4LOwgligbNE; __guid=192154668.1704509127695318000.1508318163461.3208; NCR=1; _gali=fj; PREF="TM=1508318210314:L=Chicago"; RQ="q=test&l=Chicago&ts=1508318210319"; UD="LA=1508318210:CV=1508318210:TS=1508318210:SG=2af87c9ca2f63f79de185840be3966e5"; monitor_count=5; _ga=GA1.2.1389021004.1508318165; _gid=GA1.2.1541850656.1508318165',
            'Host': 'www.indeed.com',
            'Referer': 'https://www.indeed.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3408.400 QQBrowser/9.6.12028.400'}
        # temurl = str("https://www.indeed.com/" + urllib.parse.quote("jobs") + "?q=" + urllib.parse.quote(self.keywords) +
        #              "&l=" + urllib.parse.quote(self.loctaion) + "&ts=1506609441994&rq=1&fromage=last")
        temurl=str("https://www.indeed.com/q-"+urllib.parse.quote(self.keywords)+"-l-"+urllib.parse.quote(self.loctaion)+"-jobs.html")
        b = b'/:?='
        try:
            request = urllib.request.Request(temurl, headers=my_headers)
            yresponse = urllib.request.urlopen(request)
            yread = yresponse.read()
            rspheaders = yresponse.info()
            teampresult = ""
            if ('Content-Encoding' in rspheaders and rspheaders['Content-Encoding'] == 'gzip') or ('content-encoding' in rspheaders and rspheaders['content-encoding'] == 'gzip'):
                decompressed_data = zlib.decompress(yread, 16 + zlib.MAX_WBITS)
                ystr = decompressed_data.decode('utf8')
            else:
                ystr = yread.decode('utf8', 'ignore').encode('GB2312')
            soup = BeautifulSoup(ystr, 'html.parser')
            invalid_location_div = soup.find_all(
                'div', attrs={'class': 'invalid_location'}, limit=1)
            if invalid_location_div is not None and len(invalid_location_div) > 0:
                return invalid_location_div[0].text.replace("\n", "<br/>")
            else:
                bad_query_div = soup.find_all(
                    'div', attrs={'class': 'bad_query'}, limit=1)
                if bad_query_div is not None and len(bad_query_div) > 0:
                    return bad_query_div[0].text.replace("\n", "<br/>")
                else:
                    # 获取第一个节点内容
                    a_jobTitle = soup.find_all(
                        'a', attrs={'data-tn-element': 'jobTitle'})
                    # 获取所有job描述
                    if a_jobTitle is not None and len(a_jobTitle) > 0:
                        for aitem in a_jobTitle:
                            teampresult = teampresult + aitem.text + "<br/>"

                            div_name = aitem.parent.find_all(
                                'span', attrs={'class': 'company'}, limit=1)
                            if div_name is not None and len(div_name) > 0:
                                teampresult = teampresult + div_name[0].text
                            else:
                                div_name = aitem.parent.parent.find_all(
                                    'span', attrs={'class': 'company'}, limit=1)
                                if div_name is not None and len(div_name) > 0:
                                    teampresult = teampresult + div_name[0].text
                            div_location = aitem.parent.find_all(
                                'span', attrs={'class': 'location'}, limit=1)
                            if div_location is not None and len(div_location) > 0:
                                teampresult = teampresult + \
                                    "-" + div_location[0].text
                            else:
                                div_location = aitem.parent.parent.find_all(
                                    'span', attrs={'class': 'location'}, limit=1)
                                if div_location is not None and len(div_location) > 0:
                                    teampresult = teampresult + \
                                        "-" + div_location[0].text
                            teampresult = teampresult + "<br/>"
                            div_discrip = aitem.parent.find_all(
                                'span', attrs={'class': 'summary'}, limit=1)
                            if div_discrip is not None and len(div_discrip) > 0:
                                teampresult = teampresult + \
                                    div_discrip[0].text + "<br/>"
                            else:
                                div_discrip = aitem.parent.parent.find_all(
                                    'span', attrs={'class': 'summary'}, limit=1)
                                if div_discrip is not None and len(div_discrip) > 0:
                                    teampresult = teampresult + \
                                        div_discrip[0].text + "<br/>"
                            teampresult = teampresult + "<br /><br />"
                            teampresult = teampresult + "<hr />"
                        return teampresult
                    else:
                        return teampresult
        except Exception as err:
            logging.error(err.reason)
            return "net error"
       

    # glassdoor站点根据位置获取locationId
    def readlocid(self):
        """"" if servlst["host"] != "":
            self.proxy_handler = urllib.request.ProxyHandler(
                {"http": "http://%(user)s:%(pass)s@%(host)s:%(port)d" % servlst})"""
        opener = urllib.request.build_opener(self.proxy_handler)
        urllib.request.install_opener(opener)
        my_headers = {
            'authority': 'www.glassdoor.com ',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, sdch, br',
            'accept-language': 'zh-CN,zh;q=0.8',
            'Cookie': 'trs=direct:direct:direct:2017-09-23+20%3A38%3A50.757:undefined:undefined; ARPNTS_AB=790; __qca=P0-1236245687-1506224996121; uc=8F0D0CFA50133D96DAB3D34ABA1B873324E3F5DA1D1CA8D53F7CDB15E0E972C88D8AF602813C5C4B348C3B29B3D04FF6325FD44230E522ACB46583BD23C57828C2FBC611438D6AC5EADA5958631E5766560ECF96BB9E0E1FAD47A374747D57367132A826024F7838F5DC9EF2C2FB8E598ED15531EE8C8BE5785D2F986D552DE68F6EFE586167296FD796FE79C9B653DD8F21A9CC698B2D9E; JSESSIONID=3AD5E29AF6B3E58C6D57173093068C09; GSESSIONID=3AD5E29AF6B3E58C6D57173093068C09; cass=1; gdId=82613111-63b0-4ccc-8171-cceb6625dcc6; ARPNTS=3915753664.64288.0000; _ga=GA1.2.1196569190.1506224791; _gid=GA1.2.1054940114.1507317666',
            'Referer': 'https://www.glassdoor.com/',
            'x-requested-with': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3408.400 QQBrowser/9.6.12028.400'}
        temurl = str("https://www.glassdoor.com/findPopularLocationAjax.htm?term=" +
                     urllib.parse.quote(self.loctaion) + "&maxLocationsToReturn=10")
        b = b'/:?='
        try:
            request = urllib.request.Request(temurl, headers=my_headers)
            yresponse = urllib.request.urlopen(request)
            yread = yresponse.read()
            rspheaders = yresponse.info()
            teampresult = ""
            if ('Content-Encoding' in rspheaders and rspheaders['Content-Encoding'] == 'gzip') or ('content-encoding' in rspheaders and rspheaders['content-encoding'] == 'gzip'):
                decompressed_data = zlib.decompress(yread, 16 + zlib.MAX_WBITS)
                ystr = decompressed_data.decode('utf8')
            else:
                ystr = yread.decode('utf8', 'ignore').encode('GB2312')
            if(ystr == ""):
                return "-1"
            else:
                hjson = json.loads(ystr)
            
                if len(hjson)>0:
                    tempid=hjson[0]['locationId']
                    return tempid
                else:
                    return "-1"
        except Exception as identi:
               logging.error(identi.reason)
               return "-1"


    # 获取indeed数据
    def readgadata(self):

        """"" if servlst["host"] != "":
            self.proxy_handler = urllib.request.ProxyHandler(
                {"http": "http://%(user)s:%(pass)s@%(host)s:%(port)d" % servlst})"""
        opener = urllib.request.build_opener(self.proxy_handler)
        locationId = self.readlocid()
        urllib.request.install_opener(opener)
        my_headers = {
            'authority': 'www.glassdoor.com ',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, sdch, br',
            'accept-language': 'zh-CN,zh;q=0.8',
            'Cookie': 'trs=direct:direct:direct:2017-09-23+20%3A38%3A50.757:undefined:undefined; ARPNTS_AB=790; __qca=P0-1236245687-1506224996121; uc=8F0D0CFA50133D96DAB3D34ABA1B873324E3F5DA1D1CA8D53F7CDB15E0E972C88D8AF602813C5C4B348C3B29B3D04FF6325FD44230E522ACB46583BD23C57828C2FBC611438D6AC5EADA5958631E5766560ECF96BB9E0E1FAD47A374747D57367132A826024F7838F5DC9EF2C2FB8E598ED15531EE8C8BE5785D2F986D552DE68F6EFE586167296FD796FE79C9B653DD8F21A9CC698B2D9E; JSESSIONID=3AD5E29AF6B3E58C6D57173093068C09; _ga=GA1.2.1196569190.1506224791; _gid=GA1.2.1054940114.1507317666; GSESSIONID=3AD5E29AF6B3E58C6D57173093068C09; cass=1; gdId=82613111-63b0-4ccc-8171-cceb6625dcc6; ARPNTS=3915753664.64288.0000',
            'Referer': 'https://www.glassdoor.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3408.400 QQBrowser/9.6.12028.400'}
        temurl = str("https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" +
                     urllib.parse.quote(self.keywords) + "&sc.keyword=" + urllib.parse.quote(self.keywords) + "&locT=C&locId=" + str(locationId) + "&jobType=")
        b = b'/:?='
        try:
            request = urllib.request.Request(temurl, headers=my_headers)
            yresponse = urllib.request.urlopen(request)
            yread = yresponse.read()
            rspheaders = yresponse.info()
            teampresult = ""
            if ('Content-Encoding' in rspheaders and rspheaders['Content-Encoding'] == 'gzip') or ('content-encoding' in rspheaders and rspheaders['content-encoding'] == 'gzip'):
                decompressed_data = zlib.decompress(yread, 16 + zlib.MAX_WBITS)
                ystr = decompressed_data.decode('utf8')
            else:
                ystr = yread.decode('utf8', 'ignore').encode('GB2312')
            soup = BeautifulSoup(ystr, 'html.parser')
            invalid_location_div = soup.find_all(
                'div', attrs={'class': 'noResults padVert'}, limit=1)
            if invalid_location_div is not None and len(invalid_location_div) > 0:
                return invalid_location_div[0].text.replace("\n", "<br/>")
            else:
                # 获取第一个节点内容
                a_jobTitle = soup.find_all('ul', attrs={'class': 'jlGrid hover'})
                # 获取所有job描述
                if a_jobTitle is not None and len(a_jobTitle) > 0:
                    for aitem in a_jobTitle[0].children:
                        teampresult=teampresult+aitem.text.replace("Glassdoor est.","").replace("Glassdoor","")
                        teampresult = teampresult + "<br /><br />"
                        teampresult = teampresult + "<hr />"
                    return teampresult
                else:
                    return teampresult
        except Exception as identifier:
            logging.error(identifier.reason)
            return "net error"
        
