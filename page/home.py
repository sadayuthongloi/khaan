"""
MongoDB Connection Manager - Main Application
แอปพลิเคชันหลักสำหรับจัดการการเชื่อมต่อ MongoDB
"""

import eel
from database_manager import MongoDBConnectionManager, MongoDBClient
from html_generator import HTMLGenerator


# ตั้งค่า Eel
eel.init('html')

# สร้าง instance ของ managers
connection_manager = MongoDBConnectionManager()
html_generator = HTMLGenerator()


# Eel functions สำหรับ JavaScript
@eel.expose
def get_connections():
    """ส่งข้อมูล connections ทั้งหมดไปยัง JavaScript"""
    return connection_manager.connections


@eel.expose
def add_new_connection(name: str, host: str, port: int, database: str, 
                      username: str = "", password: str = ""):
    """เพิ่ม connection ใหม่จาก JavaScript"""
    success = connection_manager.add_connection(name, host, port, database, username, password)
    return {
        'success': success,
        'message': 'เพิ่ม connection สำเร็จ' if success else 'เกิดข้อผิดพลาดในการเพิ่ม connection'
    }


@eel.expose
def delete_connection(name: str):
    """ลบ connection จาก JavaScript"""
    success = connection_manager.remove_connection(name)
    return {
        'success': success,
        'message': 'ลบ connection สำเร็จ' if success else 'เกิดข้อผิดพลาดในการลบ connection'
    }


@eel.expose
def test_connection(name: str):
    """ทดสอบการเชื่อมต่อ MongoDB"""
    try:
        # หา connection ตามชื่อ
        connection = connection_manager.get_connection(name)
        
        if not connection:
            return {'success': False, 'message': '❌ ไม่พบ connection ที่ระบุ'}
        
        # ทดสอบการเชื่อมต่อ
        client = MongoDBClient(connection)
        result = client.test_connection()
        
        if result['success']:
            return {
                'success': True, 
                'message': f'✅ เชื่อมต่อ {name} สำเร็จ\n📍 {connection["host"]}:{connection["port"]}\n🗄️ ฐานข้อมูล: {connection["database"]}'
            }
        else:
            return {'success': False, 'message': f'❌ การเชื่อมต่อล้มเหลว\n📍 {connection["host"]}:{connection["port"]}\n🔍 ข้อผิดพลาด: {result["message"]}'}
            
    except Exception as e:
        return {'success': False, 'message': f'❌ เกิดข้อผิดพลาดในการทดสอบ: {str(e)}'}


@eel.expose
def use_connection(name: str):
    """เข้าใช้งาน connection และไปยังหน้า main"""
    try:
        # หา connection ตามชื่อ
        connection = connection_manager.get_connection(name)
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        # ทดสอบการเชื่อมต่อก่อน
        client = MongoDBClient(connection)
        result = client.test_connection()
        
        if result['success']:
            return {
                'success': True, 
                'connection': connection,
                'database_exists': result.get('database_exists', False),
                'message': 'เชื่อมต่อสำเร็จ'
            }
        else:
            return {'success': False, 'message': f'ไม่สามารถเชื่อมต่อได้: {result["message"]}'}
            
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


@eel.expose
def get_collections(connection_name: str):
    """ดึงรายการ collections ในฐานข้อมูล"""
    try:
        # หา connection
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        # ดึง collections
        client = MongoDBClient(connection)
        return client.get_collections()
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


@eel.expose
def get_collection_data(connection_name: str, collection_name: str, limit: int = 50, 
                        search_field: str = "", search_operator: str = "", search_value: str = ""):
    """ดึงข้อมูลใน collection พร้อม search"""
    try:
        # หา connection
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        # ดึงข้อมูล
        client = MongoDBClient(connection)
        return client.get_collection_data(collection_name, limit, search_field, search_operator, search_value)
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


@eel.expose
def get_collection_fields(connection_name: str, collection_name: str):
    """ดึงรายการ fields ใน collection"""
    try:
        # หา connection
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        # ดึง fields
        client = MongoDBClient(connection)
        return client.get_collection_fields(collection_name)
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


@eel.expose
def create_database(connection_name: str, database_name: str):
    """สร้างฐานข้อมูลใหม่"""
    try:
        # หา connection
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        # สร้างฐานข้อมูล
        client = MongoDBClient(connection)
        return client.create_database(database_name)
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


def main():
    """ฟังก์ชันหลักสำหรับรันแอปพลิเคชัน"""
    # สร้าง HTML interface
    html_generator.generate_index_html()
    html_generator.generate_main_html()
    
    # เริ่มต้น Eel application
    print("กำลังเริ่มต้น MongoDB Connection Manager...")
    print("เปิดเบราว์เซอร์ที่: http://localhost:8000")
    
    try:
        eel.start('index.html', size=(1200, 800), port=8000)
    except (SystemExit, MemoryError, KeyboardInterrupt):
        print("ปิดแอปพลิเคชัน...")


if __name__ == "__main__":
    main()
