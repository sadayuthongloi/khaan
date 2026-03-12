"""
MongoDB Database Manager
จัดการการเชื่อมต่อและดำเนินการกับฐานข้อมูล MongoDB
"""

import json
import os
import urllib.parse
from typing import Dict, List, Optional
from pymongo import MongoClient


class MongoDBConnectionManager:
    """จัดการการเชื่อมต่อ MongoDB"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.connections = self.load_connections()
    
    def load_connections(self) -> List[Dict]:
        """โหลด connections จากไฟล์ config.json"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('connections', [])
            return []
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการโหลด config: {e}")
            return []
    
    def save_connections(self) -> bool:
        """บันทึก connections ลงไฟล์ config.json"""
        try:
            config_data = {
                'connections': self.connections
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการบันทึก config: {e}")
            return False
    
    def add_connection(self, name: str, host: str, port: int, 
                      username: str = "", password: str = "") -> bool:
        """เพิ่ม connection ใหม่"""
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
            print(f"เกิดข้อผิดพลาดในการเพิ่ม connection: {e}")
            return False
    
    def remove_connection(self, name: str) -> bool:
        """ลบ connection ตามชื่อ"""
        try:
            self.connections = [conn for conn in self.connections if conn['name'] != name]
            return self.save_connections()
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการลบ connection: {e}")
            return False
    
    def get_connection(self, name: str) -> Optional[Dict]:
        """ดึงข้อมูล connection ตามชื่อ"""
        for conn in self.connections:
            if conn['name'] == name:
                return conn
        return None


class MongoDBClient:
    """จัดการการเชื่อมต่อและดำเนินการกับ MongoDB"""
    
    def __init__(self, connection: Dict):
        self.connection = connection
        self.client = None
    
    def connect(self) -> bool:
        """เชื่อมต่อกับ MongoDB"""
        try:
            connection_string = self._build_connection_string()
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            # ทดสอบการเชื่อมต่อ
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
            return False
    
    def disconnect(self):
        """ปิดการเชื่อมต่อ"""
        if self.client:
            self.client.close()
    
    def _build_connection_string(self) -> str:
        """สร้าง connection string"""
        if self.connection['username'] and self.connection['password']:
            username = urllib.parse.quote_plus(self.connection['username'])
            password = urllib.parse.quote_plus(self.connection['password'])
            return f"mongodb://{username}:{password}@{self.connection['host']}:{self.connection['port']}/"
        else:
            return f"mongodb://{self.connection['host']}:{self.connection['port']}/"
    
    def test_connection(self) -> Dict:
        """ทดสอบการเชื่อมต่อ"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            self.disconnect()
            
            return {
                'success': True,
                'message': 'เชื่อมต่อสำเร็จ'
            }
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}
    
    def list_databases(self) -> Dict:
        """ดึงรายการฐานข้อมูลทั้งหมด"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            databases = sorted(self.client.list_database_names())
            
            self.disconnect()
            return {'success': True, 'databases': databases}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}
    
    def get_collections(self, database_name: str) -> Dict:
        """ดึงรายการ collections ในฐานข้อมูล"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            db = self.client[database_name]
            collections = sorted(list(db.list_collection_names()))
            
            self.disconnect()
            return {'success': True, 'collections': collections}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}
    
    def get_collection_fields(self, database_name: str, collection_name: str) -> Dict:
        """ดึงรายการ fields ใน collection"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            db = self.client[database_name]
            collection = db[collection_name]
            
            # ดึงข้อมูลตัวอย่างเพื่อหา fields
            sample_docs = list(collection.find().limit(10))
            
            # รวบรวม fields ทั้งหมด
            fields = set()
            for doc in sample_docs:
                fields.update(doc.keys())
            
            # เรียงลำดับ fields ตามตัวอักษร
            fields = sorted(list(fields))
            
            self.disconnect()
            return {'success': True, 'fields': fields}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}
    
    def get_collection_data(self, database_name: str, collection_name: str, limit: int = 50, 
                           search_field: str = "", search_operator: str = "", 
                           search_value: str = "") -> Dict:
        """ดึงข้อมูลใน collection พร้อม search"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            db = self.client[database_name]
            collection = db[collection_name]
            
            # สร้าง query filter
            query_filter = {}
            if search_field and search_operator and search_value:
                if search_operator == "=":
                    # ค้นหาแบบเท่ากับ
                    query_filter[search_field] = search_value
                elif search_operator == "like":
                    # ค้นหาแบบ like (regex)
                    query_filter[search_field] = {"$regex": search_value, "$options": "i"}
            
            # ดึงข้อมูล
            documents = list(collection.find(query_filter).limit(limit))
            
            # แปลง ObjectId เป็น string
            for doc in documents:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            
            self.disconnect()
            return {'success': True, 'data': documents}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}
            
    def get_document(self, database_name: str, collection_name: str, document_id: str) -> Dict:
        """ดึงข้อมูลเอกสาร 1 รายการตาม _id"""
        from bson.objectid import ObjectId
        from bson import json_util
        
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
                
            db = self.client[database_name]
            collection = db[collection_name]
            
            try:
                query_id = ObjectId(document_id)
            except Exception:
                query_id = document_id
                
            doc = collection.find_one({"_id": query_id})
            
            if not doc:
                self.disconnect()
                return {'success': False, 'message': 'ไม่พบเอกสารนี้'}
                
            doc_json_str = json_util.dumps(doc, ensure_ascii=False, indent=4)
            
            self.disconnect()
            return {'success': True, 'document_json': doc_json_str}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}

    def update_document(self, database_name: str, collection_name: str, document_id: str, document_json_str: str) -> Dict:
        """อัปเดตข้อมูลเอกสาร 1 รายการ"""
        from bson.objectid import ObjectId
        from bson import json_util
        
        try:
            if not self.connect():
                print("[DEBUG] update_document: Connection failed")
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
                
            db = self.client[database_name]
            collection = db[collection_name]
            
            print(f"[DEBUG] update_document: db={database_name}, col={collection_name}, id={document_id}")
            
            try:
                update_data = json_util.loads(document_json_str)
            except Exception as e:
                self.disconnect()
                return {'success': False, 'message': f'รูปแบบ JSON ไม่ถูกต้อง: {str(e)}'}
                
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
                return {'success': False, 'message': 'ไม่พบเอกสารนี้ในการอัปเดต'}
                
            return {'success': True, 'message': 'อัปเดตข้อมูลสำเร็จ'}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}
    

    
    def clear_collection(self, database_name: str, collection_name: str, confirm_collection_name: str) -> Dict:
        """ล้างข้อมูลใน collection"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            # ตรวจสอบว่าชื่อ collection ที่ยืนยันถูกต้องหรือไม่
            if collection_name != confirm_collection_name:
                self.disconnect()
                return {'success': False, 'message': f'ชื่อ collection ไม่ถูกต้อง กรุณากรอก "{collection_name}" ให้ถูกต้อง'}
            
            db = self.client[database_name]
            collection = db[collection_name]
            
            # ล้างข้อมูลทั้งหมดใน collection
            result = collection.delete_many({})
            
            self.disconnect()
            return {
                'success': True, 
                'message': f'ล้างข้อมูลใน collection "{collection_name}" สำเร็จ (ลบ {result.deleted_count} เอกสาร)'
            }
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}
    
    def drop_collections(self, database_name: str, collection_names: List[str]) -> Dict:
        """ลบ collections ที่เลือก (drop)"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            if not collection_names:
                return {'success': False, 'message': 'ไม่ได้เลือก collection ที่ต้องการลบ'}
            
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
                    'message': f'ลบสำเร็จ {len(dropped)} collections, ล้มเหลว {len(errors)} collections\n' + '\n'.join(errors),
                    'dropped': dropped
                }
            
            return {
                'success': True,
                'message': f'ลบ {len(dropped)} collections สำเร็จ: {", ".join(dropped)}',
                'dropped': dropped
            }
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}
    
    def import_collection(self, database_name: str, collection_name: str, documents: list) -> Dict:
        """นำเข้าข้อมูลจาก JSON เป็น collection ใหม่"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            if not documents:
                return {'success': False, 'message': 'ไม่มีข้อมูลในไฟล์ JSON'}
            
            db = self.client[database_name]
            collection = db[collection_name]
            
            # ถ้า documents เป็น dict เดี่ยว ให้แปลงเป็น list
            if isinstance(documents, dict):
                documents = [documents]
            
            result = collection.insert_many(documents)
            
            self.disconnect()
            
            return {
                'success': True,
                'message': f'นำเข้าข้อมูลสำเร็จ {len(result.inserted_ids)} รายการ ไปยัง collection "{collection_name}"',
                'count': len(result.inserted_ids)
            }
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}

    def export_collections(self, database_name: str, collection_names: List[str], export_dir: str) -> Dict:
        """ส่งออก collections เป็นไฟล์ JSON"""
        from bson import json_util
        import json
        import os
        
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            if not collection_names:
                return {'success': False, 'message': 'ไม่ได้เลือก collection ที่ต้องการส่งออก'}
                
            if not os.path.exists(export_dir):
                return {'success': False, 'message': f'ไม่พบโฟลเดอร์ปลายทาง: {export_dir}'}
            
            db = self.client[database_name]
            results = []
            errors = []
            
            for name in collection_names:
                try:
                    collection = db[name]
                    # ดึงข้อมูลทั้งหมด
                    documents = list(collection.find())
                    
                    if not documents:
                        errors.append(f'{name}: ไม่มีข้อมูลใน collection')
                        continue
                        
                    # สร้าง path ไฟล์
                    file_path = os.path.join(export_dir, f"{name}.json")
                    
                    # บันทึกเป็น JSON format (array) พร้อม format ที่สวยงาม
                    with open(file_path, 'w', encoding='utf-8') as f:
                        # ใช้ json_util.dumps เพื่อจัดการโครงสร้างแบบ BSON (เช่น ObjectId, datetime) ให้เป็น JSON มาตรฐาน
                        json_str = json_util.dumps(documents, indent=4, ensure_ascii=False)
                        f.write(json_str)
                        
                    results.append(name)
                except Exception as e:
                    errors.append(f'{name}: {str(e)}')
            
            self.disconnect()
            
            if errors:
                return {
                    'success': len(results) > 0,
                    'message': f'ส่งออกสำเร็จ {len(results)} collections, ล้มเหลว {len(errors)} collections\n' + '\n'.join(errors),
                    'results': results
                }
            
            return {
                'success': True,
                'message': f'ส่งออก {len(results)} collectionsสำเร็จไปยัง:\n{export_dir}',
                'results': results
            }
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}