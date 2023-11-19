from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

# 建立與 Neo4j 的連接
uri = "bolt://localhost:7687"
#這是林宜靜"本地"的neo4j密碼！！！
driver = GraphDatabase.driver(uri, auth=("neo4j", "Test1022"))

def run_query(tx, search_keyword):
    query = (
        "MATCH (source)-[:reward]->(destination) "
        "WHERE toLower(destination.name) CONTAINS toLower($search_keyword) "
        "WITH source, destination, labels(destination) as destLabels "
        "RETURN source, destination, "
        "CASE WHEN 'Categorical' IN destLabels "
        "     THEN NULL "
        "     ELSE [(destination)-[:include]->(categoricalNode:Categorical)-[:reward]->(categoricalCard:card) | categoricalCard] "
        "END as categoricalCards"
    )
    result = tx.run(query, search_keyword=search_keyword)
    return result.data()

# 輸入關鍵詞
search_keyword = "book"
with driver.session() as session:
    result = session.read_transaction(run_query, search_keyword)

# 查詢結果
for record in result:
    print(f"Source: {record['source']}, Destination: {record['destination']}")
    print("卡片：", record['source'])
    
driver.close()