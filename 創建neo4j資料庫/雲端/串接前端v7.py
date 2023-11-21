from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

#更改Neo4j Bolt連線設定
uri = "uri"
username = "neo4j"
password = "password"

# 用户输入的店铺名称
user_input_shop_name = "餐廳"

# 定义查询语句，并使用参数化查询
cypher_query =  """
                    OPTIONAL MATCH (c:card)-[:reward]-(shop)-[:include]-(cate:Categorical)
                    WHERE toLower(shop.name) CONTAINS toLower($user_input_shop_name)
                    RETURN c, shop, cate
                """
            
query = """
            OPTIONAL MATCH (cc:card)-[:reward]-(cate:Categorical)-[:include]-(shop)
            WHERE toLower(shop.name) CONTAINS toLower($user_input_shop_name)
            RETURN cc, cate
        """

# 定义函数执行查询
def execute_query(cypher_query, shop_name):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run(cypher_query, user_input_shop_name=shop_name)
            return result.data()

def double_query(query, shop_name):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run(query, user_input_shop_name=shop_name)
            return result.data()
    

# 查詢輸出
result_data = execute_query(cypher_query, user_input_shop_name)
result_data2 = double_query(query, user_input_shop_name)

for r in result_data:
    for r2 in result_data2:
        if r['c'] and r['cate'] and r2['cc']:
            print(f"卡片:{r2['cc']['name']} || 類別:{r2['cate']['name']}")
    break
    
for r in result_data:
    if r['c'] and r['cate']:
        print(f"卡片:{r['c']['name']} || 店家:{r['shop']['name']} || 類別:{r['cate']['name']}")

    elif r['cate']:
        for r2 in result_data2:
            print(f"卡片:{r2['cc']['name']} || 類別:{r2['cate']['name']}")
        
    else:
        print(f"卡片:{r['c']['name']} || 類別:{r['shop']['name']}")