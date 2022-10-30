from time import sleep
from wsgiref import headers

import tornado.ioloop
import tornado.web
import requests
import json
from bs4 import BeautifulSoup
ratingc = {
    2100: "真传拾段",
    2090: "真传玖段",
    2180: "真传捌段",
    2070: "真传柒段",
    2060: "真传陆段",
    2050: "真传伍段",
    2040: "真传肆段",
    2030: "真传叁段",
    2020: "真传贰段",
    2010: "真传壹段",
    2000: "真传",
    1950: "十段",
    1900: "九段",
    1850: "八段",
    1800: "七段",
    1700: "六段",
    1600: "五段",
    1500: "四段",
    1400: "三段",
    1200: "二段",
    1000: "初段",
    750: "修行中",
    500: "初出茅庐",
    250: "实习生",
    0: "初学者"
}
headerc = {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63070517)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}


def GetDetails(c):
    Page_O = BeautifulSoup(c, 'html.parser')
    time = Page_O.find_all('span', attrs={"class": "v_b"})[1].get_text()
    diffc = Page_O.find_all('img', attrs={"class": "playlog_diff v_b"})[
        0].get('src').split('/')[-1].split('.')[0].split('_')[1]
    typec = Page_O.find_all('img', attrs={"class": "playlog_music_kind_icon"})[
        0].get('src').split('/')[-1].split('.')[0].split('_')
    if (typec[1] == "standard"):
        typec = "SD"
    else:
        typec = "DX"
    title = Page_O.find_all(
        'div', attrs={"class": "basic_block m_5 p_5 p_l_10 f_13 break"})[0].get_text()
    achievement = Page_O.find_all(
        'div', attrs={"class": "playlog_achievement_txt t_r"})[0].get_text()
    dx_score = Page_O.find_all('div', attrs={"class": "white p_r_5 f_15 f_r"})[
        0].get_text()
    Stc = RecordStatus(Page_O.find_all('img', attrs={"class": "h_35 m_5 f_l"}))
    FLstat = Page_O.find_all('div', attrs={"class": "p_t_5"})
    Ratings = Page_O.find_all(
        'div', attrs={"class": "playlog_rating_val_block"})
    Fsfc = Page_O.find_all('div', attrs={"class": "f_r f_14 white"})
    TAPStat = RecordStat(Page_O.find_all('table', attrs={
                         "class": "playlog_notes_detail t_r f_l f_11 f_b"})[0].find_all('tr')[1:6])
    vsstatus = len(Page_O.find_all('img', attrs={"class": "playlog_vs v_b"}))
    rank = "1st"
    ppidlevel = '-'
    ppid = '-'
    fsd = ['-', '-']
    try:
        fsd = Fsfc[1].get_text().split('/')
        rank = Page_O.find_all('img', attrs={"class": "h_35 m_5 f_r"})[
            0].get('src').split('/')[-1].split('.')[0]
        ppid = Page_O.find_all('div', attrs={"class": "basic_block p_3 t_c f_11"})[
            0].get_text()
        ppidlevel = Page_O.find_all('div', attrs={"id": "matching"})
        cd = ppidlevel[0].find_all('img', attrs={"class": "h_16"})
        ppidlevel = cd[0].get('src').split(
            '/')[-1].split('.')[0].split('_')[1].upper()
    except Exception:
        rank = "N/A"
        fsd = ['-', '-']
    ResList = []
    ResList.append(time)
    if (',' in title):
        ResList.append('"' + title + '"')
    else:
        ResList.append(title)

    jsonid = 000
    jsonlevel = 15
    diffc = diffc.upper()
    if diffc == "REMASTER":
        diffc = "Re:MASTER"
    with open("cmp.json", 'r') as jsondata:
        oc = json.loads(jsondata.read())
        jsonid = oc[typec][title]["id"]
        levelid = 0
        if diffc[0] == 'A':
            levelid = 1
        if diffc[0] == 'E':
            levelid == 2
        if diffc[0] == 'M':
            levelid = 3
        if diffc[0] == 'R':
            levelid = 4
        jsonlevel = oc[typec][title]["level"][levelid]
    ResList.append(jsonid)  # id

    ResList.append(diffc.upper())

    ResList.append(jsonlevel)  # level
    ResList.append(typec)
    ResList.append(achievement)
    ResList.append(dx_score.replace(',', ''))
    for i in Stc:
        ResList.append(i)
    ResList.append(rank)
    if vsstatus == 0:
        ResList.append("否")
    else:
        ResList.append("是")
    ResList.append("否")
    ResList.append(ratingc[int(Ratings[0].get_text())])
    ResList.append(Ratings[0].get_text())
    ResList.append(Ratings[1].get_text())
    ResList.append(
        str(int(Ratings[0].get_text()) + int(Ratings[1].get_text())))
    ResList.append('3')
    ResList.append(FLstat[0].get_text())
    ResList.append(FLstat[1].get_text())
    fcd = Fsfc[0].get_text().split('/')
    ResList.append(fcd[0])
    ResList.append(fcd[1])
    ResList.append(fsd[0])
    ResList.append(fsd[1])
    ResList.append(ppid)
    if ppidlevel == "REMASTER":
        ppidlevel = "Re:MASTER"
    ResList.append(ppidlevel)
    for i in TAPStat:
        if (i != '\u3000' and i != ''):
            ResList.append(i)
        else:
            ResList.append('0')
    res = ','.join(ResList)
    return res


def RecordStatus(Stc):
    Status = [
        "N/A",
        "N/A"
    ]
    for i in Stc:
        StatusPng = i.get('src').split('/')[-1].split('.')[0]
        if ("dummy" in StatusPng):
            return Status
        if ("fc" in StatusPng or "ap" in StatusPng):
            Status[0] = "FC"
            if ("ap" in StatusPng):
                Status[0] = "AP"
            if ("plus") in StatusPng:
                Status[0] = Status[0]+'+'
        if ("fs" in StatusPng):
            Status[1] = "FS"
            if ("fsd" in StatusPng):
                Status[1] = "FSD"
            if ("plus") in StatusPng:
                Status[1] = Status[1]+'+'
    return Status


def RecordStat(Tablec):
    ResList = []
    for i in Tablec:
        TmpList = []
        c = i.find_all('td')
        for ii in c:
            ResList.append(ii.get_text())
    return ResList


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write(self.request.uri)
        rc = requests.session()
        rc.headers = headerc
        rec = rc.get(self.request.uri.replace("http", "https"))
        for i in range(5):
            sleep(0.2)
            Netx = rc.get(
                "https://maimai.wahlap.com/maimai-mobile/record/musicGenre/search/?genre=99&diff={}".format(i))
            with open("indexc{}".format(i), "w") as c:
                c.write(Netx.content.decode("utf8"))

        Netx = rc.get(
            "https://maimai.wahlap.com/maimai-mobile/record/".format(i))
        Page_O = BeautifulSoup(Netx.content.decode('utf8'), 'html.parser')
        res = Page_O.find_all('input', attrs={"name": "idx"})
        ResList = []
        for i in res:
            print(i.get("value"))
            cc = rc.get("https://maimai.wahlap.com/maimai-mobile/record/playlogDetail/?idx={}".format(
                i.get("value"))).content.decode('utf8')
            with open("last_Detailspage", "w") as f:
                f.write(cc)
            ResList.append(GetDetails(cc))
            sleep(0.16)

        self.write('<html><body><pre>')

        for i in reversed(ResList):
            self.write(i)
            self.write('\n')
        self.write('</pre></body></html>')


class RedirectHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect(
            "http://tgk-wcaime.wahlap.com/wc_auth/oauth/authorize/maimai-dx")


class Authorizehandler(tornado.web.RequestHandler):
    def get(self):
        resc = requests.get("https://tgk-wcaime.wahlap.com/wc_auth/oauth/authorize/maimai-dx",
                            headers=headerc, allow_redirects=False)
        wxauthurl = resc.headers.get("Location").replace("https", "http")
        print(wxauthurl)
        self.redirect(wxauthurl)


def make_app():
    return tornado.web.Application([
        (r"http://cx.wahlap.com/*", RedirectHandler),
        (r"/", RedirectHandler),
        (r"http://p.hama.icu/", RedirectHandler),
        (r"http://tgk-wcaime.wahlap.com/wc_auth/oauth/authorize/maimai-dx", Authorizehandler),
        (r"http://tgk-wcaime.wahlap.com/wc_auth/oauth/callback/maimai-dx", MainHandler)
    ])


def updateSongList():
    print("Updating Music_Data")
    musicData = requests.get(
        "https://www.diving-fish.com/api/maimaidxprober/music_data")
    c = json.loads(musicData.content)
    DataList = {
        "SD": {},
        "DX": {}

    }
    for i in c:
        music_info = {
            'id': i['id'],
            "level": i['level']
        }
        DataList[i['type']][i['title']] = music_info
    with open("cmp.json", 'w') as f:
        f.write(json.dumps(DataList))
    print("Done")


if __name__ == "__main__":
    updateSongList()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
