"""
MongoDB Database Manager
จัดการการเชื่อมต่อและดำเนินการกับฐานข้อมูล MongoDB
"""

import json
import os
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
    
    def add_connection(self, name: str, host: str, port: int, database: str, 
                      username: str = "", password: str = "") -> bool:
        """เพิ่ม connection ใหม่"""
        try:
            new_connection = {
                'name': name,
                'host': host,
                'port': port,
                'database': database,
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
            return f"mongodb://{self.connection['username']}:{self.connection['password']}@{self.connection['host']}:{self.connection['port']}/"
        else:
            return f"mongodb://{self.connection['host']}:{self.connection['port']}/"
    
    def test_connection(self) -> Dict:
        """ทดสอบการเชื่อมต่อ"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            # ตรวจสอบว่าฐานข้อมูลมีอยู่หรือไม่
            db_name = self.connection['database']
            database_exists = db_name in self.client.list_database_names()
            
            self.disconnect()
            
            return {
                'success': True,
                'database_exists': database_exists,
                'message': 'เชื่อมต่อสำเร็จ'
            }
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}
    
    def get_collections(self) -> Dict:
        """ดึงรายการ collections ในฐานข้อมูล"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            db = self.client[self.connection['database']]
            collections = sorted(list(db.list_collection_names()))
            
            self.disconnect()
            return {'success': True, 'collections': collections}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}
    
    def get_collection_fields(self, collection_name: str) -> Dict:
        """ดึงรายการ fields ใน collection"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            db = self.client[self.connection['database']]
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
    
    def get_collection_data(self, collection_name: str, limit: int = 50, 
                           search_field: str = "", search_operator: str = "", 
                           search_value: str = "") -> Dict:
        """ดึงข้อมูลใน collection พร้อม search"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            db = self.client[self.connection['database']]
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
    
    def create_database(self, database_name: str) -> Dict:
        """สร้างฐานข้อมูลใหม่"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            db = self.client[database_name]
            
            # สร้าง collection เปล่าเพื่อให้ฐานข้อมูลถูกสร้าง
            db.create_collection('temp_collection')
            db.drop_collection('temp_collection')
            
            self.disconnect()
            return {'success': True, 'message': f'สร้างฐานข้อมูล {database_name} สำเร็จ'}
            
        except Exception as e:
            self.disconnect()
            return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}
    
    def clear_collection(self, collection_name: str, confirm_collection_name: str) -> Dict:
        """ล้างข้อมูลใน collection"""
        try:
            if not self.connect():
                return {'success': False, 'message': 'ไม่สามารถเชื่อมต่อได้'}
            
            # ตรวจสอบว่าชื่อ collection ที่ยืนยันถูกต้องหรือไม่
            if collection_name != confirm_collection_name:
                self.disconnect()
                return {'success': False, 'message': f'ชื่อ collection ไม่ถูกต้อง กรุณากรอก "{collection_name}" ให้ถูกต้อง'}
            
            db = self.client[self.connection['database']]
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