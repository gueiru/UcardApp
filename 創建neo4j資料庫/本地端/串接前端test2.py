from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

# 建立與 Neo4j 的連接
uri = "neo4j+s://cd122923.databases.neo4j.io"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

# 定義一個查詢函式
def run_query(tx, search_keyword):
    query = (
        "MATCH (source)-[:reward]->(destination) "
        "WHERE toLower(destination.name) CONTAINS toLower($search_keyword) "
        "RETURN source, destination"
    )

    result = tx.run(query, search_keyword=search_keyword)
    return result.data()

# 輸入關鍵詞
search_keyword = "加油站"
with driver.session() as session:
    result = session.read_transaction(run_query, search_keyword)

# 查詢結果
for record in result:
    print(f"Source: {record['source']}, Destination: {record['destination']}")
    print("卡片：", record['source'])
    
driver.close()