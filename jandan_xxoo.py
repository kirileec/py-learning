#-*-coding:utf-8-*-
import urllib.request

import http.cookiejar
import socket,os
from bs4 import BeautifulSoup
import random
import re
import time

targetDir = r"D:\ooxx"

#socket.setdefaulttimeout(2)

#自定义opener
def makeMyOpener():
    cookie_support = urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
    #proxy_support = urllib.request.ProxyHandler({"http":"115.159.50.56:8080"})
    opener = urllib.request.build_opener(cookie_support,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    user_agents = [
		'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11','Opera/9.25 (Windows NT 5.1; U; en)',
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
		'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
		'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
		'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
		'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
		'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
		'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
		'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
		'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999',
		'Baiduspider+(+http://www.baidu.com/search/spider.htm)',
		'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
		'Sogou web spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07)',
		'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/)',
		]
    agent = random.choice(user_agents)
    opener.addheaders = [("User-agent",agent),("Accept","*/*"),('Referer','http://www.baidu.com'),('Host','http://jandan.net')]
    return opener

def getfilename(url): # url获得文件名
    pos = url.rindex('/')
    return url[pos+1:]

def get_allimgs_curpage(page,vote):  # 在页面中找符合条件的Comment
    soup = BeautifulSoup(page, "html.parser")
    data=[]
    comments = soup.find_all("div", class_="text") #找到所有帖子
    for comment in comments:
        commentids = comment.find_all("span",class_="righttext")
        for commentid in commentids:
            href = commentid.a.get("href")
            idloc=href.find("comment-")+8
            loc = href.find("\"")
            id=href[idloc:loc]  #取得ID
            #<span id="cos_support-3121207">0</span>
            pattern= "cos_support-"+str(id)  #OO支持
            votes = comment.find_all("div",class_="vote")
            for vote1 in votes:
                vote2=vote1.find_all("span")
                for vote3 in vote2:
                    re1 = re.compile(pattern)
                    if  re1.search(vote3.decode()):
                        if int(vote3.string)>vote:
                            imgs=comment.find_all("img")
                            for img in imgs:
                                data.append(img.get("src"))
    return  data

def open_url(url):
    try:
        opener = makeMyOpener()
        urlop = opener.open(url)
        page = urlop.read().decode('utf-8')
        urlop.close()
    except urllib.request.URLError as e:
        print(e.code)
    return page

def download_img(url,overwrite=False):
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    try:
        filepath = targetDir + "\\" + getfilename(url)

        if not os.path.exists(filepath):
            f = open(filepath, 'wb')
            opener = makeMyOpener()
            urlop = opener.open(url)
            f.write(urlop.read())
            f.close()
            urlop.close()
            print("下载成功:" + url)
        else:
            if overwrite:
                f = open(filepath, 'wb')
                opener = makeMyOpener()
                urlop = opener.open(url)
                f.write(urlop.read())
                f.close()
                urlop.close()
                print("下载成功:" + url +"--覆盖旧文件")
            else:
                print("下载成功:"+ url +"--文件已存在")
    except urllib.request.URLError as e:
        print(e.code)

def get_img(start=1949, end=1959,oo_higher_than=40):
    for i in range(start, end+1):
        print("--解析第"+str(i)+"页中--")
        url = 'http://jandan.net/ooxx/page-' + str(i) + '#comments'
        page = open_url(url)
        data = get_allimgs_curpage(page, oo_higher_than)
        print("--解析完成，开始下载--")
        if len(data)==0:
            print("当前页没有符合条件的图片")
            print("--下载第" + str(i) + "页完成--")
            continue
        for imgurl in data:
            time.sleep(0.5)
            download_img(imgurl,True)
        print("--下载第"+str(i)+"页完成--")


def getnewestpage():
    url = 'http://jandan.net/ooxx'
    page = open_url(url)
    soup = BeautifulSoup(page,'html.parser')
    newestpage = soup.find("span",class_="current-comment-page")
    if newestpage:
        str1 = newestpage.string
        return int(str1[1:len(str1)-1])

if __name__ == "__main__":
    # get_img()
    vote = input("请输入需要下载的图片的OO数大于的值(默认40)：")
    if not vote:
        vote= 40
    start = input("请输入起始页(最小1500 因旧存档没了,默认为最新页-1):")

    if not start:
        start = getnewestpage() - 1
    if int(start) < 1500:
        start = 1500
    end = input("请输入结束页:")
    if not end:
        end = getnewestpage()
    input("您选择了寻找从第"+str(start)+"页到第"+str(end)+"页中支持数大于"+str(vote)+"的图片，按下回车开始")
    get_img(int(start), int(end), int(vote))
