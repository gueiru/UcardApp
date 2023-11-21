from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

#更改Neo4j Bolt連線設定
uri = "uri"
username = "neo4j"
password = "password"

# 輸入
user_input_shop_name = "foodpanda"

# cypher
query1 =    """
            OPTIONAL MATCH (c:card)-[:reward]-(shop)-[:include]-(cate:Categorical)
            WHERE toLower(shop.name) CONTAINS toLower($user_input_shop_name)
            RETURN c, shop, cate
        """
            
query2 = """
            OPTIONAL MATCH (ccs:card)-[:reward]-(cate:Categorical)-[:include]-(shop)
            WHERE toLower(shop.name) CONTAINS toLower($user_input_shop_name)
            RETURN ccs, cate
        """
        
query3 = """
            OPTIONAL MATCH (cc:card)-[:reward]-(shop:Categorical)
            WHERE toLower(shop.name) CONTAINS toLower($user_input_shop_name)
            RETURN cc, shop
        """

# 查詢函數
def one_query(query1, shop_name):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run(query1, user_input_shop_name=shop_name)
            return result.data()

def double_query(query2, shop_name):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run(query2, user_input_shop_name=shop_name)
            return result.data()
        
def triple_query(query3, shop_name):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run(query3, user_input_shop_name=shop_name)
            return result.data()
    

# 查詢輸出
result1 = one_query(query1, user_input_shop_name)
result2 = double_query(query2, user_input_shop_name)
result3 = triple_query(query3, user_input_shop_name)

if result3:
    for r3 in result3:
        if r3['cc']:
            print(f"卡片:{r3['cc']['name']} || 類別:{r3['shop']['name']}")
        else:
            for r in result1:
                for r2 in result2:
                    if r['c'] and r['cate'] and r2['ccs']:
                        print(f"卡片:{r2['ccs']['name']} || 類別:{r2['cate']['name']}")
                break
        
            for r in result1:
                if r['c'] and r['cate']:
                    print(f"卡片:{r['c']['name']} || 店家:{r['shop']['name']} || 類別:{r['cate']['name']}")

                else:
                    for r2 in result2:
                        print(f"卡片:{r2['ccs']['name']} || 類別:{r2['cate']['name']}")
            

else:    
    for r in result1:
        for r2 in result2:
            if r['c'] and r['cate'] and r2['ccs']:
                print(f"卡片:{r2['ccs']['name']} || 類別:{r2['cate']['name']}")
        break
        
    for r in result1:
        if r['c'] and r['cate']:
            print(f"卡片:{r['c']['name']} || 店家:{r['shop']['name']} || 類別:{r['cate']['name']}")

        else:
            for r2 in result2:
                print(f"卡片:{r2['ccs']['name']} || 類別:{r2['cate']['name']}")