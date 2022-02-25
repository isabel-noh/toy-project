@app.route('/<address>', methods=['GET']) # <address> 로 검색할 지역의 데이터를 보냅니다.
def mnt_get():
   mnt_receive = request.args.get('mnt_give') # Ajax에서 mnt_give로 보낸 데이터를 받습니다.
   find_mnt = list(db.mnt_info.find({'mnt_area' : mnt_receive}, {'_id': False})) # 해당 지역의 산을 찾습니다.
   return jsonify({'mnt_list':find_mnt, 'msg': '검색완료!'}) # 검색된 자료들을 mnt_list로 프론트로 보냅니다.

# mnt_give로 보내는 데이터는 DB의 mnt_area로 분류된 지역명과 이름이 같아야 합니다.
# 예) '경기도', '강원도', '경상남도', '서울특별시' 등