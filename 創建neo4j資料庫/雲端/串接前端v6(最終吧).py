from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

#更改Neo4j Bolt連線設定
uri = "uri"
username = "neo4j"
password = "password"

# 用户输入的店铺名称
user_input_shop_name = "全家"

# 定义查询语句，并使用参数化查询
cypher_query = """
            OPTIONAL MATCH (c:card)-[:reward]-(shop)
            WHERE toLower(shop.name) CONTAINS toLower($user_input_shop_name)
            
            OPTIONAL MATCH (cate:Categorical)-[:include]-(shop)
            WHERE toLower(shop.name) CONTAINS toLower($user_input_shop_name)

            OPTIONAL MATCH (cc:card)-[:reward]-(cate:Categorical)
            WHERE toLower(shop.name) CONTAINS toLower($user_input_shop_name)
            
            
            RETURN c, shop, cate, cc
            """

# 定义函数执行查询
def execute_query(cypher_query, shop_name):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run(cypher_query, user_input_shop_name=shop_name)
            return result.data()

# 执行查询并打印结果
result_data = execute_query(cypher_query, user_input_shop_name)
for r in result_data:
    if r['cate']:
        print(f"卡片:{r['c']['name']} || 店家:{r['shop']['name']} || 類別:{r['cate']['name']}")
    
    else:
        print(f"卡片:{r['c']['name']} || 類別:{r['shop']['name']}")