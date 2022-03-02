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

# 하단의 코드로 100대 명산에 대한 정보를 저희들의 DB에 넣어주는 작업을 하게 됩니다. 한 번 씩만 작동시키면 되며, 4000개가 넘는 목록을 조회하므로 DB로 옮겨가기까지 많이 지연될 수 있습니다.

for item in items:

    all_mnt = list(db.mnt_info.find({}, {'_id': False}))
    mnt_no = (len(all_mnt) + 1)

    crtymd = item.find('crtymd').text
    mntiadd = item.find('mntiadd').text
    mntidetails = item.find('mntidetails').text
    mntihigh = item.find('mntihigh').text
    mntilistno = item.find('mntilistno').text
    mntiname = item.find('mntiname').text
    mntitop = item.find('mntitop').text
    mntiarea = mntiadd.split()

    request = requests.get(img_address + mntilistno, headers=headers)
    img = BeautifulSoup(request.text, 'html.parser')
    imgs = img.select('item')

    for i in imgs:
        mntiimg = (img_import + i.find('imgfilename').text)

    if mntitop != ' ':
        doc = {'mnt_no':mnt_no, # mnt_no : 자체적으로 기입한 산의 정보입니다. 1번부터 98번까지의 자료가 저장됩니다. openAPI의 정보 미표기 문제이니 DB에 리스트를 직접 추가해줘야 합니다.
               'mnt_name': mntiname, # mnt_name : 산의 이름을 저장합니다.
               'mnt_area': mntiarea[0], # mnt_area : 산의 소재지역(경상도, 서울특별시처럼)을 저장합니다.
               'mnt_address': mntiadd, # mnt_address : 산의 주소지를 저장합니다.
               'mnt_img':mntiimg, # mnt_img : 산의 이미지 정보가 담긴 주소를 저장합니다.
               'mnt_height':mntihigh, # mnt_height : 산의 높이입니다. 0으로 표기된 경우가 많아 쓰지 않는 것을 추천합니다. DB에서 직접 수정하는 방법도 있습니다.
               'mnt_desc':mntidetails, # mnt_desc : 산의 상세설명을 저장합니다.
               'mnt_crtymd':crtymd, # mnt_crtymd : 산의 정보에 대한 갱신일자를 저장합니다.
               'mnt_top':mntitop} # mnt_top : 100대 명산으로 선정된 이유를 설명합니다.
        mnt_no += 1
        db.mnt_info.insert_one(doc)