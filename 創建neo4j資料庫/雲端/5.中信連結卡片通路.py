from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

#更改Neo4j Bolt連線設定
uri = "uri"
driver = GraphDatabase.driver(uri, auth=("neo4j", "Password"))

def do_Cypher(tx, text):
    result = tx.run(text)
    return result

#建立節點函式
def create_relationship(tx, from_node_name, to_node_names, relation_type):
    # 檢查 from_node 是否存在
    check_from_node_query = "MATCH (from_node {name: $from_node_name}) RETURN from_node"
    from_node_exists = tx.run(check_from_node_query, from_node_name=from_node_name)

    if not from_node_exists.single():
        print(f"！！！！！！Node '{from_node_name}' does not exist！！！！！！")
        return

    for to_node_name in to_node_names:
        # 檢查 to_node 是否存在
        check_to_node_query = "MATCH (to_node {name: $to_node_name}) RETURN to_node"
        to_node_exists = tx.run(check_to_node_query, to_node_name=to_node_name)

        if not to_node_exists.single():
            print(f"！！！！！Node '{to_node_name}' does not exist！！！！！")
        else:
            # 如果節點存在，則建立關聯
            merge_query = (
                "MATCH (from_node {name: $from_node_name}) "
                "MATCH (to_node {name: $to_node_name}) "
                "MERGE (from_node)-[r:" + relation_type + "]->(to_node) "
                "RETURN r"
            )

            result = tx.run(merge_query, from_node_name=from_node_name, to_node_name=to_node_name)

            if result.peek():
                print(" ")
            else:
                print("++Relationship created++")


#-------------------------------以下為建立資料庫的 code------------------------------------------
# 統一企業認同卡
with driver.session() as session:
    rewards = [
        "open錢包", "icash_Pay", "Apple_Pay", "Google_Pay",
        "SevenEleven711統一超商", "星巴克", "cosmed康是美",
        "統一時代百貨", "夢時代", "速邁樂加油站", "聖德科斯",
        "misterdonut", "博客來", "foodomo"
        ]
    session.write_transaction(create_relationship, "統一企業認同卡", rewards, "reward")

# 酷玩卡_鈦金卡 
with driver.session() as session:
    rewards = [
        "台灣中油", "台灣大哥大", "中華電信", "遠傳", "台灣之星", "亞太", 
        "yahoo奇摩購物中心", "yahoo拍賣", "yahoo超級商城",
        "pchome線上購物", "momo", "樂天", "淘寶",
        "博客來", "udn買東西", "PayEasy", "東京著衣", "天母嚴選", 
        "OB嚴選", "lativ", "紅陽科技", "綠界科技", "Gomaji",
        "friday購物", "東森購物", "生活市集", "iTunes", "linepay",  
    ]
    session.write_transaction(create_relationship, "酷玩卡_鈦金卡", rewards, "reward")

# MUJI無印良品聯名卡_白金卡
with driver.session() as session:
    rewards = ["muji無印良品"]
    session.write_transaction(create_relationship, "MUJI無印良品聯名卡_白金卡", rewards, "reward")

# MUJI無印良品聯名卡_晶緻卡
with driver.session() as session:
    rewards = ["muji無印良品"]
    session.write_transaction(create_relationship, "MUJI無印良品聯名卡_晶緻卡", rewards, "reward")

# MUJI無印良品聯名卡_御璽卡
with driver.session() as session:
    rewards = ["muji無印良品"]
    session.write_transaction(create_relationship, "MUJI無印良品聯名卡_御璽卡", rewards, "reward")

# 勤美天地聯名卡_白金卡
with driver.session() as session:
    rewards = [
        "台中金典酒店", "金典綠園道商場", "勤美誠品綠園道", 
        "park2草悟廣場"
    ]
    session.write_transaction(create_relationship, "勤美天地聯名卡_白金卡", rewards, "reward")

# 勤美天地聯名卡_晶緻卡
with driver.session() as session:
    rewards = [
        "台中金典酒店", "金典綠園道商場", "勤美誠品綠園道", 
        "park2草悟廣場"
    ]
    session.write_transaction(create_relationship, "勤美天地聯名卡_晶緻卡", rewards, "reward")

# 勤美天地聯名卡_御璽卡
with driver.session() as session:
    rewards = [
        "台中金典酒店", "金典綠園道商場", "勤美誠品綠園道", 
        "park2草悟廣場"
    ]
    session.write_transaction(create_relationship, "勤美天地聯名卡_御璽卡", rewards, "reward")

# 南紡購物中心聯名卡_白金卡
with driver.session() as session:
    rewards = ["南紡購物中心"]
    session.write_transaction(create_relationship, "南紡購物中心聯名卡_白金卡", rewards, "reward")

# 南紡購物中心聯名卡_御璽卡
with driver.session() as session:
    rewards = ["南紡購物中心"]
    session.write_transaction(create_relationship, "南紡購物中心聯名卡_御璽卡", rewards, "reward")

# 南紡購物中心聯名卡_鼎極無限卡
with driver.session() as session:
    rewards = ["南紡購物中心"]
    session.write_transaction(create_relationship, "南紡購物中心聯名卡_鼎極無限卡", rewards, "reward")

# 大葉髙島屋聯名卡_白金卡
with driver.session() as session:
    rewards = ["大葉高島屋百貨"]
    session.write_transaction(create_relationship, "大葉髙島屋聯名卡_白金卡", rewards, "reward")

# 大葉髙島屋聯名卡_晶緻卡
with driver.session() as session:
    rewards = ["大葉高島屋百貨"]
    session.write_transaction(create_relationship, "大葉髙島屋聯名卡_晶緻卡", rewards, "reward")

# 大葉髙島屋聯名卡_御璽卡
with driver.session() as session:
    rewards = ["大葉高島屋百貨"]
    session.write_transaction(create_relationship, "大葉髙島屋聯名卡_御璽卡", rewards, "reward")

# 大葉髙島屋聯名卡_鈦金卡
with driver.session() as session:
    rewards = ["大葉高島屋百貨"]
    session.write_transaction(create_relationship, "大葉髙島屋聯名卡_鈦金卡", rewards, "reward")

# 大葉髙島屋聯名卡_無限卡
with driver.session() as session:
    rewards = ["大葉高島屋百貨"]
    session.write_transaction(create_relationship, "大葉髙島屋聯名卡_無限卡", rewards, "reward")

# 大葉髙島屋聯名卡_世界卡
with driver.session() as session:
    rewards = ["大葉高島屋百貨"]
    session.write_transaction(create_relationship, "大葉髙島屋聯名卡_世界卡", rewards, "reward")

# 秀泰聯名卡_白金卡
with driver.session() as session:
    rewards = [
        "ShowTimes秀泰影城", "秀泰生活", "花蓮蝴蝶谷溫泉渡假村"
    ]
    session.write_transaction(create_relationship, "秀泰聯名卡_白金卡", rewards, "reward")

# 秀泰聯名卡_晶緻卡
with driver.session() as session:
    rewards = [
        "ShowTimes秀泰影城", "秀泰生活", "花蓮蝴蝶谷溫泉渡假村"
    ]
    session.write_transaction(create_relationship, "秀泰聯名卡_晶緻卡", rewards, "reward")

# GlobalMall聯名卡_白金卡
with driver.session() as session:
    rewards = [
        "globalmall環球購物中心"
    ]
    session.write_transaction(create_relationship, "GlobalMall聯名卡_白金卡", rewards, "reward")

# GlobalMall聯名卡_御璽卡
with driver.session() as session:
    rewards = [
        "globalmall環球購物中心"
    ]
    session.write_transaction(create_relationship, "GlobalMall聯名卡_御璽卡", rewards, "reward")

# GlobalMall聯名卡_無限卡
with driver.session() as session:
    rewards = [
        "globalmall環球購物中心"
    ]
    session.write_transaction(create_relationship, "GlobalMall聯名卡_無限卡", rewards, "reward")

# 漢神百貨聯名卡_白金卡
with driver.session() as session:
    rewards = [
        "漢神百貨", "漢神巨蛋", "漢來大飯店"
    ]
    session.write_transaction(create_relationship, "漢神百貨聯名卡_白金卡", rewards, "reward")

# 漢神百貨聯名卡_鈦金卡
with driver.session() as session:
    rewards = [
        "漢神百貨", "漢神巨蛋", "漢來大飯店"
    ]
    session.write_transaction(create_relationship, "漢神百貨聯名卡_鈦金卡", rewards, "reward")

# 漢神百貨聯名卡_晶緻卡
with driver.session() as session:
    rewards = [
        "漢神百貨", "漢神巨蛋", "漢來大飯店"
    ]
    session.write_transaction(create_relationship, "漢神百貨聯名卡_晶緻卡", rewards, "reward")

# 漢神百貨聯名卡_御璽卡
with driver.session() as session:
    rewards = [
        "漢神百貨", "漢神巨蛋", "漢來大飯店"
    ]
    session.write_transaction(create_relationship, "漢神百貨聯名卡_御璽卡", rewards, "reward")

# 漢神百貨聯名卡_世界卡
with driver.session() as session:
    rewards = [
        "漢神百貨", "漢神巨蛋", "漢來大飯店"
    ]
    session.write_transaction(create_relationship, "漢神百貨聯名卡_世界卡", rewards, "reward")

# 漢神百貨聯名卡_無限卡
with driver.session() as session:
    rewards = [
        "漢神百貨", "漢神巨蛋", "漢來大飯店"
    ]
    session.write_transaction(create_relationship, "漢神百貨聯名卡_無限卡", rewards, "reward")

# 中華電信聯名卡_白金卡
with driver.session() as session:
    rewards = [
        "Hami_Pay", "中華電信", "神腦國際senao"
    ]
    session.write_transaction(create_relationship, "中華電信聯名卡_白金卡", rewards, "reward")

# 中華電信聯名卡_鈦金卡
with driver.session() as session:
    rewards = [
        "Hami_Pay", "中華電信", "神腦國際senao"
    ]
    session.write_transaction(create_relationship, "中華電信聯名卡_鈦金卡", rewards, "reward")

# 中華電信聯名卡_世界卡
with driver.session() as session:
    rewards = [
        "Hami_Pay", "中華電信", "神腦國際senao"
    ]
    session.write_transaction(create_relationship, "中華電信聯名卡_世界卡", rewards, "reward")

# 中華電信聯名卡_御璽卡
with driver.session() as session:
    rewards = [
        "Hami_Pay", "中華電信", "神腦國際senao"
    ]
    session.write_transaction(create_relationship, "中華電信聯名卡_御璽卡", rewards, "reward")

# 中華電信聯名卡_無限卡
with driver.session() as session:
    rewards = [
        "Hami_Pay", "中華電信", "神腦國際senao"
    ]
    session.write_transaction(create_relationship, "中華電信聯名卡_無限卡", rewards, "reward")

# 中信商務卡_雙幣商務卡
with driver.session() as session:
    rewards = []
    session.write_transaction(create_relationship, "中信商務卡_雙幣商務卡", rewards, "reward")

# LEXUS聯名卡
with driver.session() as session:
    rewards = [
        "Lexus凌志", "海外", "台灣中油"
    ]
    session.write_transaction(create_relationship, "LEXUS聯名卡", rewards, "reward")

# 中信兄弟聯名卡_白金卡
with driver.session() as session:
    rewards = ["中信兄弟售票網"]
    session.write_transaction(create_relationship, "中信兄弟聯名卡_白金卡", rewards, "reward")

# 中信兄弟聯名卡_鈦金卡
with driver.session() as session:
    rewards = ["中信兄弟售票網"]
    session.write_transaction(create_relationship, "中信兄弟聯名卡_鈦金卡", rewards, "reward")

# 中信兄弟聯名卡_御璽卡
with driver.session() as session:
    rewards = ["中信兄弟售票網"]
    session.write_transaction(create_relationship, "中信兄弟聯名卡_御璽卡", rewards, "reward")

# 中信兄弟聯名卡_鼎極卡 
with driver.session() as session:
    rewards = ["中信兄弟售票網"]
    session.write_transaction(create_relationship, "中信兄弟聯名卡_鼎極卡", rewards, "reward")

# SuperLife_VISA卡
with driver.session() as session:
    rewards = [
        "家樂福", "大潤發", "愛買", "楓康", "保費",
        
        # 餐廳
        "餐廳",
        "王品牛排", "tasty西堤牛排", "丰龢和牛涮", "肉次方燒肉放題", "oh_my原燒",
        "和牛涮", "尬鍋台式潮鍋", "聚北海道昆布鍋", "石二鍋", "青花驕",
        "_12MINI", "陶板屋", "藝奇和牛岩板焼", "夏慕尼新香榭鐵板燒", "品田牧場",
        "享鴨", "hot7鐵板燒", "莆田", "築間幸福鍋物", "燒肉smile",
        "有之和牛鍋物放題", "本格和牛燒肉放題", "繪馬別邸", "瓦城泰國料理", 
        "非常泰概念餐坊", "_1010湘", "大心新泰式麵食", "時時香RICE_BAR", "YABI_KITCHEN", 
        "月月THAI_BBQ", "樂子The_Dinner", "茹絲葵經典牛排館", "屋馬燒肉", "solo_pasta義大利麵", 
        "俺達の肉屋_日本和牛專門店", "鹽之華", "廚房有雞花雕雞", "碳佐麻里精品燒肉", 
        "与玥樓頂級粵菜", "RAW", "山海樓", "金蓬萊遵古台菜", "老新台菜", 
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
        "墾丁福華渡假飯店", "漢來大飯店", 
        "漢堡王", "鬍鬚張", "麥當勞", "星巴克", "TeaTop台灣第一味",
        "康青龍", "萬波島嶼紅茶", "貢茶", "赤鬼炙燒牛排", "misterdonut",
        "爭鮮迴轉壽司", "涮乃葉"
    ]
    session.write_transaction(create_relationship, "SuperLife_VISA卡", rewards, "reward")

# ---------------------------------------------------------------------------------------------------------------------------------

# 中信紅利卡_生活菁英
with driver.session() as session:
    rewards = [
        "台灣中油",
        "燦坤", "全國電子", "順發3c", "三井3c", "大同3c",
        "大潤發", "大買家", "愛買", "家樂福",
        "餐廳", "飯店",
        
        # 飯店
        "台北遠東香格里拉", "台南遠東香格里拉", "新竹國賓大飯店", "馥蘭朵烏來渡假酒店", "馥蘭朵墾丁渡假酒店",
        "馥森里山藝術生態園", "馥森阪治Trio", "花蓮理想大地", 
        "台北福華大飯店", "新竹福華大飯店", "台中福華大飯店",
        "溪頭福華渡假飯店", "高雄福華大飯店", "石門水庫福華渡假飯店",
        "墾丁福華渡假飯店", "漢來大飯店", "台中金典酒店", "民宿", "青年旅館",
        "花蓮蝴蝶谷溫泉渡假村",
        
        # 餐廳
        "王品牛排", "tasty西堤牛排", "丰龢和牛涮", "肉次方燒肉放題", "oh_my原燒",
        "和牛涮", "尬鍋台式潮鍋", "聚北海道昆布鍋", "石二鍋", "青花驕",
        "_12MINI", "陶板屋", "藝奇和牛岩板焼", "夏慕尼新香榭鐵板燒", "品田牧場",
        "享鴨", "hot7鐵板燒", "莆田", "築間幸福鍋物", "燒肉smile",
        "有之和牛鍋物放題", "本格和牛燒肉放題", "繪馬別邸", "瓦城泰國料理", 
        "非常泰概念餐坊", "_1010湘", "大心新泰式麵食", "時時香RICE_BAR", "YABI_KITCHEN", 
        "月月THAI_BBQ", "樂子The_Dinner", "茹絲葵經典牛排館", "屋馬燒肉", "solo_pasta義大利麵", 
        "俺達の肉屋_日本和牛專門店", "鹽之華", "廚房有雞花雕雞", "碳佐麻里精品燒肉", 
        "与玥樓頂級粵菜", "RAW", "山海樓", "金蓬萊遵古台菜", "老新台菜", 
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
        "墾丁福華渡假飯店", "漢來大飯店", 
        "漢堡王", "鬍鬚張", "麥當勞", "星巴克", "TeaTop台灣第一味",
        "康青龍", "萬波島嶼紅茶", "貢茶", "赤鬼炙燒牛排", "misterdonut",
        "爭鮮迴轉壽司", "涮乃葉",
        
        "旅行社", "飛機航空公司"
    ]
    session.write_transaction(create_relationship, "中信紅利卡_生活菁英", rewards, "reward")

# 中信紅利卡_時尚高手
with driver.session() as session:
    rewards = [
        "百貨公司", "書局",
        "大潤發", "大買家", "愛買", "家樂福"
    ]
    session.write_transaction(create_relationship, "中信紅利卡_時尚高手", rewards, "reward")

# ---------------------------------------------------------------------------------------------------------------------------------

# 中信現金回饋鈦金卡
with driver.session() as session:
    rewards = []
    session.write_transaction(create_relationship, "中信現金回饋鈦金卡", rewards, "reward")

# 中信現金回饋御璽卡
with driver.session() as session:
    rewards = []
    session.write_transaction(create_relationship, "中信現金回饋御璽卡", rewards, "reward")

# ---------------------------------------------------------------------------------------------------------------------------------

# 中信紅利晶緻卡_居家族
with driver.session() as session:
    rewards = [
        "超市", "海外",
        "家樂福", "全聯福利中心", "大潤發", "大買家", "愛買",
        "喜互惠", "楓康", "Mia_Cbon", "心樸市集", "棉花田生機園地",
        "好市多Costco", "聖德科斯"
    ]
    session.write_transaction(create_relationship, "中信紅利晶緻卡_居家族", rewards, "reward")

# 中信紅利晶緻卡_旅遊族
with driver.session() as session:
    rewards = [
        "海外", "旅行社", "飯店", "餐廳",
        
        # 飯店
        "台北遠東香格里拉", "台南遠東香格里拉", "新竹國賓大飯店", "馥蘭朵烏來渡假酒店", "馥蘭朵墾丁渡假酒店",
        "馥森里山藝術生態園", "馥森阪治Trio", "花蓮理想大地", 
        "台北福華大飯店", "新竹福華大飯店", "台中福華大飯店",
        "溪頭福華渡假飯店", "高雄福華大飯店", "石門水庫福華渡假飯店",
        "墾丁福華渡假飯店", "漢來大飯店", "台中金典酒店", "民宿", "青年旅館",
        "花蓮蝴蝶谷溫泉渡假村",
        
        # 餐廳
        "王品牛排", "tasty西堤牛排", "丰龢和牛涮", "肉次方燒肉放題", "oh_my原燒",
        "和牛涮", "尬鍋台式潮鍋", "聚北海道昆布鍋", "石二鍋", "青花驕",
        "_12MINI", "陶板屋", "藝奇和牛岩板焼", "夏慕尼新香榭鐵板燒", "品田牧場",
        "享鴨", "hot7鐵板燒", "莆田", "築間幸福鍋物", "燒肉smile",
        "有之和牛鍋物放題", "本格和牛燒肉放題", "繪馬別邸", "瓦城泰國料理", 
        "非常泰概念餐坊", "_1010湘", "大心新泰式麵食", "時時香RICE_BAR", "YABI_KITCHEN", 
        "月月THAI_BBQ", "樂子The_Dinner", "茹絲葵經典牛排館", "屋馬燒肉", "solo_pasta義大利麵", 
        "俺達の肉屋_日本和牛專門店", "鹽之華", "廚房有雞花雕雞", "碳佐麻里精品燒肉", 
        "与玥樓頂級粵菜", "RAW", "山海樓", "金蓬萊遵古台菜", "老新台菜", 
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
        "墾丁福華渡假飯店", "漢來大飯店", 
        "漢堡王", "鬍鬚張", "麥當勞", "星巴克", "TeaTop台灣第一味",
        "康青龍", "萬波島嶼紅茶", "貢茶", "赤鬼炙燒牛排", "misterdonut",
        "爭鮮迴轉壽司", "涮乃葉"
    ]
    session.write_transaction(create_relationship, "中信紅利晶緻卡_旅遊族", rewards, "reward")

# 中信紅利晶緻卡_行動族
with driver.session() as session:
    rewards = [
        "台灣中油", "餐廳", "保費", "海外",
        
        # 餐廳
        "王品牛排", "tasty西堤牛排", "丰龢和牛涮", "肉次方燒肉放題", "oh_my原燒",
        "和牛涮", "尬鍋台式潮鍋", "聚北海道昆布鍋", "石二鍋", "青花驕",
        "_12MINI", "陶板屋", "藝奇和牛岩板焼", "夏慕尼新香榭鐵板燒", "品田牧場",
        "享鴨", "hot7鐵板燒", "莆田", "築間幸福鍋物", "燒肉smile",
        "有之和牛鍋物放題", "本格和牛燒肉放題", "繪馬別邸", "瓦城泰國料理", 
        "非常泰概念餐坊", "_1010湘", "大心新泰式麵食", "時時香RICE_BAR", "YABI_KITCHEN", 
        "月月THAI_BBQ", "樂子The_Dinner", "茹絲葵經典牛排館", "屋馬燒肉", "solo_pasta義大利麵", 
        "俺達の肉屋_日本和牛專門店", "鹽之華", "廚房有雞花雕雞", "碳佐麻里精品燒肉", 
        "与玥樓頂級粵菜", "RAW", "山海樓", "金蓬萊遵古台菜", "老新台菜", 
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
        "墾丁福華渡假飯店", "漢來大飯店", 
        "漢堡王", "鬍鬚張", "麥當勞", "星巴克", "TeaTop台灣第一味",
        "康青龍", "萬波島嶼紅茶", "貢茶", "赤鬼炙燒牛排", "misterdonut",
        "爭鮮迴轉壽司", "涮乃葉"
    ]
    session.write_transaction(create_relationship, "中信紅利晶緻卡_行動族", rewards, "reward")

# 中信紅利晶緻卡_時尚族
with driver.session() as session:
    rewards = [
        "海外", "百貨公司"
    ]
    session.write_transaction(create_relationship, "中信紅利晶緻卡_時尚族", rewards, "reward")

# ---------------------------------------------------------------------------------------------------------------------------------

# 中信紅利御璽卡_居家族
with driver.session() as session:
    rewards = [
        "超市", "海外",
        "家樂福", "全聯福利中心", "大潤發", "大買家", "愛買",
        "喜互惠", "楓康", "Mia_Cbon", "心樸市集", "棉花田生機園地",
        "好市多Costco", "聖德科斯"
    ]
    session.write_transaction(create_relationship, "中信紅利御璽卡_居家族", rewards, "reward")

# 中信紅利御璽卡_旅遊族
with driver.session() as session:
    rewards = [
        "海外", "旅行社", "飯店", "餐廳",
        
        # 飯店
        "台北遠東香格里拉", "台南遠東香格里拉", "新竹國賓大飯店", "馥蘭朵烏來渡假酒店", "馥蘭朵墾丁渡假酒店",
        "馥森里山藝術生態園", "馥森阪治Trio", "花蓮理想大地", 
        "台北福華大飯店", "新竹福華大飯店", "台中福華大飯店",
        "溪頭福華渡假飯店", "高雄福華大飯店", "石門水庫福華渡假飯店",
        "墾丁福華渡假飯店", "漢來大飯店", "台中金典酒店", "民宿", "青年旅館",
        "花蓮蝴蝶谷溫泉渡假村",
        
        # 餐廳
        "王品牛排", "tasty西堤牛排", "丰龢和牛涮", "肉次方燒肉放題", "oh_my原燒",
        "和牛涮", "尬鍋台式潮鍋", "聚北海道昆布鍋", "石二鍋", "青花驕",
        "_12MINI", "陶板屋", "藝奇和牛岩板焼", "夏慕尼新香榭鐵板燒", "品田牧場",
        "享鴨", "hot7鐵板燒", "莆田", "築間幸福鍋物", "燒肉smile",
        "有之和牛鍋物放題", "本格和牛燒肉放題", "繪馬別邸", "瓦城泰國料理", 
        "非常泰概念餐坊", "_1010湘", "大心新泰式麵食", "時時香RICE_BAR", "YABI_KITCHEN", 
        "月月THAI_BBQ", "樂子The_Dinner", "茹絲葵經典牛排館", "屋馬燒肉", "solo_pasta義大利麵", 
        "俺達の肉屋_日本和牛專門店", "鹽之華", "廚房有雞花雕雞", "碳佐麻里精品燒肉", 
        "与玥樓頂級粵菜", "RAW", "山海樓", "金蓬萊遵古台菜", "老新台菜", 
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
        "墾丁福華渡假飯店", "漢來大飯店", 
        "漢堡王", "鬍鬚張", "麥當勞", "星巴克", "TeaTop台灣第一味",
        "康青龍", "萬波島嶼紅茶", "貢茶", "赤鬼炙燒牛排", "misterdonut",
        "爭鮮迴轉壽司", "涮乃葉"
    ]
    session.write_transaction(create_relationship, "中信紅利御璽卡_旅遊族", rewards, "reward")

# 中信紅利御璽卡_行動族
with driver.session() as session:
    rewards = [
        "台灣中油", "餐廳", "保費", "海外",
        
        # 餐廳
        "王品牛排", "tasty西堤牛排", "丰龢和牛涮", "肉次方燒肉放題", "oh_my原燒",
        "和牛涮", "尬鍋台式潮鍋", "聚北海道昆布鍋", "石二鍋", "青花驕",
        "_12MINI", "陶板屋", "藝奇和牛岩板焼", "夏慕尼新香榭鐵板燒", "品田牧場",
        "享鴨", "hot7鐵板燒", "莆田", "築間幸福鍋物", "燒肉smile",
        "有之和牛鍋物放題", "本格和牛燒肉放題", "繪馬別邸", "瓦城泰國料理", 
        "非常泰概念餐坊", "_1010湘", "大心新泰式麵食", "時時香RICE_BAR", "YABI_KITCHEN", 
        "月月THAI_BBQ", "樂子The_Dinner", "茹絲葵經典牛排館", "屋馬燒肉", "solo_pasta義大利麵", 
        "俺達の肉屋_日本和牛專門店", "鹽之華", "廚房有雞花雕雞", "碳佐麻里精品燒肉", 
        "与玥樓頂級粵菜", "RAW", "山海樓", "金蓬萊遵古台菜", "老新台菜", 
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
        "墾丁福華渡假飯店", "漢來大飯店", 
        "漢堡王", "鬍鬚張", "麥當勞", "星巴克", "TeaTop台灣第一味",
        "康青龍", "萬波島嶼紅茶", "貢茶", "赤鬼炙燒牛排", "misterdonut",
        "爭鮮迴轉壽司", "涮乃葉"
    ]
    session.write_transaction(create_relationship, "中信紅利御璽卡_行動族", rewards, "reward")

# 中信紅利御璽卡_時尚族
with driver.session() as session:
    rewards = [
        "海外", "百貨公司"
    ]
    session.write_transaction(create_relationship, "中信紅利御璽卡_時尚族", rewards, "reward")

# ---------------------------------------------------------------------------------------------------------------------------------

# 中國信託鼎極卡_世界卡
with driver.session() as session:
    rewards = []
    session.write_transaction(create_relationship, "中國信託鼎極卡_世界卡", rewards, "reward")

# 中國信託鼎極卡_極緻卡
with driver.session() as session:
    rewards = []
    session.write_transaction(create_relationship, "中國信託鼎極卡_極緻卡", rewards, "reward")

# 中國信託鼎極卡_無限卡
with driver.session() as session:
    rewards = []
    session.write_transaction(create_relationship, "中國信託鼎極卡_無限卡", rewards, "reward")

# 和泰聯名卡
with driver.session() as session:
    rewards = [
        "toyota豐田", "Lexus凌志", "yoxi計程車", "iRent",
        "hotai購商城購物", "長源汽車", "和泰產險",
        "家樂福", "大潤發", "愛買", "ikea宜家家居", "特力屋", 
        "旅行社", "飛機航空公司", "飯店", 
        
        # 飯店
        "台北遠東香格里拉", "台南遠東香格里拉", "新竹國賓大飯店", "馥蘭朵烏來渡假酒店", "馥蘭朵墾丁渡假酒店",
        "馥森里山藝術生態園", "馥森阪治Trio", "花蓮理想大地", 
        "台北福華大飯店", "新竹福華大飯店", "台中福華大飯店",
        "溪頭福華渡假飯店", "高雄福華大飯店", "石門水庫福華渡假飯店",
        "墾丁福華渡假飯店", "漢來大飯店", "台中金典酒店", "民宿", "青年旅館",
        "花蓮蝴蝶谷溫泉渡假村",
        
        "Agoda", "Booking_com", "Expedia", "Hotels_com", "AsiaYo",
        "Trip_com", "Airbnb", "KKday", "KLOOK",
        "海外", "和泰pay"
    ]
    session.write_transaction(create_relationship, "和泰聯名卡", rewards, "reward")

# TAIPEI101聯名卡_新御璽卡
with driver.session() as session:
    rewards = [
        "台北101"
    ]
    session.write_transaction(create_relationship, "TAIPEI101聯名卡_新御璽卡", rewards, "reward")

# TAIPEI101聯名卡_新鼎極卡
with driver.session() as session:
    rewards = [
        "台北101"
    ]
    session.write_transaction(create_relationship, "TAIPEI101聯名卡_新鼎極卡", rewards, "reward")

# TAIPEI101聯名卡_尊榮鼎極卡
with driver.session() as session:
    rewards = [
        "台北101"
    ]
    session.write_transaction(create_relationship, "TAIPEI101聯名卡_尊榮鼎極卡", rewards, "reward")

# 中油聯名卡_白金卡
with driver.session() as session:
    rewards = [
        "台灣中油", "中油pay"
    ]
    session.write_transaction(create_relationship, "中油聯名卡_白金卡", rewards, "reward")

# 中油聯名卡_御璽卡
with driver.session() as session:
    rewards = [
        "台灣中油", "中油pay"
    ]
    session.write_transaction(create_relationship, "中油聯名卡_御璽卡", rewards, "reward")


# 英雄聯盟信用卡
with driver.session() as session:
    rewards = [
        "App_Store", "Google_Play", "Bandai萬代南夢宮遊戲", "Blizzard暴雪", "Electronic_arts",
        "Epic_games_store", "GASH", "Garena", "MyCard", "Nintendo",
        "PlayStation", "Square_enix", "Steam", "Ubisoft", "Xbox",
        "appleTV", "CATCHPLAY", "iTunes", "KKBOX", "LINETV", 
        "LiTV", "Netflix", "Spotify", "Youtube_Premium", "KKTV",
        "Amazon_Prime_Video", "Disney_Plus", "讀墨電子書READMOO", 
        "台灣角川官方網站", "尖端網路書店", "青文出版社", "長鴻新漫網",
        "台灣東販出版社", "東立電子書城", "動畫瘋", "Booklive", "BOOKWALKER",
        "Kakao_Webtoon", "LINE_WEBTOON","POCKET_COMICS", "讀墨電子書READMOO",
        "udn售票", "iNDIEVOX售票", "KKTIX售票", "ibon售票",
        "tixcraft拓元售票", "FamiTicket全網購票", "OPENTIX兩廳院文化生活",
        "中信兄弟售票網", "年代售票", "寬宏售票"
    ]
    session.write_transaction(create_relationship, "英雄聯盟信用卡", rewards, "reward")

# LINE_Pay信用卡
with driver.session() as session:
    rewards = [
        "linepay", "ipass一卡通"
    ]
    session.write_transaction(create_relationship, "LINE_Pay信用卡", rewards, "reward")

# ALL_ME卡
with driver.session() as session:
    rewards = [
        "SevenEleven711統一超商", "全家FamilyMart", "萊爾富", "OK", "美廉社",
        "小北百貨", "棉花田生機園地", 
        "台鐵", "台灣大車隊", "嘟嘟房", "路邊停車",
        "屈臣氏", "cosmed康是美", "poya寶雅", "松本清", "日藥本舖",
        "三井3c", "順發3c", "京站時尚廣場", "美麗華百樂園",
        "宏匯廣場", "三創生活園區", "屏東太平洋百貨",
        "漢堡王", "鬍鬚張", "勝博殿", "大戶屋", "沃克牛排", 
        "TeaTop台灣第一味", "金色三麥", "康青龍", "萬波島嶼紅茶",
        "貢茶", "赤鬼炙燒牛排",
        "FunNow", "拍享券", "一起寄", "九乘九文具專家",
        "卡多摩嬰童館", "Wstyle", "咕咕G寵物城", "貓狗大棧寵物百貨",
        "SofyDog蘇菲狗寵物精品", "寵物公園", "凱朵寵物美容沙龍", "貓狗隊長",
        "讀墨電子書READMOO"
    ]
    session.write_transaction(create_relationship, "ALL_ME卡", rewards, "reward")

# LaLaport聯名卡
with driver.session() as session:
    rewards = [
        "台中Mitsui_Shopping_Park_LaLaport"
    ]
    session.write_transaction(create_relationship, "LaLaport聯名卡", rewards, "reward")

# Agoda聯名卡
with driver.session() as session:
    rewards = [
        "Agoda"
    ]
    session.write_transaction(create_relationship, "Agoda聯名卡", rewards, "reward")

print("-------------done----------")
