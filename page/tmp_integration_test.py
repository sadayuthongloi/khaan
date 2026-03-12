import sys
import os
sys.path.append(r"d:\khaan\page")

from database_manager import MongoDBConnectionManager, MongoDBClient

def run_test():
    cm = MongoDBConnectionManager()
    connections = cm.connections
    if not connections:
        print("No connections found")
        return
    
    conn = connections[0]
    print(f"Using connection: {conn['name']}")
    
    client = MongoDBClient(conn)
    
    db_name = "endoindex"
    col_name = "tb_booking"
    
    # get a small set of data
    res = client.get_collection_data(db_name, col_name, limit=1)
    if not res.get('success'):
        print("Failed to get data:", res)
        return
        
    data = res['data']
    if not data:
        print("No data in collection")
        return
        
    doc = data[0]
    doc_id = str(doc['_id'])
    
    print(f"Found doc_id: {doc_id}")
    
    res = client.get_document(db_name, col_name, doc_id)
    if not res.get('success'):
        print("Failed to get document:", res)
        return
        
    json_str = res['document_json']
    
    # Try saving it back unchanged
    print("Trying to update...")
    res = client.update_document(db_name, col_name, doc_id, json_str)
    print("Update result:", res)

if __name__ == '__main__':
    run_test()
