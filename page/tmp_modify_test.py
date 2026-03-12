import sys
import os
import json
sys.path.append(r"d:\khaan\page")

from database_manager import MongoDBConnectionManager, MongoDBClient
from bson import json_util

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
    
    res = client.get_collection_data(db_name, col_name, limit=1)
    if not res.get('success'):
        print("Failed to get data:", res)
        return
        
    doc = res['data'][0]
    doc_id = str(doc['_id'])
    
    res = client.get_document(db_name, col_name, doc_id)
    doc_json = json_util.loads(res['document_json'])
    
    print("Old firstname:", doc_json.get('firstname'))
    doc_json['firstname'] = doc_json.get('firstname', '') + "_edited"
    
    new_json_str = json_util.dumps(doc_json)
    
    res = client.update_document(db_name, col_name, doc_id, new_json_str)
    print("Update result:", res)
    
    # revert
    doc_json['firstname'] = doc_json['firstname'].replace('_edited', '')
    res = client.update_document(db_name, col_name, doc_id, json_util.dumps(doc_json))

if __name__ == '__main__':
    run_test()
