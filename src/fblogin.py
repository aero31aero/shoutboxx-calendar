import requests
import urllib.request, http.cookiejar, re, os, sys
from lxml import html

class Facebook():
    def __init__(self, email, password):
        self.email = email
        self.password = password

        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.addheaders = [('Referer', 'http://login.facebook.com/login.php'),
                            ('Content-Type', 'application/x-www-form-urlencoded'),
                            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')]
        self.opener = opener

    def login(self):
        url = 'https://login.facebook.com/login.php?login_attempt=1'
        data = "locale=en_US&non_com_login=&email="+self.email+"&pass="+self.password+"&lsd=20TOl"
        usock = self.opener.open('http://www.facebook.com')
        usock = self.opener.open(url, data.encode())
        usock = self.opener.open('https://developers.facebook.com/tools/explorer/')
        self.page = usock.read()
        htmlExtract = str(usock.read())
        

    def getToken(self):
        count=0
        find="accessToken"
        for z in re.finditer(find,self.page):
            count+=1
            if(count==2):
                mark=z.start()

        htmlMod=htmlExtract[mark+14:]
        token=None
        for a in htmlMod:
            if(a=='"'):
                break
            else:
                token=a
                return token;
        return token