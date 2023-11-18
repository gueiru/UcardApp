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
def create_relationship(tx, from_node_name, to_node_names, relation_type):
    # 檢查 from_node 是否存在
    check_from_node_query = "MATCH (from_node {name: $from_node_name}) RETURN from_node"
    from_node_exists = tx.run(check_from_node_query, from_node_name=from_node_name)

    if not from_node_exists.single():
        print(f"！！！！！！Node '{from_node_name}' does not exist")
        return

    for to_node_name in to_node_names:
        # 檢查 to_node 是否存在
        check_to_node_query = "MATCH (to_node {name: $to_node_name}) RETURN to_node"
        to_node_exists = tx.run(check_to_node_query, to_node_name=to_node_name)

        if not to_node_exists.single():
            print(f"！！！！！Node '{to_node_name}' does not exist")
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
                print("--Relationship existed--")
            else:
                print("++Relationship created++")


#-------------------------------以下為建立資料庫的 code------------------------------------------
# CUBE卡_趣旅行
with driver.session() as session:
    rewards = [
        "日本", "韓國", "泰國", "新加坡", "國外餐飲",
               
        "Uber", "LINE_TAXI", "yoxi計程車", "台灣大車隊", "大都會計程車",
        
        "和運租車", "iRent", "格上租車", "中租租車", "AVIS租車",
        
        "虎航", "長榮航空", "華航", "星宇", "立榮",  "華信", 
        
        "民宿", "青年旅館", "連鎖飯店",
        
        "KKday", "Agoda", "KLOOK", "Airbnb", "Hotels_com",
        "Expedia", "Booking_com", "Trip_com", "AsiaYo",
        
        "ezTravel易遊網", "雄獅旅遊",
        "可樂旅遊", "東南旅遊", "五福旅遊", "燦星旅遊", "山富旅遊", "長汎假期",
        "鳳凰旅行社", "Ezfly易飛網", "理想旅遊", "永利旅行社", "三賀旅行社"
        ]
    session.write_transaction(create_relationship, "CUBE卡_趣旅行", rewards, "reward")

# CUBE卡_慶生月
with driver.session() as session:
    rewards = [
        "遠東SOGO百貨", "太平洋百貨", "廣三SOGO",
        
        "民宿", "青年旅館", "連鎖飯店",
        
        "茹絲葵經典牛排館", "屋馬燒肉", "solo_pasta義大利麵", 
        "俺達の肉屋_日本和牛專門店", "鹽之華法式餐廳", "廚房有雞花雕雞", "碳佐麻里精品燒肉", 
        "与玥樓頂級粵菜餐廳", "RAW", "山海樓", "金蓬萊遵古台菜餐廳", "老新台菜",
        
        "國賓影城", "威秀影城", "ShowTimes秀泰影城",
        
        "錢櫃KTV", "好樂迪KTV", "星聚點KTV", "享溫馨KTV" 
    ]
    session.write_transaction(create_relationship,"CUBE卡_慶生月", rewards, "reward")

# 雙幣商務鈦金卡
with driver.session() as session:
    rewards = [
        "台北遠東香格里拉", "台南遠東香格里拉", "新北美食地標Mega50", "新竹國賓大飯店",
        "花蓮理想大地", "馥蘭朵烏來渡假酒店", "馥蘭朵墾丁渡假酒店","馥森里山藝術生態園", "馥森阪治Trio"
    ]        
    session.write_transaction(create_relationship,"雙幣商務鈦金卡", rewards, "reward")

# CUBE卡_集精選
with driver.session() as session:
    rewards = [
        "家樂福",
        "台灣中油",
        "高鐵",
        "SevenEleven711統一超商", "全家FamilyMart", "全聯福利中心",
        "麥當勞", "星巴克",
        "foodomo",
        "遠東SOGO百貨",
        "博客來",
        "城市車旅", "嘟嘟房",
        "open錢包"
    ]
    session.write_transaction(create_relationship,"CUBE卡_集精選", rewards, "reward")

# 蝦皮購物聯名卡
with driver.session() as session:
    rewards = [
        "蝦皮購物", "蝦皮商城"
    ]
    session.write_transaction(create_relationship,"蝦皮購物聯名卡", rewards, "reward")

# CUBE卡_樂饗購
with driver.session() as session:
    rewards = [ "遠東SOGO百貨", "太平洋百貨", "新光三越", "SKM_Park", "遠東百貨",
                "Big_City遠東巨城購物中心", "微風廣場", "誠品生活", "globalmall環球購物中心", "CITYLINK",
                "BELLAVITA", "統一時代百貨", "台北101", "ATT_4_FUN", "明曜百貨", "京站時尚廣場",
                "美麗華百樂園", "大葉高島屋百貨", "遠企購物中心", "比漾廣場", "大江國際購物中心",
                "中友百貨", "廣三SOGO", "Tiger_City", "勤美誠品綠園道", "金典綠園道商場",
                "大魯閣新時代", "耐斯廣場", "南紡購物中心", "德安百貨", "夢時代", "大立百貨",
                "大統百貨", "漢神百貨", "漢神巨蛋",
                "林口MITSUI_OUTLET_PARK", "台中港MITSUI_OUTLET_PARK", "台南MITSUI_OUTLET_PARK",
                "台中Mitsui_Shopping_Park_LaLaport", "禮客", "義大世界購物廣場", "華泰名品城",
                "義享天地", "麗寶OUTLET_Mall", "麗寶百貨廣場", "秀泰生活", "徐匯廣場",
                "台茂購物中心", "桃園統領百貨", "新月廣場", "日曜天地", "三創生活園區", "_6_Plaza廣場",
                "iFG遠雄廣場", "台南FOCUS", "悅誠廣場", "欣欣百貨", "宏匯廣場",
                "高雄棧貳庫商場", "樂購廣場", "NOKE忠泰樂生活", "昇恆昌", 
                
                "Uber_Eats", "foodpanda", "foodomo", "inline", 
                
                "國內餐飲",
                
                "cosmed康是美", "poya寶雅", "屈臣氏", "日藥本舖", "tomod_s", "松本清"
            ]
    session.write_transaction(create_relationship, "CUBE卡_樂饗購", rewards, "reward")

# CUBE卡_玩數位
with driver.session() as session:
    rewards = [
        "Google_Play", "Disney_Plus", "Netflix", "Spotify", "KKBOX", "KKTV",
        "App_Store", "Apple_Music", "iCloud",
                
        "蝦皮購物", "momo", "pchome線上購物", "yahoo奇摩購物中心", "小樹購",
        "amazon", "淘寶", "天貓"
    ]
    session.write_transaction(create_relationship, "CUBE卡_玩數位", rewards, "reward")

# 台塑聯名卡
with driver.session() as session:
    rewards = [
        "台塑生醫", "長庚生技", "台塑購物網", "台塑網旅行社"
    ]
    session.write_transaction(create_relationship,"台塑聯名卡", rewards, "reward")

# 雙幣白金卡
with driver.session() as session:
    rewards = [
        "台北遠東香格里拉", "台南遠東香格里拉", "新北美食地標Mega50", "新竹國賓大飯店",
        "花蓮理想大地", "馥蘭朵烏來渡假酒店", "馥蘭朵墾丁渡假酒店","馥森里山藝術生態園", "馥森阪治Trio"
    ]        
    session.write_transaction(create_relationship,"雙幣白金卡", rewards, "reward")

# 現金回饋御璽卡
with driver.session() as session:
    rewards = [
        "台北遠東香格里拉", "台南遠東香格里拉", "新竹國賓大飯店", "馥蘭朵烏來渡假酒店", "馥蘭朵墾丁渡假酒店",
        "馥森里山藝術生態園", "馥森阪治Trio"
    ]
    session.write_transaction(create_relationship,"現金回饋御璽卡", rewards, "reward")

# eTag聯名卡
with driver.session() as session:
    rewards = [
        "馥蘭朵烏來渡假酒店", "馥蘭朵墾丁渡假酒店", "台南遠東香格里拉"
    ]   

# 世界卡
with driver.session() as session:
    rewards = [
        "台北萬豪酒店", "君悅酒店", "台北遠東香格里拉", "台南遠東香格里拉", "中山招待所",
        "高雄萬豪酒店", "台北寒舍艾美酒店", "台北美福大飯店", "台北晶華酒店", "文華東方酒店",
        "維多麗亞酒店", "漢來名人坊", "瑞穗天合國際觀光酒店", "JR東日本大飯店", "台北美食地標Mega50",
        "新北美食地標Mega50", "新竹國賓大飯店", "林酒店", "高雄林皇宮", "台中長榮桂冠酒店",
        "大地酒店", "台北國泰萬怡酒店", "台北六福萬怡酒店"
    ]
    session.write_transaction(create_relationship,"世界卡", rewards, "reward")

print("-------------done----------")
