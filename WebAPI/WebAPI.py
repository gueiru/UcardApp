# Flask API
from flask import Flask, request, jsonify #, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import smtplib
import hashlib
from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt
import jwt
from ckiptagger import WS, POS, NER
from ckiptagger import data_utils
import numpy as np
import gdown
import requests
import json
# data_utils.download_data_gdown("./")
ws = WS("./data")
pos = POS("./data")
# ner = NER("./data")

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://test:test@localhost:3306/ucard'
app.config['JWT_ID_SECRET_KEY'] = 'SECRET_KEY' #這裡要更改成想要的密碼
app.config['JWT_EMAIL_SECRET_KEY'] = 'SECRET_KEY' #這裡要更改成想要的密碼
db = SQLAlchemy(app)
bcrypt = Bcrypt()

class users(db.Model):
  user_id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150))
  password = db.Column(db.String(60))

  def __init__(self, user_id, email, password):
    self.user_id = user_id
    self.email = email
    self.password = password

class banks(db.Model):
  bank_id = db.Column(db.String(3), primary_key=True)
  bank_name = db.Column(db.String(15))

  def __init__(self, bank_id, bank_name):
    self.id = bank_id
    self.name = bank_name

class cards(db.Model):
  bank_id = db.Column(db.String(3), primary_key=True)
  category = db.Column(db.String(1), primary_key=True)
  card_id = db.Column(db.String(3), primary_key=True)
  card_name = db.Column(db.String(20))
  feedback_type = db.Column(db.String(1))
  link = db.Column(db.String(120))

  def __init__(self, bank_id, category, card_id, card_name, feedback_type, link):
    self.bank_id = bank_id
    self.category = category
    self.card_id = card_id
    self.card_name = card_name
    self.feedback_type = feedback_type
    self.link = link

class user_banklist(db.Model):
  user_id = db.Column(db.Integer, primary_key=True)
  bank_id = db.Column(db.String(3))
  auto_debit = db.Column(db.Boolean)
  e_bill = db.Column(db.Boolean)

  def __init__(self, user_id, bank_id, auto_debit, e_bill):
    self.user_id = user_id
    self.bank_id = bank_id
    self.auto_debit = auto_debit
    self.e_bill = e_bill
    
class user_cardlist(db.Model):
  user_id = db.Column(db.Integer, primary_key=True)
  bank_id = db.Column(db.String(3), primary_key=True)
  category = db.Column(db.String(1), primary_key=True)
  card_id = db.Column(db.String(3), primary_key=True)

  def __init__(self, user_id, bank_id, category, card_id):
    self.user_id = user_id
    self.bank_id = bank_id
    self.category = category
    self.card_id = card_id
    
class basic(db.Model):
  bank_id = db.Column(db.String(3), primary_key=True)
  category = db.Column(db.String(1))
  card_id = db.Column(db.String(3))
  feedback = db.Column(db.Float)
  kind = db.Column(db.String(50))
  basic_remark = db.Column(db.String(100))
  auto_debit = db.Column(db.Boolean)
  e_bill = db.Column(db.Boolean)

  def __init__(self, bank_id, category, card_id, feedback, kind, basic_remark, auto_debit, e_bill):
    self.bank_id = bank_id
    self.category = category
    self.card_id = card_id
    self.feedback = feedback
    self.kind = kind
    self.basic_remark = basic_remark
    self.auto_debit = auto_debit
    self.e_bill = e_bill

class activity(db.Model):
  bank_id = db.Column(db.String(3), primary_key=True)
  category = db.Column(db.String(1))
  card_id = db.Column(db.String(3))
  title = db.Column(db.String(100))
  start = db.Column(db.Date)
  end = db.Column(db.Date)
  feedback = db.Column(db.Float)
  restriction = db.Column(db.Integer)  # 回饋上限
  condition = db.Column(db.Integer)  # 回饋條件
  store = db.Column(db.String(200))
  activity_remark = db.Column(db.String(200))
  link = db.Column(db.String(200)) 
  state = db.Column(db.Boolean)  # 是否還有活動,0是有 1是結束

  def __init__(self, bank_id, category, card_id, title, start, end, feedback, restriction, condition, store, activity_remark, link, state):
    self.bank_id = bank_id
    self.category = category
    self.card_id = card_id
    self.title = title
    self.start = start
    self.end = end
    self.feedback = feedback
    self.restriction = restriction
    self.condition = condition
    self.store = store
    self.activity_remark = activity_remark
    self.link = link
    self.state = state

@app.route('/login', methods=['POST'])
def login():
  email = request.json['email']
  jwt_email = jwt.encode({'email':email}, app.config['JWT_EMAIL_SECRET_KEY'], algorithm='HS256')
  password = request.json['password']
  # 檢查是使用者是否存在
  user = users.query.filter_by(email=jwt_email).first()
  if not user:
    return jsonify({'message': '查無此帳號，請重新輸入'}), 404
  # 確認密碼是否吻合
  if not bcrypt.check_password_hash(user.password, password):
    return jsonify({'message': '密碼錯誤'}), 401
  # 登入成功通知
  username = email[:email.index("@")]
  usertoken = jwt.encode({'user_id': user.user_id}, app.config['JWT_ID_SECRET_KEY'], algorithm='HS256')

  return jsonify({'message': 'User logged in successfully','userinf':{'username': username,'email': email,'token': usertoken}}), 200

@app.route('/register', methods=['POST'])
def register():
  email = request.json['email']
  password = request.json['password']
  hashed_password = bcrypt.generate_password_hash(password=password)
  jwt_email = jwt.encode({'email':email}, app.config['JWT_EMAIL_SECRET_KEY'], algorithm='HS256')
  # 檢查是否註冊
  email_check = users.query.filter_by(email=jwt_email).first()
  if email_check:
    return jsonify({'message': '電子信箱已註冊過'}), 400
  # Create a new user
  new_user = users(None, jwt_email, hashed_password)
  db.session.add(new_user)
  db.session.commit()
  username = email[:email.index("@")]
  user_id = users.query.filter_by(email=jwt_email).first().user_id
  usertoken = jwt.encode({'user_id': user_id}, app.config['JWT_ID_SECRET_KEY'], algorithm='HS256')

  return jsonify({'message': 'User registered successfully','userinf':{'username': username,'email': email,'token': usertoken}}), 201

@app.route('/forgetpw', methods=['POST'])
def forgetpw():
  email = request.json['email']
  jwt_email = jwt.encode({'email':email}, app.config['JWT_EMAIL_SECRET_KEY'], algorithm='HS256')
  user = users.query.filter_by(email=jwt_email).first()
  if not user:
    return jsonify({'message': '查無此帳號，請重新輸入'}), 404
  else:
    while True: #執行do-while
      characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" #建立包含數字大小寫英文的字串
      password = "".join([random.choice(characters) for _ in range(8)]) #從上述字串中抽取隨機8碼字元
      uppercase = 0 ; lowercase = 0 ; number = 0 
      for strs in password: #檢查是否有大小寫及數字
        if(strs.isupper()) :
          uppercase += 1
        elif(strs.islower()):
          lowercase += 1
        elif(strs.isdigit()):
          number +=1
      if(lowercase!=0 and number!=0 and uppercase!=0): #檢查是否符合包含大小寫英文及數字如有就不用重新生成
        break  
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "Ucard forgot reset"  #郵件標題
    content["from"] = "ucard112408@gmail.com"  #寄件者
    content["to"] = email #收件者
    content.attach(MIMEText("臨時密碼："+str(password)+"\n請立即回到app並更改密碼確保資料安全"))  #郵件內容
    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as smtp:  # 設定SMTP伺服器
      try:
        smtp.ehlo()  # 驗證SMTP伺服器
        smtp.login("ucard112408@gmail.com", "密碼密碼密碼")  # 登入寄件者gmail     #######################################gmail密碼
        smtp.send_message(content)  # 寄送郵件
        smtp.close()
      except Exception as e:
        print("Error message: ", e)
  
  password = hashlib.sha256(password.encode('utf-8')).hexdigest()
  users.query.filter_by(email=jwt_email).update({'password': bcrypt.generate_password_hash(password=password)})
  db.session.commit()
  return jsonify({'message': 'User change password successfully'}), 202

@app.route('/changepwd', methods=['POST'])
def changepwd():
  email = request.json['email']
  jwt_email = jwt.encode({'email':email}, app.config['JWT_EMAIL_SECRET_KEY'], algorithm='HS256')
  password = request.json['password']
  newpassword = request.json['newpassword']
  user = users.query.filter_by(email=jwt_email).first()
  #判斷舊密碼是否正確
  if not bcrypt.check_password_hash(user.password, password):
    return jsonify({'message': '密碼錯誤'}), 401
  users.query.filter_by(email=jwt_email).update({'password': bcrypt.generate_password_hash(password=newpassword)})
  db.session.commit()
  username = email[:email.index("@")]
  return jsonify({'message': 'User logged in successfully','userinf':{'username': username,'email': email,'token': user.user_id}}), 203

@app.route('/getbank', methods=['POST'])
def getbank():
  data = request.json
  user_id = jwt.decode(data['usertoken'], app.config['JWT_ID_SECRET_KEY'], algorithms=['HS256'])['user_id']
  banklist = banks.query.all()
  
  # 陣列化資料
  serialized_banks = []
  for bank in banklist:
    check = user_banklist.query.filter_by(user_id=user_id,bank_id=bank.bank_id).first()
    if not check:
      serialized_bank = {
        'bank_id': bank.bank_id,
        'bank_name': bank.bank_name,
        'ischeck': False,
        'auto_debit': False,
        'e_bill': False
      }
    else:
      serialized_bank = {
        'bank_id': bank.bank_id,
        'bank_name': bank.bank_name,
        'ischeck': True,
        'auto_debit': check.auto_debit,
        'e_bill': check.e_bill
      }
    serialized_banks.append(serialized_bank)
  return jsonify(serialized_banks),201

@app.route('/editgetbank', methods=['POST'])
def editgetbank():
  data = request.json
  user_id = jwt.decode(data['usertoken'], app.config['JWT_ID_SECRET_KEY'], algorithms=['HS256'])['user_id']
  banklist = banks.query.all()
  
  # 陣列化資料
  serialized_banks = []
  for bank in banklist:
    check = user_banklist.query.filter_by(user_id=user_id,bank_id=bank.bank_id).first()
    if check:
      serialized_bank = {
        'bank_id': bank.bank_id,
        'bank_name': bank.bank_name,
        'ischeck': True,
        'auto_debit': check.auto_debit,
        'e_bill': check.e_bill
      }
    serialized_banks.append(serialized_bank)
  return jsonify(serialized_banks),201

@app.route('/add_bank', methods=['POST'])
def add_bank():
  data = request.json
  user_id = jwt.decode(data['usertoken'], app.config['JWT_ID_SECRET_KEY'], algorithms=['HS256'])['user_id']
  bankdata = data['bank_data']
  user_banklist.query.filter_by(user_id=user_id).delete()
  
  for i in range(len(bankdata)):
     if(bankdata[i]['ischeck'] == True):
       new_banklist = user_banklist(user_id, bankdata[i]['bank_id'], bankdata[i]['auto_debit'], bankdata[i]['e_bill'])
       db.session.add(new_banklist)
       db.session.commit()
  
  return jsonify({'message': 'Add bank successfully'}),201

@app.route('/getcard', methods=['POST'])
def getcard():
  bank_id = request.json['bank_id']
  user_id = jwt.decode(request.json['usertoken'], app.config['JWT_ID_SECRET_KEY'], algorithms=['HS256'])['user_id']
  cardlist = cards.query.filter_by(bank_id=bank_id).all()

  # 陣列化資料
  serialized_cards_visa = []
  serialized_cards_ms = []
  serialized_cards_jcb = []
  for card in cardlist:
    check = user_cardlist.query.filter_by(user_id=user_id,bank_id=card.bank_id,category=card.category,card_id=card.card_id).first()
    if(card.bank_id == '013' and int(card.card_id) >=101 and int(card.card_id) <=105): #& int(card.card_id) >= 101 & int(card.card_id) <= 105
      if(int(card.card_id) == 101):
        if not check:
          serialized_card = {
            'card_id': card.bank_id + card.category + card.card_id,
            'card_name': '國泰CUBE卡',
            'ischeck': False
          }
        else:
          serialized_card = {
            'card_id': card.bank_id + card.category + card.card_id,
            'card_name': '國泰CUBE卡',
            'ischeck': True
          }
      else:
        continue
    else:
      if not check:
        serialized_card = {
          'card_id': card.bank_id + card.category + card.card_id,
          'card_name': card.card_name,
          'ischeck': False
        }
      else:
        serialized_card = {
          'card_id': card.bank_id + card.category + card.card_id,
          'card_name': card.card_name,
          'ischeck': True
        }

    match(card.category):
      case '0':
        serialized_cards_visa.append(serialized_card)
      case '1':
        serialized_cards_ms.append(serialized_card)
      case '2':
        serialized_cards_jcb.append(serialized_card)
  
  return jsonify({'visa':serialized_cards_visa, 'ms':serialized_cards_ms, 'jcb':serialized_cards_jcb}),201

@app.route('/add_card', methods=['POST'])
def add_card():
  data = request.json
  user_id = jwt.decode(data['usertoken'], app.config['JWT_ID_SECRET_KEY'], algorithms=['HS256'])['user_id']
  bank_id = data['bank_id']
  carddata = data['card_list']
  user_cardlist.query.filter_by(user_id=user_id,bank_id=bank_id).delete()
  db.session.commit()
  for i in range(len(carddata)):
    if(carddata[i]['ischeck'] == True):
      if(carddata[i]['card_id'] == '0130101' or carddata[i]['card_id'] == '0131101' or carddata[i]['card_id'] == '0132101'): 
        cube = ['101', '102', '103', '104', '105']
        for j in cube:
          new_cardlist = user_cardlist(user_id, carddata[i]['card_id'][:3], carddata[i]['card_id'][3:4], j)
          db.session.add(new_cardlist)
          db.session.commit()
      else:
        new_cardlist = user_cardlist(user_id, carddata[i]['card_id'][:3], carddata[i]['card_id'][3:4], carddata[i]['card_id'][4:])
        db.session.add(new_cardlist)
        db.session.commit()
  
  return jsonify({'message': 'Add bank successfully'}),201

@app.route('/getshop', methods=['POST'])
def getshop():
  # 設定 Google Maps API 金鑰
  API_KEY = "API_KEY"   #  API_KEY  API_KEY  API_KEY  API_KEY  API_KEY

  # 設定查詢經緯度
  LATITUDE = request.json['latitude'] # 25.042401556125302
  LONGITUDE = request.json['longitude'] # 121.52531344898848

  # 建立 Google Maps API 查詢物件
  params = {
    "key": API_KEY,
    "location": f"{LATITUDE},{LONGITUDE}",
    "radius": 1000,
    "type": "bakery|bar|book_store|bowling_alley|cafe\
      |car_dealer|car_rental|car_repair|clothing_store\
      |convenience_store|department_store|drugstore\
      |electronics_store|florist|furniture_store\
      |gas_station|gym|hardware_store|home_goods_store\
      |jewelry_store|liquor_store|lodging|meal_delivery|meal_takeaway\
      |movie_theater|night_club|parking|pet_store|pharmacy\
      |restaurant|shoe_store|shopping_mall|store|supermarket|travel_agency"
  }

  # 發送查詢請求
  response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=params)

  # 解析查詢回應
  results = json.loads(response.content)

  # 列出距離最近的五個銷售店家
  names_list = []  # 創建一個空的列表來儲存名稱
  for result in results["results"]:
    names_list.append(result['name'])

  return jsonify(names_list),203

@app.route('/recommend', methods=['POST'])
def recommend():
  search_keyword = request.json["shopname"]
  amount = request.json["amount"]
  user_id = jwt.decode(request.json['usertoken'], app.config['JWT_ID_SECRET_KEY'], algorithms=['HS256'])['user_id']

  cardlist = user_cardlist.query.filter_by(user_id = user_id).all()
  serialized_cards = [] # 推薦前的卡片id
  
  for card in cardlist:
    check = cards.query.filter_by(bank_id = card.bank_id, category = card.category, card_id = card.card_id).first()
    serialized_card = {
      'bank_id': card.bank_id,
      'category': card.category,
      'card_id': card.card_id,
      'card_name': check.card_name,
      'yn': True,
      'fbamount': 0.0,
      'shortremark': '展開看詳細...',
      'longremark': '',
      'link': check.link
    }
    serialized_cards.append(serialized_card)
  
  # neo4j讀取資料

  #更改Neo4j Bolt連線設定
  uri = ""    # neo4j連結
  username = ""  # neo4j帳號
  password = ""  # neo4j密碼

  # 定義查詢，並加入查詢參數
  cypher_query =  """
                    OPTIONAL MATCH (c:card)-[:reward]-(shop)-[:include]-(cate:Categorical)
                    WHERE toLower(shop.name) CONTAINS toLower($search_keyword)
                    RETURN c, shop, cate
                """
            
  query = """
              OPTIONAL MATCH (cc:card)-[:reward]-(cate:Categorical)-[:include]-(shop)
              WHERE toLower(shop.name) CONTAINS toLower($search_keyword)
              RETURN cc, cate
          """

  # 定義函數執行查詢
  def execute_query(cypher_query, shop_name):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run(cypher_query, search_keyword=shop_name)
            return result.data()

  def double_query(query, shop_name):
      with GraphDatabase.driver(uri, auth=(username, password)) as driver:
          with driver.session() as session:
              result = session.run(query, search_keyword=shop_name)
              return result.data()
          
  card_namelist =[]
  # 執行並存入陣列
  result_data = execute_query(cypher_query, search_keyword)
  result_data2 = double_query(query, search_keyword)

  for r in result_data:
    for r2 in result_data2:
        if r['c'] and r['cate'] and r2['cc']:
            card_namelist.append(r2['cc']['name'])
            categoricals = r2['cate']['name']
    break
    
  for r in result_data:
      if r['c'] and r['cate']:
          card_namelist.append(r['c']['name'])
          categoricals = r['cate']['name']
      elif r['cate']:
          for r2 in result_data2:
              card_namelist.append(r2['cc']['name'])
              categoricals = r2['cate']['name'] 
      else:
          print(f"卡片:{r['c']['name']} || 類別:{r['shop']['name']}")
          card_namelist.append(r['c']['name'])
          categoricals = search_keyword

  # 將neo4j讀取到的卡片存入陣列
  for i in range(len(card_namelist)):
    cardinf = cards.query.filter_by(card_name = card_namelist[i]).all()
    for card in cardinf:
      serialized_card = {
        'bank_id': card.bank_id,
        'category': card.category,
        'card_id': card.card_id,
        'card_name': card.card_name,
        'yn': False,
        'fbamount': 0,
        'shortremark': '展開看詳細...',
        'longremark': '',
        'link': check.link
      }
      serialized_cards.append(serialized_card)
  
  unique_cards = {}

  for card in serialized_cards:
    card_name = card['card_name']
    if card_name not in unique_cards:
        unique_cards[card_name] = card

  result = []

  for card in unique_cards.values():
    bank_data = user_banklist.query.filter_by(user_id=user_id, bank_id=card['bank_id']).first()
    if not bank_data:
      auto_debit = False
      e_bill = False
    else:
      auto_debit = bank_data.auto_debit
      e_bill = bank_data.e_bill
    
    # 短期活動回饋計算
    if(card['yn'] == True):
      activity_data = activity.query.filter_by(bank_id = card['bank_id'], category = card['category'], card_id = card['card_id'], state = 0).filter(activity.store.ilike(search_keyword)).all()
      if activity_data:
        card['shortremark'] = '有符合短期活動，' + card['shortremark']
        for ac in activity_data:
          if(ac.feedback<0):
            if ac.restriction and ac.restriction <= amount:
              card['fbamount'] = card['fbamount'] + ac.restrictionround
              card['longremark'] = card['longremark'] + '短期活動名稱：' + ac.title + '\n短期活動加碼金額：' + ac.restrictionround + '元\n'
            else:
              card['fbamount'] = card['fbamount'] + round(amount*ac.feedback)
              card['longremark'] = card['longremark'] + '短期活動名稱：' + ac.title + '\n短期活動加碼金額：' + round(amount*ac.feedback) + '元\n'
          else:
            if ac.condition and ac.condition <= amount:
              card['fbamount'] = card['fbamount'] + ac.feedback
              card['longremark'] = card['longremark'] + '短期活動名稱：' + ac.title + '\n短期活動加碼金額：' + ac.feedback + '元\n'
      else:
        activity_data = activity.query.filter_by(bank_id = card['bank_id'], category = card['category'], card_id = '000', state = 0).filter(activity.store.ilike(search_keyword)).all()
        if activity_data:
          card['shortremark'] = '有符合短期活動，' + card['shortremark']
          for ac in activity_data:
            if(ac.feedback<0):
              if ac.restriction and ac.restriction <= amount:
                card['fbamount'] = card['fbamount'] + ac.restrictionround
                card['longremark'] = card['longremark'] + '短期活動名稱：' + ac.title + '\n短期活動加碼金額：' + ac.restrictionround + '元\n'
              else:
                card['fbamount'] = card['fbamount'] + round(amount*ac.feedback)
                card['longremark'] = card['longremark'] + '短期活動名稱：' + ac.title + '\n短期活動加碼金額：' + round(amount*ac.feedback) + '元\n'
            else:
              if ac.condition and ac.condition <= amount:
                card['fbamount'] = card['fbamount'] + ac.feedback
                card['longremark'] = card['longremark'] + '短期活動名稱：' + ac.title + '\n短期活動加碼金額：' + ac.feedback + '元\n'
    # 長期活動回饋計算
    if(card['card_name'] in card_namelist):
      basic_data = basic.query.filter_by(bank_id=card['bank_id'], category=card['category'], card_id=card['card_id'], kind=categoricals).all()
    else:
      basic_data = basic.query.filter_by(bank_id=card['bank_id'], category=card['category'], card_id=card['card_id'], kind='linepay').all()
      card['shortremark'] = '需透過linepay支付，' + card['shortremark']
    if len (basic_data) > 1:
      a_list =[]
      e_list =[]
      for a_e in basic_data:
        a_list.append(a_e.auto_debit)
        e_list.append(a_e.e_bill)
      # 如果使用者選擇自動扣繳，則選擇自動扣繳條件為 True 的那一種
      if auto_debit == False and len(list(dict.fromkeys(a_list))) == 2:
        basic_data = [x for x in basic_data if x.auto_debit == False]
      # 如果使用者選擇電子帳單，則選擇電子帳單條件為 True 的那一種
      if e_bill == False and len(list(dict.fromkeys(e_list))) == 2:
        basic_data = [x for x in basic_data if x.e_bill == False]
      # 如果還有多種回饋比例，則選擇回饋比例最高的那一種
      if len (basic_data) > 1:
        basic_data = max (basic_data, key=lambda x: x.feedback)
    try:
      card['fbamount'] = round(amount*basic_data.feedback)
      card['longremark'] = card['longremark'] + '長期卡片回饋比例：' + basic_data.feedback*100 + '%\n' + '長期活動回饋金額：' + round(amount*basic_data.feedback) + '元'
    except:
      card['fbamount'] = round(amount*basic_data[0].feedback)
      card['longremark'] = card['longremark'] + '長期卡片回饋比例：' + basic_data[0].feedback*100 + '%\n' + '長期活動回饋金額：' + round(amount*basic_data[0].feedback) + '元'
    
    card['card_name'] = card['card_name'].replace('_', '\n')
    result.append(card)
  sorted_data = sorted(result, key=lambda x: x['fbamount'], reverse=True)
  sorted_data = sorted_data[:5]
  
  return jsonify(sorted_data),201

if __name__ == '__main__':
  app.run(debug='true',host='192.168.50.151') #192.168.50.151、192.168.176.197
