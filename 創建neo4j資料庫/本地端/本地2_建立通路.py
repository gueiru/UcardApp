from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

#更改Neo4j Bolt連線設定
uri = "bolt://localhost:7687"
#這是林宜靜"本地"的neo4j密碼！！！
driver = GraphDatabase.driver(uri, auth=("neo4j", "Test1022"))

def do_Cypher(tx, text):
    result = tx.run(text)
    return result

#建立節點函式
def create_knowledge_point(tx, label, relation, obj):
    command = []
    
    # 查看 node A 是否存在 (類別)
    text = "MATCH (n:Categorical {name: $label}) RETURN n"
    result = tx.run(text, label=label)    
    # 檢查查詢結果
    if not result.peek():
        # 如果節點不存在，則建立它
        text = "CREATE (" + label + ":Categorical {name: $label})"
        tx.run(text, label=label)
        command.append(text)
        print("Node created.")
    else:
        print("Node already exists.")
    print(command)
    
    # 查看 node B 是否存在
    text = "MATCH (n:"+label+" {name: $obj}) RETURN n"
    result = tx.run(text, obj=obj)
    # 檢查查詢結果
    if not result.peek():
        # 如果節點不存在，則建立它
        text = "CREATE (" + obj + ":" + label + " {name: $obj})"
        tx.run(text, obj=obj)
        command.append(text)
        print("Node created.")
    else:
        print("Node already exists.")
    print(command)


    # 查看 node A 與 node B 之間的關係是否存在
    text = "MATCH (a:Categorical {name: $label}), (b:" + label + " {name: $obj}) RETURN EXISTS((a)-[:" + relation + "]->(b)) AS relationship_exists"
    result = tx.run(text, label=label, obj=obj)
    single_result = result.single()
    if single_result is not None:
        exists = single_result["relationship_exists"]
    else:
        exists = False
    
    # 如果關聯不存在，則建立它
    if exists is False:
        text = "MATCH (a:Categorical {name: $label}), (b:" + label + " {name: $obj}) CREATE (a)-[:" + relation + "]->(b)"
        tx.run(text, label=label, obj=obj)
        command.append(text)
        print("Relationship created.")
    else:
        print("Relationship already exists.")
    
    print(command)

#-------------------------------以下為建立資料庫的code------------------------------------------


# 和泰集團
with driver.session() as session:
    hotais = [
        "toyota豐田", "Lexus凌志", "yoxi計程車", "iRent",
        "hotai購商城購物", "長源汽車", "和泰產險"
    ]
    for hotai in hotais:
        session.write_transaction(create_knowledge_point, "和泰集團", "include", hotai)
print("----------------------------------------------------------------")

# 費用
with driver.session() as session:
    taxs = [
        "保費", "所得稅", "地價稅", "牌照稅", "房屋稅", "燃料稅"
    ]
    for tax in taxs:
        session.write_transaction(create_knowledge_point, "費用", "include", tax)
print("----------------------------------------------------------------")

# 嬰幼兒用品
with driver.session() as session:
    babys = [
        "小獅王辛巴", "MARURU", "cipu喜舖", "麗嬰房"
    ]
    for baby in babys:
        session.write_transaction(create_knowledge_point, "嬰幼兒用品", "include", baby)
print("----------------------------------------------------------------")

# 國內餐飲
with driver.session() as session:
    restaurants = [
        "王品牛排", "tasty西堤牛排", "丰龢和牛涮", "肉次方燒肉放題", "oh_my原燒",
        "和牛涮", "尬鍋台式潮鍋", "聚北海道昆布鍋", "石二鍋", "青花驕",
        "_12MINI", "陶板屋", "藝奇和牛岩板焼", "夏慕尼新香榭鐵板燒", "品田牧場",
        "享鴨", "hot7鐵板燒", "莆田", "築間幸福鍋物", "燒肉smile",
        "有之和牛鍋物放題", "本格和牛燒肉放題", "繪馬別邸", "瓦城泰國料理", 
        "非常泰概念餐坊", "_1010湘", "大心新泰式麵食", "時時香RICE_BAR", "YABI_KITCHEN", 
        "月月THAI_BBQ", "樂子The_Dinner", "茹絲葵經典牛排館", "屋馬燒肉", "solo_pasta義大利麵", 
        "俺達の肉屋_日本和牛專門店", "鹽之華法式餐廳", "廚房有雞花雕雞", "碳佐麻里精品燒肉", 
        "与玥樓頂級粵菜餐廳", "RAW", "山海樓", "金蓬萊遵古台菜餐廳", "老新台菜", 
        "欣葉台菜", "欣葉小聚", "欣葉鐘菜", "NAGOMI和食饗宴", "欣葉日本料理",
        "欣葉SHABUSHABU", "咖哩匠", "欣葉生活廚房", "paparich金爸爸", "唐點小聚",
        "勝博殿", "大戶屋", "沃克牛排", "金色三麥", 

        "台北萬豪酒店", "君悅酒店", "台北遠東香格里拉", "台南遠東香格里拉", "中山招待所",
        "高雄萬豪酒店", "台北寒舍艾美酒店", "台北美福大飯店", "台北晶華酒店", "文華東方酒店",
        "維多麗亞酒店", "漢來名人坊", "瑞穗天合國際觀光酒店", "JR東日本大飯店", "台北美食地標Mega50",
        "新北美食地標Mega50", "新竹國賓大飯店", "林酒店", "高雄林皇宮", "台中長榮桂冠酒店",
        "大地酒店", "台北國泰萬怡酒店", "台北六福萬怡酒店", "寒舍艾麗酒店", "台北新板希爾頓酒店",
        "台北W飯店", "台北君悅酒店", "台中日月千禧酒店", "君品酒店",
        "台北福華大飯店", "新竹福華大飯店", "台中福華大飯店",
        "溪頭福華渡假飯店", "高雄福華大飯店", "石門水庫福華渡假飯店",
        "墾丁福華渡假飯店", "漢來大飯店"
        
        "漢堡王", "鬍鬚張", "麥當勞", "星巴克", "TeaTop台灣第一味",
        "康青龍", "萬波島嶼紅茶", "貢茶", "赤鬼炙燒牛排", "misterdonut",
        "爭鮮迴轉壽司", "漢堡王"
    ]
    for restaurant in restaurants:
        session.write_transaction(create_knowledge_point, "國內餐飲", "include", restaurant)
print("----------------------------------------------------------------")

# 海外
with driver.session() as session:
    books = [
        "日本", "韓國", "新加坡", "泰國", "國外餐飲",
        "中國", "香港", "澳門"
    ]
    for book in books:
        session.write_transaction(create_knowledge_point, "海外", "include", book)
print("----------------------------------------------------------------")

# 書店
with driver.session() as session:
    books = [
        "金石堂", "金玉堂", "誠品", "墊腳石", "紀伊國屋",
        "法雅客", "博客來", "敦煌書局", "三民書局", "商業週刊",
        "天下雜誌"
    ]
    for book in books:
        session.write_transaction(create_knowledge_point, "書局", "include", book)
print("----------------------------------------------------------------")

# 加油站
with driver.session() as session:
    Gas = [
        "台灣中油", "全國加油站", "台亞", "西歐加油站", "速邁樂加油站"
    ]
    for gas in Gas:
        session.write_transaction(create_knowledge_point, "加油站", "include", gas)
print("----------------------------------------------------------------")

# 電動機車
with driver.session() as session:
    motorcycles = [
        "Gogoro", "USPACE", "UDRIVE", "WeMo", "iRent", "GoShare"
    ]
    for motor in motorcycles:
        session.write_transaction(create_knowledge_point, "電動機車", "include", motor)

# 台塑關係企業
with driver.session() as session:
    relations = [
        "台塑生醫", "長庚生技", "台塑購物網", "台塑網旅行社"
    ]
    for relation in relations:
        session.write_transaction(create_knowledge_point, "台塑關係企業", "include", relation)

# 娛樂
with driver.session() as session:
    entertaments = [
        "錢櫃KTV", "好樂迪KTV", "星聚點KTV", "享溫馨KTV", 
        
        "國賓影城", "威秀影城", "ShowTimes秀泰影城"
    ]
    for ent in entertaments:
        session.write_transaction(create_knowledge_point,"娛樂", "include", ent)
print("----------------------------------------------------------------")

# 停車場
with driver.session() as session:
    parks = [
        "城市車旅", "嘟嘟房", "台灣聯通", "路邊停車"
    ]
    for park in parks:
        session.write_transaction(create_knowledge_point,"停車場", "include", park)
print("----------------------------------------------------------------")

# 超市
with driver.session() as session:
    markets = [
        "家樂福", "全聯福利中心", "大潤發", "大買家", "愛買",
        "喜互惠", "楓康", "Mia_Cbon", "心樸市集", "棉花田生機園地",
        "好市多Costco", "聖德科斯"
    ]
    for m in markets:
        session.write_transaction(create_knowledge_point,"超市", "include", m)
print("----------------------------------------------------------------")

# 連鎖飯店
with driver.session() as session:
    hotels = [
        "台北遠東香格里拉", "台南遠東香格里拉", "新竹國賓大飯店", "馥蘭朵烏來渡假酒店", "馥蘭朵墾丁渡假酒店",
        "馥森里山藝術生態園", "馥森阪治Trio", "花蓮理想大地", 
        "台北福華大飯店", "新竹福華大飯店", "台中福華大飯店",
        "溪頭福華渡假飯店", "高雄福華大飯店", "石門水庫福華渡假飯店",
        "墾丁福華渡假飯店", "漢來大飯店", "台中金典酒店"
    ]
    for h in hotels:
        session.write_transaction(create_knowledge_point, "連鎖飯店", "include", h)
print("----------------------------------------------------------------")

# 住宿
with driver.session() as session:
    hotels = [
        "民宿", "青年旅館", "連鎖飯店"
    ]
    for h in hotels:
        session.write_transaction(create_knowledge_point, "住宿", "include", h)
print("----------------------------------------------------------------")

# 旅行社
with driver.session() as session:
    travel_agencies = [
        "ezTravel易遊網", "雄獅旅遊","可樂旅遊", "東南旅遊", "五福旅遊",
        "燦星旅遊", "山富旅遊", "長汎假期","鳳凰旅行社", "Ezfly易飛網",
        "理想旅遊", "永利旅行社", "三賀旅行社", "台塑網旅行社" 
    ]
    for ta in travel_agencies:
        session.write_transaction(create_knowledge_point, "旅行社", "include", ta)
print("----------------------------------------------------------------")

# 訂房平台
with driver.session() as session:
	travel_platforms = [
        "KKday", "Agoda", "KLOOK", "Airbnb", "Hotels_com",
        "Expedia", "Booking_com", "Trip_com", "AsiaYo"
		]
	for travel in travel_platforms:
	        session.write_transaction(create_knowledge_point, "訂房平台", "include", travel)
print("----------------------------------------------------------------")

# 百貨公司
with driver.session() as session:
    shopping_centers = [
        "遠東SOGO百貨", "太平洋百貨", "新光三越", "SKM_Park", "遠東百貨",
        "Big_City遠東巨城購物中心", "微風廣場", "誠品生活", "globalmall環球購物中心", "CITYLINK",
        "BELLAVITA", "統一時代百貨", "台北101", "ATT_4_FUN", "明曜百貨", "京站時尚廣場",
        "美麗華百樂園", "大葉高島屋百貨", "遠企購物中心", "比漾廣場", "大江國際購物中心",
        "中友百貨", "廣三SOGO", "Tiger_City", "勤美誠品綠園道", "金典綠園道商場", "park2草悟廣場",
        "大魯閣新時代", "耐斯廣場", "南紡購物中心", "德安百貨", "夢時代", "大立百貨",
        "大統百貨", "漢神百貨", "漢神巨蛋", "屏東太平洋百貨",
        "林口MITSUI_OUTLET_PARK", "台中港MITSUI_OUTLET_PARK", "台南MITSUI_OUTLET_PARK",
        "台中Mitsui_Shopping_Park_LaLaport", "禮客", "義大世界購物廣場", "華泰名品城",
        "義享天地", "麗寶OUTLET_Mall", "麗寶百貨廣場", "秀泰生活", "徐匯廣場",
        "台茂購物中心", "桃園統領百貨", "新月廣場", "日曜天地", "三創生活園區", "_6_Plaza廣場",
        "iFG遠雄廣場", "台南FOCUS", "悅誠廣場", "欣欣百貨", "宏匯廣場",
        "高雄棧貳庫商場", "樂購廣場", "NOKE忠泰樂生活", "昇恆昌", "采盟"
    ]
    for shop in shopping_centers:
        session.write_transaction(create_knowledge_point, "百貨公司", "include", shop)
print("----------------------------------------------------------------")

# 電信
with driver.session() as session:
    phones = [
        "台灣大哥大", "中華電信", "遠傳", "台灣之星", "亞太", 
        "神腦國際senao"
    ]
    for p in phones:
        session.write_transaction(create_knowledge_point, "電信", "include", p)
print("----------------------------------------------------------------")
   
# 國內藥妝
with driver.session() as session:
    pharmacies = [
        "cosmed康是美", "poya寶雅", "屈臣氏", "日藥本舖", "tomod_s", "松本清", "DHC"
    ]
    for p in pharmacies:
        session.write_transaction(create_knowledge_point, "國內藥妝", "include", p)
print("----------------------------------------------------------------")

# 外送平台
with driver.session() as session:
    food_delivery_platforms = [
        "Uber_Eats", "foodpanda", "foodomo", "inline"
    ]
    for p in food_delivery_platforms:
        session.write_transaction(create_knowledge_point, "外送平台", "include", p)
print("----------------------------------------------------------------")

# 超商
with driver.session() as session:
    convenience_store = ["SevenEleven711統一超商", "全家FamilyMart", "萊爾富", "OK", "美廉社"]
    for cv in convenience_store:
        session.write_transaction(create_knowledge_point, "超商", "include", cv)
print("----------------------------------------------------------------")

# 生活百貨+3C
with driver.session() as session:
    lifes = [
        "小北百貨", "poya寶雅", "ikea宜家家居", "特力屋", "muji無印良品",
        "FunNow", "拍享券", "一起寄", "九乘九文具專家",
        "卡多摩嬰童館", "Wstyle", "咕咕G寵物城", "貓狗大棧寵物百貨",
        "SofyDog蘇菲狗寵物精品", "寵物公園", "凱朵寵物美容沙龍", "貓狗隊長",
        "燦坤", "全國電子", "順發3c", "三井3c", "大同3c"   
    ]
    for life in lifes:
        session.write_transaction(create_knowledge_point, "生活百貨", "include", life)
print("----------------------------------------------------------------")

# 影音串流平台
with driver.session() as session:
    musics = [
        "Google_Play", "Disney_Plus", "Netflix", "Spotify", "KKBOX", "KKTV",
        "App_Store", "Apple_Music", "iCloud", "MyVideo", "friday影音",
        "凱擘", "PlayStation", "Nintendo", "Steam",
        "Bandai萬代南夢宮遊戲", "Blizzard暴雪", "Electronic_arts",
        "Epic_games_store", "GASH", "Garena", "MyCard", "Nintendo",
        "Square_enix", "Ubisoft", "Xbox",
        "appleTV", "CATCHPLAY", "iTunes", "LINETV", 
        "LiTV", "Youtube_Premium", "Amazon_Prime_Video",
        "讀墨電子書READMOO"
    ]
    for music in musics:
        session.write_transaction(create_knowledge_point, "影音遊戲", "include", music)
print("----------------------------------------------------------------")

# 漫畫動畫
with driver.session() as session:
    animations = [
        "台灣角川官方網站", "尖端網路書店", "青文出版社", "長鴻新漫網",
        "台灣東販出版社", "東立電子書", "動畫瘋", "Booklive", "BOOKWALKER",
        "Kakao_Webtoon", "LINE_WEBTOON","POCKET_COMICS", "讀墨電子書READMOO"
    ]
    for anim in animations:
        session.write_transaction(create_knowledge_point, "漫畫動畫", "include", anim)
print("----------------------------------------------------------------")

# 數位購票
with driver.session() as session:
    Tickets = [
        "udn售票", "iNDIEVOX售票", "KKTIX售票", "ibon售票",
        "tixcraft拓元售票", "FamiTicket全網購票", "OPENTIX兩廳院文化生活",
        "中信兄弟售票網", "年代售票", "寬宏售票"
    ]
    for ticket in Tickets:
        session.write_transaction(create_knowledge_point, "數位購票", "include", ticket)
print("----------------------------------------------------------------")

#電商購物
with driver.session() as session:
    shopping_websites = [
        "蝦皮購物", "momo", "pchome線上購物", "yahoo奇摩購物中心", "小樹購",
        "蝦皮商城", "amazon", "淘寶", "天貓", "博客來",
        "超級商城", "myfone購物", "udn買東西", "pchome商店街",
        "樂天", "friday購物", "生活市集", "yahoo超級商城",
        "松果購物", "citiesocial找好東西", "zalora", "shopback", "yahoo拍賣",
        "東森購物", "森森", "viva", "PayEasy", "東京著衣", "天母嚴選", 
        "OB嚴選", "lativ", "紅陽科技", "綠界科技", "Gomaji"
    ]
    for shop in shopping_websites:
        session.write_transaction(create_knowledge_point, "電商購物", "include", shop)
print("----------------------------------------------------------------")

#支付方式
with driver.session() as session:
    PayList = [
        "歐付寶", "橘子支付", "ezPay簡單付", "街口支付", "全盈_PAY", "全支付" 
        "PChome國際連", "一卡通Money", "悠遊付", "icash_Pay", "linepay", 
        "Apple_Pay", "Samsung_Pay", "Google_Pay", "台灣Pay", "玉山Wallet", 
        "Hami_Pay", "open錢包", "中油pay", "和泰pay"
    ]
    for pay in PayList:
        session.write_transaction(create_knowledge_point, "支付方式", "include", pay)
print("----------------------------------------------------------------")
      
# 交通
with driver.session() as session:
    Traffic_List = [
        "高鐵", "計程車", "公車", "台鐵", "捷運",
        "Uber", "LINE_TAXI", "yoxi計程車", "台灣大車隊", "大都會計程車",
        "和運租車", "iRent", "格上租車", "中租租車", "AVIS租車",
        "ipass一卡通", "悠遊卡"
    ]
    for transportation in Traffic_List:
        session.write_transaction(create_knowledge_point, "交通", "include", transportation)
print("----------------------------------------------------------------")

# 航空公司
with driver.session() as session:
    Airlines = [
        "虎航", "長榮航空", "華航", "星宇", "立榮", "華信"
    ]
    for airline in Airlines:
        session.write_transaction(create_knowledge_point, "航空公司", "include", airline)
        
print("------------------done------------------")