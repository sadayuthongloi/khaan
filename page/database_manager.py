"""
MongoDB Database Manager
Manage connections and operations with MongoDB.
"""

import json
import os
import sys
import urllib.parse
from typing import Dict, List, Optional
from pymongo import MongoClient

from crypto_config import maybe_decrypt_field, maybe_encrypt_field, derive_fernet_key


class MongoDBConnectionManager:
    """Manage MongoDB connections"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = self._resolve_config_path(config_file)
        self._fernet_key = self._load_fernet_key()
        self.connections = self.load_connections()

    def _resolve_config_path(self, config_file: str) -> str:
        """
        Make config/key lookup robust for PyInstaller onefile:
        - If `config_file` is relative, resolve it next to the running app (exe) or this module.
        """
        if os.path.isabs(config_file):
            return config_file
        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, config_file)

    def _load_fernet_key(self) -> Optional[bytes]:
        """
        Key source priority:
        1) KHAA_N_KEY_WORDING env var
        2) key.local file (same directory as config.json, or current working directory for relative paths)
        """
        try:
            env_wording = os.environ.get("KHAA_N_KEY_WORDING", "").strip()
            if env_wording:
                return derive_fernet_key(env_wording)

            config_abs = os.path.abspath(self.config_file)
            config_dir = os.path.dirname(config_abs)
            key_file = os.path.join(config_dir, "key.local")

            if os.path.exists(key_file):
                with open(key_file, "r", encoding="utf-8") as f:
                    key_wording = f.read().strip()
                if key_wording:
                    return derive_fernet_key(key_wording)

            return None
        except Exception as e:
            print(f"Error loading encryption key: {e}")
            return None
    
    def load_connections(self) -> List[Dict]:
        """Load connections from config.json"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    connections = data.get('connections', [])
                    if not self._fernet_key:
                        has_encrypted = any(
                            isinstance(conn, dict)
                            and (
                                (isinstance(conn.get("username"), str) and conn.get("username", "").startswith("ENC:"))
                                or (isinstance(conn.get("password"), str) and conn.get("password", "").startswith("ENC:"))
                            )
                            for conn in connections
                        )
                        if has_encrypted:
                            print(
                                "Warning: Encrypted fields found in config.json but no key was provided "
                                "(set KHAA_N_KEY_WORDING or create key.local)."
                            )
                    # Decrypt sensitive fields if possible (backward-compatible with plaintext)
                    for conn in connections:
                        if isinstance(conn, dict):
                            if 'username' in conn:
                                conn['username'] = maybe_decrypt_field(conn.get('username', ''), self._fernet_key)
                            if 'password' in conn:
                                conn['password'] = maybe_decrypt_field(conn.get('password', ''), self._fernet_key)
                    return connections
            return []
        except Exception as e:
            print(f"Error loading config: {e}")
            return []
    
    def save_connections(self) -> bool:
        """Save connections to config.json"""
        try:
            # Write encrypted values to disk but keep in-memory values as plaintext
            serialized_connections: List[Dict] = []
            for conn in self.connections:
                if not isinstance(conn, dict):
                    serialized_connections.append(conn)
                    continue
                disk_conn = dict(conn)
                if 'username' in disk_conn:
                    disk_conn['username'] = maybe_encrypt_field(disk_conn.get('username', ''), self._fernet_key)
                if 'password' in disk_conn:
                    disk_conn['password'] = maybe_encrypt_field(disk_conn.get('password', ''), self._fernet_key)
                serialized_connections.append(disk_conn)

            config_data = {
                'connections': serialized_connections
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def add_connection(self, name: str, host: str, port: int, 
                      username: str = "", password: str = "") -> bool:
        """Add new connection"""
        try:
            new_connection = {
                'name': name,
                'host': host,
                'port': port,
                'username': username,
                'password': password
            }
            self.connections.append(new_connection)
            return self.save_connections()
        except Exception as e:
            print(f"Error adding connection: {e}")
            return False
    
    def remove_connection(self, name: str) -> bool:
        """Remove connection by name"""
        try:
            self.connections = [conn for conn in self.connections if conn['name'] != name]
            return self.save_connections()
        except Exception as e:
            print(f"Error removing connection: {e}")
            return False
    
    def get_connection(self, name: str) -> Optional[Dict]:
        """Get connection by name"""
        for conn in self.connections:
            if conn['name'] == name:
                return conn
        return None


class MongoDBClient:
    """Manage connection and operations with MongoDB"""
    
    def __init__(self, connection: Dict):
        self.connection = connection
        self.client = None
    
    def connect(self) -> bool:
        """Connect to MongoDB"""
        try:
            connection_string = self._build_connection_string()
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"Error connecting: {e}")
            return False
    
    def disconnect(self):
        """Close connection"""
        if self.client:
            self.client.close()
    
    def _build_connection_string(self) -> str:
        """Build connection string"""
        if self.connection['username'] and self.connection['password']:
            username = urllib.parse.quote_plus(self.connection['username'])
            password = urllib.parse.quote_plus(self.connection['password'])
            return f"mongodb://{username}:{password}@{self.connection['host']}:{self.connection['port']}/"
        else:
            return f"mongodb://{self.connection['host']}:{self.connection['port']}/"
    
    def test_connection(self) -> Dict:
        """Test connection"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}
            
            self.disconnect()
            
            return {
                'success': True,
                'message': 'Connected successfully'
            }
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def list_databases(self) -> Dict:
        """Get list of all databases"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}
            
            databases = sorted(self.client.list_database_names())
            
            self.disconnect()
            return {'success': True, 'databases': databases}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_collections(self, database_name: str) -> Dict:
        """Get list of collections in database"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}
            
            db = self.client[database_name]
            collections = sorted(list(db.list_collection_names()))
            
            self.disconnect()
            return {'success': True, 'collections': collections}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_collection_fields(self, database_name: str, collection_name: str) -> Dict:
        """Get list of fields in collection"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}
            
            db = self.client[database_name]
            collection = db[collection_name]
            
            # Get sample docs to find fields
            sample_docs = list(collection.find().limit(10))
            
            fields = set()
            for doc in sample_docs:
                fields.update(doc.keys())
            
            fields = sorted(list(fields))
            fields = sorted(list(fields))
            
            self.disconnect()
            return {'success': True, 'fields': fields}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_collection_data(self, database_name: str, collection_name: str, limit: int = 50,
                           skip: int = 0,
                           search_field: str = "", search_operator: str = "",
                           search_value: str = "") -> Dict:
        """Get collection data with optional search and pagination"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}
            
            db = self.client[database_name]
            collection = db[collection_name]
            
            query_filter = {}
            if search_field and search_operator and search_value:
                if search_operator == "=":
                    query_filter[search_field] = search_value
                elif search_operator == "like":
                    query_filter[search_field] = {"$regex": search_value, "$options": "i"}
            
            total = collection.count_documents(query_filter)
            cursor = collection.find(query_filter).sort("_id", 1).skip(skip).limit(limit)
            documents = list(cursor)
            
            # Convert ObjectId to string
            for doc in documents:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            
            self.disconnect()
            return {'success': True, 'data': documents, 'total': total}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}
            
    def get_document(self, database_name: str, collection_name: str, document_id: str) -> Dict:
        """Get single document by _id"""
        from bson.objectid import ObjectId
        from bson import json_util
        
        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}
                
            db = self.client[database_name]
            collection = db[collection_name]
            
            try:
                query_id = ObjectId(document_id)
            except Exception:
                query_id = document_id
                
            doc = collection.find_one({"_id": query_id})
            
            if not doc:
                self.disconnect()
                return {'success': False, 'message': 'Document not found'}
                
            doc_json_str = json_util.dumps(doc, ensure_ascii=False, indent=4)
            
            self.disconnect()
            return {'success': True, 'document_json': doc_json_str}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}

    def update_document(self, database_name: str, collection_name: str, document_id: str, document_json_str: str) -> Dict:
        """Update single document"""
        from bson.objectid import ObjectId
        from bson import json_util
        
        try:
            if not self.connect():
                print("[DEBUG] update_document: Connection failed")
                return {'success': False, 'message': 'Could not connect'}
                
            db = self.client[database_name]
            collection = db[collection_name]
            
            print(f"[DEBUG] update_document: db={database_name}, col={collection_name}, id={document_id}")
            
            try:
                update_data = json_util.loads(document_json_str)
            except Exception as e:
                self.disconnect()
                return {'success': False, 'message': f'Invalid JSON format: {str(e)}'}
                
            try:
                query_id = ObjectId(document_id)
            except Exception:
                query_id = document_id
                
            if "_id" in update_data:
                del update_data["_id"]
            
            result = collection.replace_one({"_id": query_id}, update_data)
            print(f"[DEBUG] update_document: replaced! matched={result.matched_count}, modified={result.modified_count}")
            
            self.disconnect()
            
            if result.matched_count == 0:
                return {'success': False, 'message': 'Document not found for update'}
                
            return {'success': True, 'message': 'Document updated successfully'}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}

    def update_document_field(self, database_name: str, collection_name: str, document_id: str, field_key: str, field_value_json_str: str) -> Dict:
        """Update single field of document"""
        from bson.objectid import ObjectId
        from bson import json_util
        
        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}
                
            db = self.client[database_name]
            collection = db[collection_name]
            
            # Parse value from JSON string
            try:
                field_value = json_util.loads(field_value_json_str)
            except Exception as e:
                self.disconnect()
                return {'success': False, 'message': f'Invalid JSON format: {str(e)}'}
            
            # Parse document_id
            try:
                query_id = ObjectId(document_id)
            except Exception:
                query_id = document_id
            
            # Use $set to update single field
            result = collection.update_one(
                {"_id": query_id},
                {"$set": {field_key: field_value}}
            )
            
            self.disconnect()
            
            if result.matched_count == 0:
                return {'success': False, 'message': 'Document not found for update'}
                
            return {'success': True, 'message': f'Field "{field_key}" updated successfully'}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}

    def unset_document_field(self, database_name: str, collection_name: str, document_id: str, field_key: str) -> Dict:
        """Remove a single field from document using $unset"""
        from bson.objectid import ObjectId

        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}

            db = self.client[database_name]
            collection = db[collection_name]

            try:
                query_id = ObjectId(document_id)
            except Exception:
                query_id = document_id

            result = collection.update_one(
                {"_id": query_id},
                {"$unset": {field_key: ""}}
            )

            self.disconnect()

            if result.matched_count == 0:
                return {'success': False, 'message': 'Document not found for unset'}

            return {'success': True, 'message': f'Field "{field_key}" removed successfully'}

        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}

    def clear_collection(self, database_name: str, collection_name: str, confirm_collection_name: str) -> Dict:
        """Clear all data in collection"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}
            
            if collection_name != confirm_collection_name:
                self.disconnect()
                return {'success': False, 'message': f'Collection name incorrect. Please enter "{collection_name}" exactly'}
            
            db = self.client[database_name]
            collection = db[collection_name]
            
            result = collection.delete_many({})
            
            self.disconnect()
            return {
                'success': True, 
                'message': f'Cleared collection "{collection_name}" ({result.deleted_count} documents deleted)'
            }
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def create_database(self, database_name: str, collection_name: str) -> Dict:
        """Create a new database by creating an initial collection"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}
            
            db = self.client[database_name]
            # Check if database exists
            if database_name in self.client.list_database_names():
                if collection_name in db.list_collection_names():
                    self.disconnect()
                    return {'success': False, 'message': f'Collection "{collection_name}" already exists in database "{database_name}"'}
            
            db.create_collection(collection_name)
            
            self.disconnect()
            return {'success': True, 'message': f'Database "{database_name}" created with collection "{collection_name}"'}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}

    def drop_collections(self, database_name: str, collection_names: List[str]) -> Dict:
        """Drop selected collections"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}
            
            if not collection_names:
                return {'success': False, 'message': 'No collections selected for delete'}
            
            db = self.client[database_name]
            dropped = []
            errors = []
            
            for name in collection_names:
                try:
                    db.drop_collection(name)
                    dropped.append(name)
                except Exception as e:
                    errors.append(f'{name}: {str(e)}')
            
            self.disconnect()
            
            if errors:
                return {
                    'success': len(dropped) > 0,
                    'message': f'Deleted {len(dropped)} collections, failed {len(errors)} collections\n' + '\n'.join(errors),
                    'dropped': dropped
                }
            
            return {
                'success': True,
                'message': f'Deleted {len(dropped)} collections: {", ".join(dropped)}',
                'dropped': dropped
            }
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def import_collection(self, database_name: str, collection_name: str, documents: list) -> Dict:
        """Import data from JSON into new collection"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}
            
            if not documents:
                return {'success': False, 'message': 'No data in JSON file'}
            
            db = self.client[database_name]
            collection = db[collection_name]
            
            if isinstance(documents, dict):
                documents = [documents]
            
            result = collection.insert_many(documents)
            
            self.disconnect()
            
            return {
                'success': True,
                'message': f'Imported {len(result.inserted_ids)} items into collection "{collection_name}"',
                'count': len(result.inserted_ids)
            }
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}

    def export_collections(self, database_name: str, collection_names: List[str], export_dir: str) -> Dict:
        """Export collections to JSON files"""
        from bson import json_util
        import json
        import os
        
        try:
            if not self.connect():
                return {'success': False, 'message': 'Could not connect'}
            
            if not collection_names:
                return {'success': False, 'message': 'No collections selected for export'}
                
            if not os.path.exists(export_dir):
                return {'success': False, 'message': f'Destination folder not found: {export_dir}'}
            
            db = self.client[database_name]
            results = []
            errors = []
            
            for name in collection_names:
                try:
                    collection = db[name]
                    documents = list(collection.find())
                    
                    if not documents:
                        errors.append(f'{name}: No data in collection')
                        continue
                        
                    file_path = os.path.join(export_dir, f"{name}.json")
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        # Use json_util.dumps for BSON types (ObjectId, datetime)
                        json_str = json_util.dumps(documents, indent=4, ensure_ascii=False)
                        f.write(json_str)
                        
                    results.append(name)
                except Exception as e:
                    errors.append(f'{name}: {str(e)}')
            
            self.disconnect()
            
            if errors:
                return {
                    'success': len(results) > 0,
                    'message': f'Exported {len(results)} collections, failed {len(errors)} collections\n' + '\n'.join(errors),
                    'results': results
                }
            
            return {
                'success': True,
                'message': f'Exported {len(results)} collections to:\n{export_dir}',
                'results': results
            }
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'Error: {str(e)}'}