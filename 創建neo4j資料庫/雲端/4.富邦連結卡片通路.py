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
# 富邦鑽保卡
with driver.session() as session:
    rewards = [
        "保費"
    ]
    session.write_transaction(create_relationship, "富邦鑽保卡", rewards, "reward")

# 富邦J卡
with driver.session() as session:
    rewards = [
        "日本", "韓國", "linepay"
    ]
    session.write_transaction(create_relationship, "富邦J卡", rewards, "reward")

# momo卡
with driver.session() as session:
    rewards = [
        "momo"
    ]
    session.write_transaction(create_relationship, "momo卡", rewards, "reward")

# 富邦悍將悠遊聯名卡
with driver.session() as session:
    rewards = [
        
    ]
    session.write_transaction(create_relationship, "富邦悍將悠遊聯名卡", rewards, "reward")

# 富邦世界卡
with driver.session() as session:
    rewards = [
        
    ]
    session.write_transaction(create_relationship, "富邦世界卡", rewards, "reward")

# 富邦IMPERIAL_尊御世界卡
with driver.session() as session:
    rewards = [
        "台北美福大飯店", "寒舍艾麗酒店", "台北新板希爾頓酒店", "台北君悅酒店",
        "新竹國賓大飯店", "台中日月千禧酒店", "台南遠東香格里拉", "君品酒店",
        "台北W飯店"    
    ]
    session.write_transaction(create_relationship, "富邦IMPERIAL_尊御世界卡", rewards, "reward")

# 富邦數位生活_一卡通聯名卡
with driver.session() as session:
    rewards = [
        "yahoo奇摩購物中心", "yahoo超級商城", "yahoo拍賣", "pchome線上購物",
        "pchome商店街", "淘寶", "天貓", "蝦皮購物",
        "myfone購物", "udn買東西", "樂天", "friday購物", "博客來", "生活市集",
        "松果購物", "citiesocial找好東西", "zalora", "shopback",
        "東森購物", "森森", "viva", "momo",
        
        "台灣大哥大", "中華電信", "遠傳", "台灣之星", "亞太"
    ]
    session.write_transaction(create_relationship, "富邦數位生活_一卡通聯名卡", rewards, "reward")

# 富邦鈦金卡
with driver.session() as session:
    rewards = [
        
    ]
    session.write_transaction(create_relationship, "富邦鈦金卡", rewards, "reward")

# 富邦數位生活_悠遊聯名卡
with driver.session() as session:
    rewards = [
        "yahoo奇摩購物中心", "yahoo超級商城", "yahoo拍賣", "pchome線上購物",
        "pchome商店街", "淘寶", "天貓", "蝦皮購物",
        "myfone購物", "udn買東西", "樂天", "friday購物", "博客來", "生活市集",
        "松果購物", "citiesocial找好東西", "zalora", "shopback",
        "東森購物", "森森", "viva", "momo",
        
        "台灣大哥大", "中華電信", "遠傳", "台灣之星", "亞太"
    ]
    session.write_transaction(create_relationship, "富邦數位生活_悠遊聯名卡", rewards, "reward")
    
# 采盟聯名卡
with driver.session() as session:
    rewards = [
        "采盟"
    ]
    session.write_transaction(create_relationship, "采盟聯名卡", rewards, "reward")

# 台茂聯名卡
with driver.session() as session:
    rewards = [
        "台茂購物中心"
    ]
    session.write_transaction(create_relationship, "台茂聯名卡", rewards, "reward")

# 廣三SOGO聯名卡
with driver.session() as session:
    rewards = [
        "廣三SOGO"
    ]
    session.write_transaction(create_relationship, "廣三SOGO聯名卡", rewards, "reward")


# 富邦Costco聯名卡
with driver.session() as session:
    rewards = [
        "好市多Costco"
    ]
    session.write_transaction(create_relationship, "富邦Costco聯名卡", rewards, "reward")


# OpenPossible聯名卡
with driver.session() as session:
    rewards = [
        "台灣大哥大", "MyVideo", "凱擘", "App_Store", "Google_Play",
        "PlayStation", "Nintendo", "Steam",
        "SevenEleven711統一超商", "全家FamilyMart",
        "台灣中油", "全國加油站", "台亞", "西歐加油站", "速邁樂加油站",
        "保費", "淘寶", "天貓", "中國", "香港", "澳門"
    ]
    session.write_transaction(create_relationship, "OpenPossible聯名卡", rewards, "reward")

# 麗嬰房聯名卡
with driver.session() as session:
    rewards = [
        "麗嬰房"
    ]
    session.write_transaction(create_relationship, "麗嬰房聯名卡", rewards, "reward")

# 廣三SOGO悠遊聯名卡
with driver.session() as session:
    rewards = [
        "廣三SOGO"
    ]
    session.write_transaction(create_relationship, "廣三SOGO悠遊聯名卡", rewards, "reward")

# 富邦銀行卡
with driver.session() as session:
    rewards = [
        "嘟嘟房", "台灣聯通"
    ]
    session.write_transaction(create_relationship, "富邦銀行卡", rewards, "reward")
    
# 富邦財神系列卡
with driver.session() as session:
    rewards = [
        
    ]
    session.write_transaction(create_relationship, "富邦財神系列卡", rewards, "reward")

# 富邦無限卡
with driver.session() as session:
    rewards = [
        
    ]
    session.write_transaction(create_relationship, "富邦無限卡", rewards, "reward")

# 福華聯名卡
with driver.session() as session:
    rewards = [
        "台北福華大飯店", "新竹福華大飯店", "台中福華大飯店",
        "溪頭福華渡假飯店", "高雄福華大飯店", "石門水庫福華渡假飯店",
        "墾丁福華渡假飯店"
    ]
    session.write_transaction(create_relationship, "福華聯名卡", rewards, "reward")
    
# DHC聯名卡
with driver.session() as session:
    rewards = [
        "DHC"
    ]
    session.write_transaction(create_relationship, "DHC聯名卡", rewards, "reward")

# 富邦數位生活卡
with driver.session() as session:
    rewards = [
        "yahoo奇摩購物中心", "yahoo超級商城", "yahoo拍賣", "pchome線上購物",
        "pchome商店街", "淘寶", "天貓", "蝦皮購物",
        "myfone購物", "udn買東西", "樂天", "friday購物", "博客來", "生活市集",
        "松果購物", "citiesocial找好東西", "zalora", "shopback",
        "東森購物", "森森", "viva", "momo",
        
        "台灣大哥大", "中華電信", "遠傳", "台灣之星", "亞太"
    ]
    session.write_transaction(create_relationship, "富邦數位生活卡", rewards, "reward")

# 富邦富利生活系列卡
with driver.session() as session:
    rewards = [
        "百貨公司", "超市", "餐廳", "加油站", "書局",
        
        # 超市
        "家樂福", "全聯福利中心", "大潤發", "大買家", "愛買",
        "喜互惠", "楓康", "Mia_Cbon", "心樸市集", "棉花田生機園地",
        "好市多Costco", "聖德科斯",
        
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
        
        "旅行社",
        "虎航", "長榮航空", "華航", "星宇", "立榮",  "華信"
    ]
    session.write_transaction(create_relationship, "富邦富利生活系列卡", rewards, "reward")

print("-------------done----------")
