import eel
import json
import os
from typing import Dict, List, Optional

# ตั้งค่า Eel
eel.init('html')

class MongoDBConnectionManager:
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
    
    def save_connections(self):
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

# สร้าง instance ของ connection manager
connection_manager = MongoDBConnectionManager()

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
        connection = None
        for conn in connection_manager.connections:
            if conn['name'] == name:
                connection = conn
                break
        
        if not connection:
            return {'success': False, 'message': '❌ ไม่พบ connection ที่ระบุ'}
        
        # ทดสอบการเชื่อมต่อจริงด้วย pymongo
        try:
            from pymongo import MongoClient
            
            # สร้าง connection string
            if connection['username'] and connection['password']:
                # มี authentication
                connection_string = f"mongodb://{connection['username']}:{connection['password']}@{connection['host']}:{connection['port']}/"
            else:
                # ไม่มี authentication
                connection_string = f"mongodb://{connection['host']}:{connection['port']}/"
            
            # ทดสอบการเชื่อมต่อ
            client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            client.close()
            
            return {'success': True, 'message': f'✅ เชื่อมต่อ {name} สำเร็จ\n📍 {connection["host"]}:{connection["port"]}\n🗄️ ฐานข้อมูล: {connection["database"]}'}
            
        except ImportError:
            # กรณีที่ไม่ได้ติดตั้ง pymongo
            return {'success': True, 'message': f'✅ การตั้งค่า {name} ถูกต้อง\n📍 {connection["host"]}:{connection["port"]}\n🗄️ ฐานข้อมูล: {connection["database"]}\n⚠️ หมายเหตุ: ต้องติดตั้ง pymongo เพื่อทดสอบการเชื่อมต่อจริง'}
            
        except Exception as e:
            return {'success': False, 'message': f'❌ การเชื่อมต่อล้มเหลว\n📍 {connection["host"]}:{connection["port"]}\n🔍 ข้อผิดพลาด: {str(e)}'}
            
    except Exception as e:
        return {'success': False, 'message': f'❌ เกิดข้อผิดพลาดในการทดสอบ: {str(e)}'}

@eel.expose
def use_connection(name: str):
    """เข้าใช้งาน connection และไปยังหน้า main"""
    try:
        # หา connection ตามชื่อ
        connection = None
        for conn in connection_manager.connections:
            if conn['name'] == name:
                connection = conn
                break
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        # ทดสอบการเชื่อมต่อก่อน
        try:
            from pymongo import MongoClient
            
            # สร้าง connection string
            if connection['username'] and connection['password']:
                connection_string = f"mongodb://{connection['username']}:{connection['password']}@{connection['host']}:{connection['port']}/"
            else:
                connection_string = f"mongodb://{connection['host']}:{connection['port']}/"
            
            # ทดสอบการเชื่อมต่อ
            client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            
            # ตรวจสอบว่าฐานข้อมูลมีอยู่หรือไม่
            db_name = connection['database']
            database_exists = db_name in client.list_database_names()
            
            client.close()
            
            return {
                'success': True, 
                'connection': connection,
                'database_exists': database_exists,
                'message': 'เชื่อมต่อสำเร็จ'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'ไม่สามารถเชื่อมต่อได้: {str(e)}'}
            
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}

@eel.expose
def get_collections(connection_name: str):
    """ดึงรายการ collections ในฐานข้อมูล"""
    try:
        # หา connection
        connection = None
        for conn in connection_manager.connections:
            if conn['name'] == connection_name:
                connection = conn
                break
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        from pymongo import MongoClient
        
        # สร้าง connection string
        if connection['username'] and connection['password']:
            connection_string = f"mongodb://{connection['username']}:{connection['password']}@{connection['host']}:{connection['port']}/"
        else:
            connection_string = f"mongodb://{connection['host']}:{connection['port']}/"
        
        client = MongoClient(connection_string)
        db = client[connection['database']]
        
        # ดึงรายการ collections และเรียงลำดับตามตัวอักษร
        collections = sorted(list(db.list_collection_names()))
        
        client.close()
        
        return {'success': True, 'collections': collections}
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}

@eel.expose
def get_collection_data(connection_name: str, collection_name: str, limit: int = 50, search_field: str = "", search_operator: str = "", search_value: str = ""):
    """ดึงข้อมูลใน collection พร้อม search"""
    try:
        # หา connection
        connection = None
        for conn in connection_manager.connections:
            if conn['name'] == connection_name:
                connection = conn
                break
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        from pymongo import MongoClient
        import re
        
        # สร้าง connection string
        if connection['username'] and connection['password']:
            connection_string = f"mongodb://{connection['username']}:{connection['password']}@{connection['host']}:{connection['port']}/"
        else:
            connection_string = f"mongodb://{connection['host']}:{connection['port']}/"
        
        client = MongoClient(connection_string)
        db = client[connection['database']]
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
        
        client.close()
        
        return {'success': True, 'data': documents}
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}

@eel.expose
def get_collection_fields(connection_name: str, collection_name: str):
    """ดึงรายการ fields ใน collection"""
    try:
        # หา connection
        connection = None
        for conn in connection_manager.connections:
            if conn['name'] == connection_name:
                connection = conn
                break
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        from pymongo import MongoClient
        
        # สร้าง connection string
        if connection['username'] and connection['password']:
            connection_string = f"mongodb://{connection['username']}:{connection['password']}@{connection['host']}:{connection['port']}/"
        else:
            connection_string = f"mongodb://{connection['host']}:{connection['port']}/"
        
        client = MongoClient(connection_string)
        db = client[connection['database']]
        collection = db[collection_name]
        
        # ดึงข้อมูลตัวอย่างเพื่อหา fields
        sample_docs = list(collection.find().limit(10))
        
        # รวบรวม fields ทั้งหมด
        fields = set()
        for doc in sample_docs:
            fields.update(doc.keys())
        
        # เรียงลำดับ fields ตามตัวอักษร
        fields = sorted(list(fields))
        
        client.close()
        
        return {'success': True, 'fields': fields}
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}

@eel.expose
def create_database(connection_name: str, database_name: str):
    """สร้างฐานข้อมูลใหม่"""
    try:
        # หา connection
        connection = None
        for conn in connection_manager.connections:
            if conn['name'] == connection_name:
                connection = conn
                break
        
        if not connection:
            return {'success': False, 'message': 'ไม่พบ connection ที่ระบุ'}
        
        from pymongo import MongoClient
        
        # สร้าง connection string
        if connection['username'] and connection['password']:
            connection_string = f"mongodb://{connection['username']}:{connection['password']}@{connection['host']}:{connection['port']}/"
        else:
            connection_string = f"mongodb://{connection['host']}:{connection['port']}/"
        
        client = MongoClient(connection_string)
        db = client[database_name]
        
        # สร้าง collection เปล่าเพื่อให้ฐานข้อมูลถูกสร้าง
        db.create_collection('temp_collection')
        db.drop_collection('temp_collection')
        
        client.close()
        
        return {'success': True, 'message': f'สร้างฐานข้อมูล {database_name} สำเร็จ'}
        
    except Exception as e:
        return {'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}

def create_html_interface():
    """สร้างไฟล์ HTML สำหรับ interface"""
    # สร้างโฟลเดอร์ html ถ้ายังไม่มี
    if not os.path.exists('html'):
        os.makedirs('html')
    
    # สร้างไฟล์ index.html
    html_content = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MongoDB Connection Manager</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .connections-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .connection-card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        
        .connection-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        
        .connection-name {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        
        .connection-details {
            color: #666;
            margin-bottom: 15px;
        }
        
        .connection-actions {
            display: flex;
            gap: 10px;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5a6fd8;
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-success:hover {
            background: #218838;
        }
        
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c82333;
        }
        
        .btn-warning {
            background: #ffc107;
            color: #212529;
        }
        
        .btn-warning:hover {
            background: #e0a800;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .alert {
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .hidden {
            display: none;
        }
        
        .loading {
            opacity: 0.6;
            pointer-events: none;
        }
        
        .test-result-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .test-result-content {
            background: white;
            border-radius: 15px;
            padding: 30px;
            max-width: 500px;
            width: 90%;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .test-result-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        .test-result-message {
            font-size: 1.1em;
            line-height: 1.6;
            margin-bottom: 25px;
            white-space: pre-line;
        }
        
        .test-result-success {
            color: #28a745;
        }
        
        .test-result-error {
            color: #dc3545;
        }
        
        .test-result-warning {
            color: #ffc107;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>MongoDB Connection Manager</h1>
            <p>จัดการการเชื่อมต่อฐานข้อมูล MongoDB ของคุณ</p>
        </div>
        
        <div class="content">
            <!-- แสดง Connections ที่มีอยู่ -->
            <div class="section">
                <h2>การเชื่อมต่อที่มีอยู่</h2>
                <div id="connections-container" class="connections-grid">
                    <!-- Connections จะถูกแสดงที่นี่ -->
                </div>
                <button class="btn btn-primary" onclick="showNewConnectionForm()">
                    + สร้างการเชื่อมต่อใหม่
                </button>
            </div>
            
            <!-- Form สำหรับสร้าง Connection ใหม่ -->
            <div id="new-connection-form" class="section hidden">
                <h2>สร้างการเชื่อมต่อใหม่</h2>
                <div id="form-alert"></div>
                <form id="connection-form">
                    <div class="form-group">
                        <label for="connection-name">ชื่อการเชื่อมต่อ *</label>
                        <input type="text" id="connection-name" required>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="connection-host">Host *</label>
                            <input type="text" id="connection-host" value="localhost" required>
                        </div>
                        <div class="form-group">
                            <label for="connection-port">Port *</label>
                            <input type="number" id="connection-port" value="27017" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="connection-database">ชื่อฐานข้อมูล *</label>
                        <input type="text" id="connection-database" required>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="connection-username">ชื่อผู้ใช้ (ไม่บังคับ)</label>
                            <input type="text" id="connection-username">
                        </div>
                        <div class="form-group">
                            <label for="connection-password">รหัสผ่าน (ไม่บังคับ)</label>
                            <input type="password" id="connection-password">
                        </div>
                    </div>
                    
                    <div class="connection-actions">
                        <button type="submit" class="btn btn-success">บันทึกการเชื่อมต่อ</button>
                        <button type="button" class="btn btn-danger" onclick="hideNewConnectionForm()">ยกเลิก</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script type="text/javascript" src="/eel.js"></script>
    <script>
        // โหลด connections เมื่อหน้าเว็บโหลดเสร็จ
        document.addEventListener('DOMContentLoaded', function() {
            loadConnections();
        });
        
        // โหลดและแสดง connections
        async function loadConnections() {
            try {
                const connections = await eel.get_connections()();
                displayConnections(connections);
            } catch (error) {
                console.error('เกิดข้อผิดพลาดในการโหลด connections:', error);
            }
        }
        
        // แสดง connections ในหน้าเว็บ
        function displayConnections(connections) {
            const container = document.getElementById('connections-container');
            
            if (connections.length === 0) {
                container.innerHTML = '<p style="grid-column: 1 / -1; text-align: center; color: #666;">ยังไม่มีการเชื่อมต่อใดๆ</p>';
                return;
            }
            
            container.innerHTML = connections.map(conn => `
                <div class="connection-card">
                    <div class="connection-name">${conn.name}</div>
                    <div class="connection-details">
                        <div><strong>Host:</strong> ${conn.host}:${conn.port}</div>
                        <div><strong>Database:</strong> ${conn.database}</div>
                        ${conn.username ? `<div><strong>Username:</strong> ${conn.username}</div>` : ''}
                    </div>
                    <div class="connection-actions">
                        <button class="btn btn-success" onclick="testConnection('${conn.name}')">ทดสอบ</button>
                        <button class="btn btn-primary" onclick="useConnection('${conn.name}')">เข้าใช้งาน</button>
                        <button class="btn btn-danger" onclick="deleteConnection('${conn.name}')">ลบ</button>
                    </div>
                </div>
            `).join('');
        }
        
        // แสดง form สำหรับสร้าง connection ใหม่
        function showNewConnectionForm() {
            document.getElementById('new-connection-form').classList.remove('hidden');
            document.getElementById('form-alert').innerHTML = '';
        }
        
        // ซ่อน form สำหรับสร้าง connection ใหม่
        function hideNewConnectionForm() {
            document.getElementById('new-connection-form').classList.add('hidden');
            document.getElementById('connection-form').reset();
        }
        
        // จัดการการส่ง form
        document.getElementById('connection-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('connection-name').value,
                host: document.getElementById('connection-host').value,
                port: parseInt(document.getElementById('connection-port').value),
                database: document.getElementById('connection-database').value,
                username: document.getElementById('connection-username').value,
                password: document.getElementById('connection-password').value
            };
            
            try {
                const result = await eel.add_new_connection(
                    formData.name,
                    formData.host,
                    formData.port,
                    formData.database,
                    formData.username,
                    formData.password
                )();
                
                showAlert(result.message, result.success ? 'success' : 'danger');
                
                if (result.success) {
                    hideNewConnectionForm();
                    loadConnections();
                }
            } catch (error) {
                showAlert('เกิดข้อผิดพลาดในการบันทึก', 'danger');
                console.error('เกิดข้อผิดพลาด:', error);
            }
        });
        
        // ลบ connection
        async function deleteConnection(name) {
            if (!confirm(`คุณแน่ใจหรือไม่ที่จะลบการเชื่อมต่อ "${name}"?`)) {
                return;
            }
            
            try {
                const result = await eel.delete_connection(name)();
                showAlert(result.message, result.success ? 'success' : 'danger');
                
                if (result.success) {
                    loadConnections();
                }
            } catch (error) {
                showAlert('เกิดข้อผิดพลาดในการลบ', 'danger');
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }
        
        // ทดสอบ connection
        async function testConnection(name) {
            try {
                // แสดง loading state
                const button = event.target;
                const originalText = button.textContent;
                button.textContent = '🔄 กำลังทดสอบ...';
                button.disabled = true;
                button.classList.add('loading');
                
                const result = await eel.test_connection(name)();
                
                // คืนค่าเดิมของปุ่ม
                button.textContent = originalText;
                button.disabled = false;
                button.classList.remove('loading');
                
                // แสดงผลลัพธ์
                showTestResult(result.message, result.success);
            } catch (error) {
                // คืนค่าเดิมของปุ่มในกรณีเกิดข้อผิดพลาด
                const button = event.target;
                button.textContent = 'ทดสอบ';
                button.disabled = false;
                button.classList.remove('loading');
                
                showTestResult('❌ เกิดข้อผิดพลาดในการทดสอบ', false);
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }
        
        // แสดง alert
        function showAlert(message, type) {
            const alertDiv = document.getElementById('form-alert');
            alertDiv.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
            
            // ลบ alert หลังจาก 5 วินาที
            setTimeout(() => {
                alertDiv.innerHTML = '';
            }, 5000);
        }
        
        // แสดงผลลัพธ์การทดสอบในรูปแบบ modal
        function showTestResult(message, isSuccess) {
            // สร้าง modal element
            const modal = document.createElement('div');
            modal.className = 'test-result-modal';
            
            // กำหนด icon และสีตามผลลัพธ์
            let icon, colorClass;
            if (isSuccess) {
                icon = '✅';
                colorClass = 'test-result-success';
            } else {
                icon = '❌';
                colorClass = 'test-result-error';
            }
            
            modal.innerHTML = `
                <div class="test-result-content">
                    <div class="test-result-icon ${colorClass}">${icon}</div>
                    <div class="test-result-message ${colorClass}">${message}</div>
                    <button class="btn btn-primary" onclick="closeTestResult()">ตกลง</button>
                </div>
            `;
            
            // เพิ่ม modal ลงใน body
            document.body.appendChild(modal);
            
            // ปิด modal เมื่อคลิกพื้นหลัง
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    closeTestResult();
                }
            });
            
            // ปิด modal เมื่อกด ESC
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeTestResult();
                }
            });
        }
        
        // ปิด modal ผลลัพธ์การทดสอบ
        function closeTestResult() {
            const modal = document.querySelector('.test-result-modal');
            if (modal) {
                modal.remove();
            }
        }
        
        // ใช้ connection และไปยังหน้า main
        async function useConnection(name) {
            try {
                const result = await eel.use_connection(name)();
                
                if (result.success) {
                    // เก็บข้อมูล connection ใน sessionStorage
                    sessionStorage.setItem('currentConnection', JSON.stringify(result.connection));
                    sessionStorage.setItem('databaseExists', result.database_exists);
                    
                    // ไปยังหน้า main
                    window.location.href = 'main.html';
                } else {
                    showAlert(result.message, 'danger');
                }
            } catch (error) {
                showAlert('เกิดข้อผิดพลาดในการเชื่อมต่อ', 'danger');
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }
    </script>
</body>
</html>
    """
    
    # บันทึกไฟล์ index.html
    with open('html/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # สร้างไฟล์ main.html
    main_html_content = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MongoDB Manager - Main</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            height: 100vh;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 1.8em;
        }
        
        .connection-info {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .connection-details {
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5a6fd8;
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-success:hover {
            background: #218838;
        }
        
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c82333;
        }
        
        .main-container {
            display: flex;
            height: calc(100vh - 80px);
        }
        
        .sidebar {
            width: 300px;
            background: white;
            border-right: 1px solid #e9ecef;
            overflow-y: auto;
        }
        
        .content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .database-section {
            background: white;
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
        }
        
        .database-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .database-name {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }
        
        .collections-section {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }
        
        .collection-item {
            padding: 12px 15px;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        
        .collection-item:hover {
            background: #e9ecef;
            border-color: #667eea;
        }
        
        .collection-item.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .data-section {
            flex: 1;
            background: white;
            margin: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        
        .data-header {
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
            background: #f8f9fa;
        }
        
        .data-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        
        .data-stats {
            color: #666;
            font-size: 0.9em;
        }
        
        .data-content {
            flex: 1;
            overflow: auto;
            padding: 20px;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .data-table th,
        .data-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }
        
        .data-table th {
            background: #f8f9fa;
            font-weight: bold;
            color: #333;
        }
        
        .data-table tr:hover {
            background: #f8f9fa;
        }
        
        .json-view {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            overflow-x: auto;
        }
        
        .no-data {
            text-align: center;
            color: #666;
            padding: 40px;
            font-size: 1.1em;
        }
        
        .alert {
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>MongoDB Manager</h1>
            <div class="connection-info">
                <div class="connection-details" id="connection-details">
                    <!-- รายละเอียดการเชื่อมต่อจะแสดงที่นี่ -->
                </div>
            </div>
        </div>
        <button class="btn btn-danger" onclick="goBack()">← กลับ</button>
    </div>
    
    <div class="main-container">
        <div class="sidebar">
            <div class="database-section">
                <div class="database-info">
                    <div class="database-name" id="database-name">
                        <!-- ชื่อฐานข้อมูลจะแสดงที่นี่ -->
                    </div>
                    <button class="btn btn-success" id="create-db-btn" onclick="createDatabase()" style="display: none;">
                        สร้างฐานข้อมูล
                    </button>
                </div>
                <div id="database-alert"></div>
            </div>
            
            <div class="collections-section">
                <h3>Collections</h3>
                <div id="collections-container">
                    <div class="loading">
                        <div class="spinner"></div>
                        กำลังโหลด collections...
                    </div>
                </div>
            </div>
        </div>
        
        <div class="content">
            <div class="data-section">
                <div class="data-header">
                    <div class="data-title" id="data-title">เลือก Collection เพื่อดูข้อมูล</div>
                    <div class="data-stats" id="data-stats"></div>
                </div>
                <div class="data-content" id="data-content">
                    <div class="no-data">เลือก Collection จากรายการด้านซ้ายเพื่อดูข้อมูล</div>
                </div>
            </div>
        </div>
    </div>

    <script type="text/javascript" src="/eel.js"></script>
    <script>
        let currentConnection = null;
        let currentCollection = null;
        
        // โหลดข้อมูลเมื่อหน้าเว็บโหลดเสร็จ
        document.addEventListener('DOMContentLoaded', function() {
            loadConnectionInfo();
            loadCollections();
        });
        
        // โหลดข้อมูลการเชื่อมต่อ
        function loadConnectionInfo() {
            const connectionData = sessionStorage.getItem('currentConnection');
            if (connectionData) {
                currentConnection = JSON.parse(connectionData);
                
                // แสดงรายละเอียดการเชื่อมต่อ
                document.getElementById('connection-details').innerHTML = `
                    <strong>${currentConnection.name}</strong><br>
                    ${currentConnection.host}:${currentConnection.port}
                `;
                
                // แสดงชื่อฐานข้อมูล
                document.getElementById('database-name').textContent = currentConnection.database;
                
                // ตรวจสอบว่าฐานข้อมูลมีอยู่หรือไม่
                const databaseExists = sessionStorage.getItem('databaseExists') === 'true';
                if (!databaseExists) {
                    document.getElementById('create-db-btn').style.display = 'inline-block';
                }
            } else {
                // ถ้าไม่มีข้อมูลการเชื่อมต่อ ให้กลับไปหน้าแรก
                goBack();
            }
        }
        
        // โหลด collections
        async function loadCollections() {
            try {
                const result = await eel.get_collections(currentConnection.name)();
                
                if (result.success) {
                    displayCollections(result.collections);
                } else {
                    showDatabaseAlert(result.message, 'danger');
                }
            } catch (error) {
                showDatabaseAlert('เกิดข้อผิดพลาดในการโหลด collections', 'danger');
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }
        
        // แสดง collections
        function displayCollections(collections) {
            const container = document.getElementById('collections-container');
            
            if (collections.length === 0) {
                container.innerHTML = '<div class="no-data">ไม่มี collections ในฐานข้อมูลนี้</div>';
                return;
            }
            
            const collectionsList = collections.map(collection => `
                <div class="collection-item" onclick="selectCollection('${collection}')">
                    📄 ${collection}
                </div>
            `).join('');
            
            container.innerHTML = collectionsList;
        }
        
        // เลือก collection
        async function selectCollection(collectionName) {
            try {
                // อัปเดต active state
                document.querySelectorAll('.collection-item').forEach(item => {
                    item.classList.remove('active');
                });
                event.target.classList.add('active');
                
                currentCollection = collectionName;
                
                // แสดง loading
                document.getElementById('data-title').textContent = `Collection: ${collectionName}`;
                document.getElementById('data-content').innerHTML = `
                    <div class="loading">
                        <div class="spinner"></div>
                        กำลังโหลดข้อมูล...
                    </div>
                `;
                
                // โหลดข้อมูล
                const result = await eel.get_collection_data(currentConnection.name, collectionName, 50)();
                
                if (result.success) {
                    displayData(result.data);
                } else {
                    document.getElementById('data-content').innerHTML = `
                        <div class="alert alert-danger">${result.message}</div>
                    `;
                }
            } catch (error) {
                document.getElementById('data-content').innerHTML = `
                    <div class="alert alert-danger">เกิดข้อผิดพลาดในการโหลดข้อมูล</div>
                `;
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }
        
        // แสดงข้อมูล
        function displayData(data) {
            const container = document.getElementById('data-content');
            
            if (data.length === 0) {
                container.innerHTML = '<div class="no-data">ไม่มีข้อมูลใน collection นี้</div>';
                document.getElementById('data-stats').textContent = '0 เอกสาร';
                return;
            }
            
            // แสดงสถิติ
            document.getElementById('data-stats').textContent = `${data.length} เอกสาร (แสดง 50 รายการแรก)`;
            
            // สร้างตาราง
            if (data.length > 0) {
                const fields = Object.keys(data[0]);
                
                const tableHTML = `
                    <table class="data-table">
                        <thead>
                            <tr>
                                ${fields.map(field => `<th>${field}</th>`).join('')}
                            </tr>
                        </thead>
                        <tbody>
                            ${data.map(doc => `
                                <tr>
                                    ${fields.map(field => `<td>${formatValue(doc[field])}</td>`).join('')}
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                `;
                
                container.innerHTML = tableHTML;
            }
        }
        
        // จัดรูปแบบค่า
        function formatValue(value) {
            if (value === null || value === undefined) {
                return '<em>null</em>';
            }
            
            if (typeof value === 'object') {
                return `<div class="json-view">${JSON.stringify(value, null, 2)}</div>`;
            }
            
            if (typeof value === 'string' && value.length > 100) {
                return value.substring(0, 100) + '...';
            }
            
            return String(value);
        }
        
        // สร้างฐานข้อมูล
        async function createDatabase() {
            if (!currentConnection) return;
            
            try {
                const result = await eel.create_database(currentConnection.name, currentConnection.database)();
                
                if (result.success) {
                    showDatabaseAlert(result.message, 'success');
                    document.getElementById('create-db-btn').style.display = 'none';
                    loadCollections();
                } else {
                    showDatabaseAlert(result.message, 'danger');
                }
            } catch (error) {
                showDatabaseAlert('เกิดข้อผิดพลาดในการสร้างฐานข้อมูล', 'danger');
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }
        
        // แสดง alert ในส่วนฐานข้อมูล
        function showDatabaseAlert(message, type) {
            const alertDiv = document.getElementById('database-alert');
            alertDiv.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
            
            setTimeout(() => {
                alertDiv.innerHTML = '';
            }, 5000);
        }
        
        // กลับไปหน้าแรก
        function goBack() {
            sessionStorage.removeItem('currentConnection');
            sessionStorage.removeItem('databaseExists');
            window.location.href = 'index.html';
        }
    </script>
</body>
</html>
    """
    
    # บันทึกไฟล์ main.html
    with open('html/main.html', 'w', encoding='utf-8') as f:
        f.write(main_html_content)

def main():
    """ฟังก์ชันหลักสำหรับรันแอปพลิเคชัน"""
    # สร้าง HTML interface
    create_html_interface()
    
    # เริ่มต้น Eel application
    print("กำลังเริ่มต้น MongoDB Connection Manager...")
    print("เปิดเบราว์เซอร์ที่: http://localhost:8000")
    
    try:
        eel.start('index.html', size=(1200, 800), port=8000)
    except (SystemExit, MemoryError, KeyboardInterrupt):
        print("ปิดแอปพลิเคชัน...")

if __name__ == "__main__":
    main()
