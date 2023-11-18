from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

# 建立與 Neo4j 的連接
uri = "neo4j+s://cd122923.databases.neo4j.io"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

# 定義一個查詢函式
def run_query(tx, search_keyword):
    query = (
        "MATCH (c)-[:reward]->(r) "
        "WHERE r CONTAINS $search_keyword "
        "RETURN c, r"
    )

    result = tx.run(query, search_keyword=search_keyword)
    return result.data()

# 進行查詢
search_keyword = "蝦皮購物"

with driver.session() as session:
    result = session.read_transaction(run_query, search_keyword)

# 處理查詢結果
for record in result:
    print(f"Card: {record['c']}, Reward: {record['r']}")