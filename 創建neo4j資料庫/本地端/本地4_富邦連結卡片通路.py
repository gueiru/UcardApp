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
                print("--Relationship existed--")
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

# 富邦IMPERIAL尊御世界卡
with driver.session() as session:
    rewards = [
        "台北美福大飯店", "寒舍艾麗酒店", "台北新板希爾頓酒店", "台北君悅酒店",
        "新竹國賓大飯店", "台中日月千禧酒店", "台南遠東香格里拉", "君品酒店",
        "台北W飯店"    
    ]
    session.write_transaction(create_relationship, "富邦IMPERIAL尊御世界卡", rewards, "reward")

# 富邦數位生活一卡通聯名卡
with driver.session() as session:
    rewards = [
        "yahoo奇摩購物中心", "yahoo超級商城", "yahoo拍賣", "pchome線上購物",
        "pchome商店街", "淘寶", "天貓", "蝦皮購物",
        "myfone購物", "udn買東西", "樂天", "friday購物", "博客來", "生活市集",
        "松果購物", "citiesocial找好東西", "zalora", "shopback",
        "東森購物", "森森", "viva", "momo",
        
        "台灣大哥大", "中華電信", "遠傳", "台灣之星", "亞太"
    ]
    session.write_transaction(create_relationship, "富邦數位生活一卡通聯名卡", rewards, "reward")

# 富邦鈦金卡
with driver.session() as session:
    rewards = [
        
    ]
    session.write_transaction(create_relationship, "富邦鈦金卡", rewards, "reward")

# 富邦數位生活悠遊聯名卡
with driver.session() as session:
    rewards = [
        "yahoo奇摩購物中心", "yahoo超級商城", "yahoo拍賣", "pchome線上購物",
        "pchome商店街", "淘寶", "天貓", "蝦皮購物",
        "myfone購物", "udn買東西", "樂天", "friday購物", "博客來", "生活市集",
        "松果購物", "citiesocial找好東西", "zalora", "shopback",
        "東森購物", "森森", "viva", "momo",
        
        "台灣大哥大", "中華電信", "遠傳", "台灣之星", "亞太"
    ]
    session.write_transaction(create_relationship, "富邦數位生活悠遊聯名卡", rewards, "reward")
    
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
        "百貨公司", "超市", "國內餐飲", "加油站", "書局",
        "旅行社",
        "虎航", "長榮航空", "華航", "星宇", "立榮",  "華信"
    ]
    session.write_transaction(create_relationship, "富邦富利生活系列卡", rewards, "reward")

print("-------------done----------")
