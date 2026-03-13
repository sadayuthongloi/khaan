import eel
from database_manager import MongoDBConnectionManager, MongoDBClient


# ตั้งค่า Eel
eel.init('html')

# สร้าง instance ของ managers
connection_manager = MongoDBConnectionManager()


# Eel functions สำหรับ JavaScript
@eel.expose
def get_connections():
    """ส่งข้อมูล connections ทั้งหมดไปยัง JavaScript"""
    return connection_manager.connections


@eel.expose
def add_new_connection(name: str, host: str, port: int, 
                      username: str = "", password: str = ""):
    """เพิ่ม connection ใหม่จาก JavaScript"""
    success = connection_manager.add_connection(name, host, port, username, password)
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
                'message': 'เชื่อมต่อสำเร็จ'
            }
        else:
            return {'success': False, 'message': f'ไม่สามารถเชื่อมต่อได้: {result["message"]}'}
            
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


@eel.expose
def get_databases(connection_name: str):
    """ดึงรายการฐานข้อมูลทั้งหมด"""
    try:
        # หา connection
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        # ดึงรายการฐานข้อมูล
        client = MongoDBClient(connection)
        return client.list_databases()
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


@eel.expose
def get_collections(connection_name: str, database_name: str):
    """ดึงรายการ collections ในฐานข้อมูล"""
    try:
        # หา connection
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        # ดึง collections
        client = MongoDBClient(connection)
        return client.get_collections(database_name)
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


@eel.expose
def get_collection_data(connection_name: str, database_name: str, collection_name: str, limit: int = 50, 
                        search_field: str = "", search_operator: str = "", search_value: str = ""):
    """ดึงข้อมูลใน collection พร้อม search"""
    try:
        # หา connection
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        # ดึงข้อมูล
        client = MongoDBClient(connection)
        return client.get_collection_data(database_name, collection_name, limit, search_field, search_operator, search_value)
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}

@eel.expose
def get_document(connection_name: str, database_name: str, collection_name: str, document_id: str):
    """ดึงข้อมูลเอกสาร 1 รายการตาม _id"""
    try:
        connection = connection_manager.get_connection(connection_name)
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
            
        client = MongoDBClient(connection)
        return client.get_document(database_name, collection_name, document_id)
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}

@eel.expose
def update_document(connection_name: str, database_name: str, collection_name: str, document_id: str, document_json_str: str):
    """อัปเดตข้อมูลเอกสาร 1 รายการ"""
    try:
        connection = connection_manager.get_connection(connection_name)
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
            
        client = MongoDBClient(connection)
        return client.update_document(database_name, collection_name, document_id, document_json_str)
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


@eel.expose
def update_document_field(connection_name: str, database_name: str, collection_name: str, document_id: str, field_key: str, field_value_json_str: str):
    """อัปเดตเฉพาะ field เดียวของเอกสาร"""
    try:
        connection = connection_manager.get_connection(connection_name)
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
            
        client = MongoDBClient(connection)
        return client.update_document_field(database_name, collection_name, document_id, field_key, field_value_json_str)
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


@eel.expose
def get_collection_fields(connection_name: str, database_name: str, collection_name: str):
    """ดึงรายการ fields ใน collection"""
    try:
        # หา connection
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        # ดึง fields
        client = MongoDBClient(connection)
        return client.get_collection_fields(database_name, collection_name)
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}




@eel.expose
def clear_collection(connection_name: str, database_name: str, collection_name: str, confirm_collection_name: str):
    """ล้างข้อมูลใน collection"""
    try:
        # หา connection
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        # ล้างข้อมูลใน collection
        client = MongoDBClient(connection)
        return client.clear_collection(database_name, collection_name, confirm_collection_name)
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


@eel.expose
def drop_collections(connection_name: str, database_name: str, collection_names: list):
    """ลบ collections ที่เลือก"""
    try:
        # หา connection
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        # ลบ collections
        client = MongoDBClient(connection)
        return client.drop_collections(database_name, collection_names)
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


@eel.expose
def import_collection(connection_name: str, database_name: str):
    """นำเข้า collection จากไฟล์ JSON (รองรับหลายไฟล์)"""
    import json
    import os
    import tkinter as tk
    from tkinter import filedialog
    from bson import json_util
    
    try:
        # เปิด file dialog เพื่อเลือกไฟล์ JSON (หลายไฟล์)
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        file_paths = filedialog.askopenfilenames(
            title='เลือกไฟล์ JSON เพื่อนำเข้า (เลือกได้หลายไฟล์)',
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')]
        )
        
        root.destroy()
        
        if not file_paths:
            return {'success': False, 'message': 'ไม่ได้เลือกไฟล์'}
        
        # หา connection
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        results = []
        errors = []
        
        for file_path in file_paths:
            try:
                # อ่านชื่อไฟล์เป็นชื่อ collection
                collection_name = os.path.splitext(os.path.basename(file_path))[0]
                
                # อ่านไฟล์ JSON - รองรับทั้ง JSON array และ JSONL (หนึ่ง JSON ต่อบรรทัด)
                documents = []
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                    if content.startswith('['):
                        # JSON array format
                        documents = json_util.loads(content)
                    else:
                        # JSONL format (one JSON per line)
                        for line in content.split('\n'):
                            line = line.strip()
                            if line:
                                documents.append(json_util.loads(line))
                
                # นำเข้าข้อมูล
                client = MongoDBClient(connection)
                result = client.import_collection(database_name, collection_name, documents)
                
                if result['success']:
                    results.append(f'{collection_name}: {result["count"]} รายการ')
                else:
                    errors.append(f'{collection_name}: {result["message"]}')
                    
            except json.JSONDecodeError as e:
                errors.append(f'{os.path.basename(file_path)}: ไฟล์ JSON ไม่ถูกต้อง')
            except Exception as e:
                errors.append(f'{os.path.basename(file_path)}: {str(e)}')
        
        # สร้างข้อความสรุป
        message_parts = []
        if results:
            message_parts.append(f'นำเข้าสำเร็จ {len(results)} ไฟล์:\n' + '\n'.join(results))
        if errors:
            message_parts.append(f'ล้มเหลว {len(errors)} ไฟล์:\n' + '\n'.join(errors))
        
        return {
            'success': len(results) > 0,
            'message': '\n\n'.join(message_parts),
            'imported': len(results),
            'failed': len(errors)
        }
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}

@eel.expose
def export_collections(connection_name: str, database_name: str, collection_names: list):
    """ส่งออก collections เป็นไฟล์ JSON"""
    import tkinter as tk
    from tkinter import filedialog
    import os
    
    try:
        # หา connection ก่อนเพื่อไม่ให้เสียเวลาถ้าไม่มี
        connection = connection_manager.get_connection(connection_name)
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
            
        if not collection_names:
            return {'success': False, 'message': 'ไม่ได้เลือก collection ที่ต้องการส่งออก'}
            
        # เปิด file dialog เพื่อเลือกโฟลเดอร์สำหรับบันทึก
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        export_dir = filedialog.askdirectory(
            title=f'เลือกโฟลเดอร์สำหรับบันทึก {len(collection_names)} collections'
        )
        
        root.destroy()
        
        if not export_dir:
            return {'success': False, 'message': 'ยกเลิกการส่งออก'}
            
        # เริ่มการส่งออก
        client = MongoDBClient(connection)
        return client.export_collections(database_name, collection_names, export_dir)
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}

@eel.expose
def open_mongodb_folder():
    """เปิดโฟลเดอร์ MongoDB Server ใน Windows Explorer"""
    import os
    import platform
    import subprocess
    
    path = r"C:\Program Files\MongoDB\Server"
    try:
        if platform.system() == "Windows":
            if os.path.exists(path):
                os.startfile(path)
                return {'success': True, 'message': 'เปิดโฟลเดอร์สำเร็จ'}
            else:
                return {'success': False, 'message': f'ไม่พบโฟลเดอร์ {path}'}
        else:
            return {'success': False, 'message': 'ฟีเจอร์นี้รองรับเฉพาะ Windows'}
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}


def main():
    """ฟังก์ชันหลักสำหรับรันแอปพลิเคชัน"""
    # เริ่มต้น Eel application (serve ไฟล์จากโฟลเดอร์ html/ โดยตรง)
    print("กำลังเริ่มต้น MongoDB Connection Manager...")
    print("เปิดเบราว์เซอร์ที่: http://localhost:8000")

    try:
        eel.start('index.html', size=(1200, 800), port=8000)
    except (SystemExit, MemoryError, KeyboardInterrupt):
        print("ปิดแอปพลิเคชัน...")



if __name__ == "__main__":
    main()
