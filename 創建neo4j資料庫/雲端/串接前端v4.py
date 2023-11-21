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
        "OPTIONAL MATCH (source)-[:reward]->(destination) "
        "WHERE toLower(destination.name) CONTAINS toLower($search_keyword) "
        "WITH source, destination "
        "OPTIONAL MATCH (categorical)-[:include]->(destination) "
        "WITH source, destination, COLLECT(DISTINCT categorical) as categoricals "
        "OPTIONAL MATCH (card)-[:reward]->(categorical) "
        "RETURN source, destination, categoricals, COLLECT(DISTINCT card) as cards"
    )
    result = tx.run(query, search_keyword=search_keyword)
    return result.data()


# 輸入關鍵詞
search_keyword = "全家"
with driver.session() as session:
    result = session.read_transaction(run_query, search_keyword)

# 查詢結果
for record in result:
    if record['source']:
        if record['categoricals']:
            print(f"Card: {record['source']}  || shop: {record['destination']} || Categoricals: {record['categoricals']}")
            for card in record['cards']:
                print(f"Card: {card}, Categoricals: {record['categoricals']}")
        else:
            print(f"Source: {record['source']}  ||  Destination: {record['destination']}")
    else:
        for card in record['cards']:
             print(f"Card: {card}, Categoricals: {record['categoricals']}")
    
# 關閉 Neo4j 連線
driver.close()
