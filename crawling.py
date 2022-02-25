from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
address_first = 'http://api.forest.go.kr/openapi/service/cultureInfoService/gdTrailInfoOpenAPI?serviceKey=9RucDw1Xmk16mCnCOBY3aAfQPMCnyS3sTP3v2tthlVw0CS9TZ6j64bTzDG1UEW9u%2BiY6X05TKK6OaYDR4HySog%3D%3D&searchArNm='
address_last = '&pageNo=1&numOfRows=100'
# address를 검색 키워드를 기준으로 쪼갭니다.
# 프론트에서 전달받은 키워드와 합쳐 주소를 만든 뒤, 데이터를 크롤링하여 프론트로 전달합니다.


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/mnt_info', methods=['GET'])
def mnt_info_get():
   areanm_receive = request.args.get('areanm_give') # Ajax에서 GET API의 형식으로 검색 키워드를 제공합니다.
   address = address_first + areanm_receive + address_last # 제공받은 키워드로 데이터를 제공합니다.
   data = requests.get(address, headers=headers)
   soup = BeautifulSoup(data.text, 'html.parser')
   items = soup.find_all('item')
   mnt_array = []

   for item in items:
      mntncd_list = item.find_next('mntncd').text
      aeatreason_list = item.find_next('aeatreason').text
      areanm_list = item.find_next('areanm').text
      details_list = item.find_next('details').text
      etccourse_list = item.find_next('etccourse').text
      mntheight_list = item.find_next('mntheight').text
      mntnm_list = item.find_next('mntnm').text
      overview_list = item.find_next('overview').text
      subnm_list = item.find_next('subnm').text
      # tourisminfo_list = item.find_next('tourisminfo').text # find_next 메소드가 작동하지 않으므로 xml을 살펴봐야 합니다.
      transport_list = item.find_next('transport').text
      doc = {'mntncd' : mntncd_list,
             'mntnm': mntnm_list,
             'subnm': subnm_list,
             'areanm': areanm_list,
             'mntheight': mntheight_list,
             'etccourse': etccourse_list,
             'aeatreason' : aeatreason_list,
             'details' : details_list,
             'overview' : overview_list,
             'transport' : transport_list }
      mnt_array.append(doc)

   return jsonify({'mnt_info':mnt_array, 'msg': '연결되었습니다.'}) # 리스트화 시킨 자료를 전달합니다.

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)