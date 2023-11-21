from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

#更改Neo4j Bolt連線設定
uri = "uri"
driver = GraphDatabase.driver(uri, auth=("neo4j", "Password"))

def do_Cypher(tx, text):
    result = tx.run(text)
    return result

def run_query(tx, search_keyword):
    query = (
        "OPTIONAL MATCH (source)-[:reward]-(destination)  "
        "WHERE toLower(destination.name) CONTAINS toLower($search_keyword) "
        "WITH source, destination "
        
        "OPTIONAL MATCH (card)-[:reward]-(cate:Categorical)-[:include]-(destination)  "
        "WHERE toLower(destination.name) CONTAINS toLower($search_keyword) "
        "WITH COLLECT(DISTINCT card) as cards, source, destination, cate "
        "RETURN cards, source, destination, cate "
    )

# 輸入關鍵詞  
search_keyword = "萊爾富"

with driver.session() as session:
    result = session.read_transaction(run_query, search_keyword)
    
    for record in result:
        print(f"卡片: {record['source']['name']} || 店家: {record['destination']['name']} || 類別: {record['cate']}") 

# 關閉 Neo4j 連線
driver.close()