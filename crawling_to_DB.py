import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
# client = MongoClient('mongodb+srv://<id>:<pw>@cluster0.xkvvx.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#data = requests.get('http://apis.data.go.kr/1400000/service/cultureInfoService/mntInfoOpenAPI?ServiceKey=<KeyValue>&pageNo=1&examdate=2017-12-27&numOfRows=4704',headers=headers)
# 위 주소의 <KeyValue>에 키값을 입력해 주십시오.

soup = BeautifulSoup(data.text, 'html.parser')

items = soup.select('item')

img_address = 'http://apis.data.go.kr/1400000/service/cultureInfoService/mntInfoImgOpenAPI?serviceKey=X9EDkk%2FU5LjubctVnvGU3Nq3xjQ%2Byl6lcfP9Yk2DqGTEvZ%2F4UynHm5%2FoaMvzn9YIDyOkzvLPKuTixih8d1yNlg%3D%3D&mntiListNo='
img_import = 'http://www.forest.go.kr/images/data/down/mountain/'
mnt_no = 1

for item in items:
    crtymd = item.find('crtymd').text
    mntiadd = item.find('mntiadd').text
    mntidetails = item.find('mntidetails').text
    mntihigh = item.find('mntihigh').text # 산 높이는 0으로 표기된 경우가 많아 쓰지 않는 것을 추천합니다. DB에서 직접 수정하는 방법도 있습니다.
    mntilistno = item.find('mntilistno').text
    mntiname = item.find('mntiname').text
    mntitop = item.find('mntitop').text

    request = requests.get(img_address + mntilistno, headers=headers)
    img = BeautifulSoup(request.text, 'html.parser')
    imgs = img.select('item')

    for i in imgs:
        mntiimg = (img_import + i.find('imgfilename').text)

    if mntitop != ' ':
        doc = {'mnt_no':mnt_no, # OpenAPI의 명산 미표기로 인해 총 100개 중 98개의 명산만 등록돼 있습니다. 이 역시 DB에서 추가 기입이 가능합니다.
               'mnt_name': mntiname,
               'mnt_address': mntiadd,
               'mnt_img':mntiimg,
               'mnt_height':mntihigh,
               'mnt_desc':mntidetails,
               'mnt_crtymd':crtymd,
               'mnt_top':mntitop}
        mnt_no = (mnt_no + 1)
        db.mnt_info.insert_one(doc)