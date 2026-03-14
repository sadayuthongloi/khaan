"""
HTML Generator
สร้างไฟล์ HTML สำหรับ interface ของแอปพลิเคชัน
"""

import os


class HTMLGenerator:
    """สร้างไฟล์ HTML สำหรับ interface"""
    
    def __init__(self, html_dir: str = 'html'):
        self.html_dir = html_dir
        self.views_dir = os.path.join(html_dir, 'views')
        self._ensure_html_directory()
    
    def _ensure_html_directory(self):
        """สร้างโฟลเดอร์ html และ views ถ้ายังไม่มี"""
        if not os.path.exists(self.html_dir):
            os.makedirs(self.html_dir)
        if not os.path.exists(self.views_dir):
            os.makedirs(self.views_dir)
    
    def generate_index_html(self):
        """สร้างไฟล์ index.html"""
        html_content = self._get_index_html_content()
        self._write_html_file('index.html', html_content)
    
    def generate_main_html(self):
        """สร้างไฟล์ main.html"""
        html_content = self._get_main_html_content()
        self._write_html_file('main.html', html_content)

    def generate_views(self):
        """สร้างไฟล์ view แยกใน views/"""
        self._write_view_file('collections.html', self._get_collections_view_content())
        self._write_view_file('data.html', self._get_data_view_content())
        self._write_view_file('editor.html', self._get_editor_view_content())

    def generate_all(self):
        """สร้างไฟล์ HTML ทั้งหมด"""
        self.generate_index_html()
        self.generate_main_html()
        self.generate_views()

    def _write_html_file(self, filename: str, content: str):
        """เขียนไฟล์ HTML หลัก"""
        filepath = os.path.join(self.html_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def _write_view_file(self, filename: str, content: str):
        """เขียนไฟล์ view ใน views/"""
        filepath = os.path.join(self.views_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def _get_collections_view_content(self) -> str:
        """อ่านเนื้อหา views/collections.html จากไฟล์ (ถ้ามี) หรือ return string เปล่า"""
        path = os.path.join(self.views_dir, 'collections.html')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return '<!-- collections view not found -->'

    def _get_data_view_content(self) -> str:
        """อ่านเนื้อหา views/data.html จากไฟล์ (ถ้ามี)"""
        path = os.path.join(self.views_dir, 'data.html')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return '<!-- data view not found -->'

    def _get_editor_view_content(self) -> str:
        """อ่านเนื้อหา views/editor.html จากไฟล์ (ถ้ามี)"""
        path = os.path.join(self.views_dir, 'editor.html')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return '<!-- editor view not found -->'
    
    def _get_index_html_content(self) -> str:
        """สร้างเนื้อหา index.html"""
        return """
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
            background: #f4f6f9;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: #f4f6f9;
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
            border-bottom: 2px solid #0a58ca;
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
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
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
            background: #0a58ca;
            color: white;
        }
        
        .btn-primary:hover {
            background: #0b5ed7;
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
            border-color: #0a58ca;
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
        
        .page-id-badge {
            position: fixed;
            top: 12px;
            right: 16px;
            background: #0a58ca;
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            letter-spacing: 0.5px;
            z-index: 9999;
            opacity: 0.85;
            pointer-events: none;
            user-select: none;
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
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
    </style>
</head>
<body>
    <div class="page-id-badge">P1 · Connections</div>
    <div class="container">
        <div class="header">
            <h1>MongoDB Connection Manager</h1>
            <p>จัดการการเชื่อมต่อฐานข้อมูล MongoDB ของคุณ</p>
        </div>
        
        <div class="content">
            <!-- แสดง Connections ที่มีอยู่ -->
            <div class="section">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="margin-bottom: 0;">การเชื่อมต่อที่มีอยู่</h2>
                    <button class="btn btn-secondary" onclick="openMongodbFolder()" style="display: flex; align-items: center; gap: 5px;" title="เปิดโฟลเดอร์ใน Windows Explorer">
                        📁 C:\Program Files\MongoDB\Server
                    </button>
                </div>
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
        
        // เปิดโฟลเดอร์ MongoDB 
        async function openMongodbFolder() {
            try {
                const result = await eel.open_mongodb_folder()();
                if (!result.success) {
                    showAlert(result.message, 'danger');
                }
            } catch (error) {
                console.error('เกิดข้อผิดพลาด:', error);
                showAlert('เกิดข้อผิดพลาดในการเปิดโฟลเดอร์', 'danger');
            }
        }

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
                username: document.getElementById('connection-username').value,
                password: document.getElementById('connection-password').value
            };
            
            try {
                const result = await eel.add_new_connection(
                    formData.name,
                    formData.host,
                    formData.port,
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
        
        // ใช้ connection และไปยังหน้า main
        async function useConnection(name) {
            try {
                const result = await eel.use_connection(name)();
                
                if (result.success) {
                    // เก็บข้อมูล connection ใน sessionStorage
                    sessionStorage.setItem('currentConnection', JSON.stringify(result.connection));
                    
                    // ไปยังหน้า main
                    window.location.href = 'main.html?v=' + new Date().getTime();
                } else {
                    showAlert(result.message, 'danger');
                }
            } catch (error) {
                showAlert('เกิดข้อผิดพลาดในการเชื่อมต่อ', 'danger');
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
    </script>
</body>
</html>
        """
    
    def _get_main_html_content(self) -> str:
        """สร้างเนื้อหา main.html"""
        return """<!DOCTYPE html>
<html lang="th">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MongoDB Manager - Main</title>
    <style>
        .page-id-badge {
            position: fixed;
            top: 12px;
            right: 16px;
            background: #0a58ca;
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            letter-spacing: 0.5px;
            z-index: 9999;
            opacity: 0.85;
            pointer-events: none;
            user-select: none;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8f9fa;
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        /* Custom scrollbar for a premium look */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: #cbd5e0;
            border-radius: 10px;
            border: 2px solid #f1f1f1;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #a0aec0;
        }

        .header {
            background: #f4f6f9;
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
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
            background: #0a58ca;
            color: white;
        }

        .btn-primary:hover {
            background: #084298;
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

        .btn-secondary {
            background: #6c757d;
            color: white;
        }

        .btn-secondary:hover {
            background: #5a6268;
        }

        .btn-info {
            background: #17a2b8;
            color: white;
        }

        .btn-info:hover {
            background: #138496;
        }

        .main-container {
            display: flex;
            flex: 1;
            min-height: 0;
        }

        .sidebar {
            width: 300px;
            background: white;
            border-right: 1px solid #e9ecef;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }

        .content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            min-height: 0;
        }

        /* Database list section */
        .databases-section {
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
        }

        .databases-section h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 1em;
        }

        .database-item {
            padding: 10px 15px;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            background: #f8f9fa;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .database-item:hover {
            background: #e9ecef;
            border-color: #0a58ca;
        }

        .database-item.active {
            background: #0a58ca;
            color: white;
            border-color: #0a58ca;
        }

        .database-name-label {
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-weight: 500;
        }

        /* Collections grid in content area */
        .collections-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 12px;
            padding: 10px 0;
        }

        .collections-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .collections-header h3 {
            color: #333;
            font-size: 1em;
        }

        .btn-del {
            padding: 4px 12px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: bold;
            transition: all 0.3s ease;
            display: none;
        }

        .btn-del:hover {
            background: #c82333;
        }

        .btn-del.show {
            display: inline-block;
        }

        .collection-item {
            padding: 15px;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            background: #f8f9fa;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.95em;
        }

        .collection-item:hover {
            background: #e9ecef;
            border-color: #0a58ca;
        }

        .collection-item.active {
            background: #0a58ca;
            color: white;
            border-color: #0a58ca;
        }

        .collection-checkbox {
            width: 16px;
            height: 16px;
            cursor: pointer;
            accent-color: #0a58ca;
            flex-shrink: 0;
        }

        .collection-name {
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .data-section {
            flex: 1;
            background: white;
            margin: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            min-height: 0;
        }

        .data-header {
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
            background: #f8f9fa;
            display: flex;
            justify-content: space-between;
            align-items: center;
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

        .data-header-right {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .delete-modal {
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

        .delete-modal-content {
            background: white;
            border-radius: 15px;
            padding: 30px;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .delete-modal-header {
            text-align: center;
            margin-bottom: 20px;
        }

        .delete-modal-title {
            font-size: 1.5em;
            font-weight: bold;
            color: #dc3545;
            margin-bottom: 10px;
        }

        .delete-modal-message {
            color: #666;
            line-height: 1.5;
        }

        .delete-modal-form {
            margin-bottom: 25px;
        }

        .delete-modal-form label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
        }

        .delete-modal-form input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 5px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }

        .delete-modal-form input:focus {
            outline: none;
            border-color: #dc3545;
        }

        .delete-modal-actions {
            display: flex;
            gap: 15px;
            justify-content: center;
        }

        .btn-warning {
            background: #ffc107;
            color: #212529;
        }

        .btn-warning:hover {
            background: #e0a800;
        }

        /* Generic Modals (Alert & Confirm) */
        .generic-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1050;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }

        .generic-modal.show {
            opacity: 1;
            visibility: visible;
        }

        .generic-modal-content {
            background: white;
            border-radius: 12px;
            padding: 25px;
            max-width: 400px;
            width: 90%;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            transform: translateY(-20px);
            transition: transform 0.3s ease;
        }

        .generic-modal.show .generic-modal-content {
            transform: translateY(0);
        }

        .generic-modal-header {
            margin-bottom: 15px;
        }

        .generic-modal-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }

        .generic-modal-title.error {
            color: #dc3545;
        }

        .generic-modal-title.success {
            color: #28a745;
        }

        .generic-modal-title.warning {
            color: #ffc107;
        }

        .generic-modal-message {
            color: #555;
            line-height: 1.5;
            margin-bottom: 25px;
            white-space: pre-line;
            max-height: 300px;
            overflow-y: auto;
            padding-right: 5px;
        }

        .generic-modal-actions {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }

        .search-form {
            background: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            flex-shrink: 0;
            border-bottom: 1px solid #e9ecef;
        }

        .search-row {
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }

        .search-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .search-group label {
            font-size: 0.9em;
            font-weight: bold;
            color: #333;
        }

        .search-group select,
        .search-group input {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            min-width: 120px;
        }

        .search-group select:focus,
        .search-group input:focus {
            outline: none;
            border-color: #0a58ca;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }

        .search-actions {
            display: flex;
            gap: 10px;
            align-items: end;
        }

        .data-content {
            flex: 1;
            overflow-y: auto;
            overflow-x: auto;
            padding: 20px;
            min-height: 0;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
        }

        .data-table th,
        .data-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
            white-space: nowrap;
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .data-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
            position: sticky;
            top: 0;
            z-index: 10;
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
            border-top: 3px solid #0a58ca;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            0% {
                transform: rotate(0deg);
            }

            100% {
                transform: rotate(360deg);
            }
        }

        /* Editor Field Rows */
        .editor-fields-container {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 5px;
        }

        .editor-field-row {
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 10px;
            padding: 8px 12px;
            margin-bottom: 6px;
            border: 1px solid #f0f0f0;
            border-radius: 6px;
            background: #fafafa;
            transition: background 0.15s;
        }

        .editor-field-row:hover {
            background: #f0f4ff;
            border-color: #c8d8ff;
        }

        .editor-field-key {
            font-weight: 600;
            color: #0a58ca;
            font-size: 0.85em;
            word-break: break-word;
            letter-spacing: 0.02em;
            width: 150px;
            min-width: 150px;
            flex-shrink: 0;
        }

        .editor-field-value {
            flex: 1;
            min-width: 0;
        }

        .editor-field-value input,
        .editor-field-value textarea {
            width: 100%;
            padding: 6px 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            transition: border-color 0.3s ease;
            box-sizing: border-box;
        }

        .editor-field-value input:focus,
        .editor-field-value textarea:focus {
            outline: none;
            border-color: #0a58ca;
            box-shadow: 0 0 0 2px rgba(10, 88, 202, 0.15);
        }

        .editor-field-value textarea {
            resize: vertical;
            min-height: 38px;
        }

        .editor-field-value .field-readonly {
            padding: 6px 10px;
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            color: #6c757d;
            word-break: break-all;
        }

        .editor-field-actions {
            display: flex;
            flex-shrink: 0;
        }

        .btn-update-field {
            padding: 5px 14px;
            background: #0a58ca;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.3s ease;
            white-space: nowrap;
        }

        .btn-update-field:hover {
            background: #084298;
        }

        .btn-update-field:disabled {
            background: #6c757d;
            cursor: not-allowed;
        }

        .btn-update-field.success {
            background: #28a745;
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
            <!-- Databases List -->
            <div class="databases-section">
                <h3>🗄️ ฐานข้อมูล</h3>
                <div id="databases-container">
                    <div class="loading">
                        <div class="spinner"></div>
                        กำลังโหลดฐานข้อมูล...
                    </div>
                </div>
            </div>
        </div>

        <div class="content">
            <div class="data-section">
                <div class="data-header">
                    <div>
                        <div class="data-title" id="data-title">เลือกฐานข้อมูลและ Collection เพื่อดูข้อมูล</div>
                        <div class="data-stats" id="data-stats"></div>
                    </div>
                    <div class="data-header-right">
                        <button class="btn btn-danger" id="delete-btn" onclick="showDeleteModal()"
                            style="display: none;">
                            🗑️ ล้างข้อมูล
                        </button>
                    </div>
                </div>

                <!-- Search Form -->
                <div class="search-form" id="search-form" style="display: none;">
                    <div class="search-row">
                        <div class="search-group">
                            <label for="search-field">ฟิลด์</label>
                            <select id="search-field">
                                <option value="">เลือกฟิลด์</option>
                            </select>
                        </div>
                        <div class="search-group">
                            <label for="search-operator">เงื่อนไข</label>
                            <select id="search-operator">
                                <option value="">เลือกเงื่อนไข</option>
                                <option value="=">= (เท่ากับ)</option>
                                <option value="like">like (คล้าย)</option>
                            </select>
                        </div>
                        <div class="search-group">
                            <label for="search-value">ค่า</label>
                            <input type="text" id="search-value" placeholder="กรอกค่าที่ต้องการค้นหา">
                        </div>
                        <div class="search-actions">
                            <button class="btn btn-primary" onclick="performSearch()">🔍 ค้นหา</button>
                            <button class="btn btn-secondary" onclick="clearSearch()">🗑️ ล้างการค้นหา</button>
                        </div>
                    </div>
                </div>

                <div class="data-content" id="data-content">
                    <div class="no-data">เลือกฐานข้อมูลจากรายการด้านซ้ายเพื่อเริ่มต้น</div>
                </div>
            </div>

            <!-- Editor Section -->
            <div class="editor-section" id="editor-section" style="display: none; height: 100%; flex-direction: column;">
                <div class="data-header" style="margin-bottom: 10px;">
                    <div>
                        <div class="data-title" id="editor-title">แก้ไข Document</div>
                        <div class="data-stats" id="editor-subtitle"></div>
                    </div>
                    <div class="data-header-right">
                        <button class="btn btn-info" onclick="sortEditorFields()">🔠 A-Z</button>
                        <button class="btn btn-info" onclick="sortEditorFieldsZA()" style="margin-left: 5px;">🔡 Z-A</button>
                        <button class="btn btn-secondary" onclick="closeEditor()">❌ ปิด</button>
                    </div>
                </div>
                <div class="editor-fields-container" id="editor-fields-container">
                    <!-- Field rows will be rendered here -->
                </div>
            </div>
        </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="delete-modal" id="delete-modal" style="display: none;">
        <div class="delete-modal-content">
            <div class="delete-modal-header">
                <div class="delete-modal-title">⚠️ ยืนยันการล้างข้อมูล</div>
                <div class="delete-modal-message">
                    คุณกำลังจะล้างข้อมูลทั้งหมดใน collection <strong id="modal-collection-name"></strong><br>
                    การดำเนินการนี้ไม่สามารถยกเลิกได้ กรุณายืนยันชื่อ collection เพื่อดำเนินการต่อ
                </div>
            </div>
            <div class="delete-modal-form">
                <label for="confirm-collection-name">กรอกชื่อ collection เพื่อยืนยัน:</label>
                <input type="text" id="confirm-collection-name" placeholder="กรอกชื่อ collection ที่ต้องการล้างข้อมูล">
            </div>
            <div class="delete-modal-actions">
                <button class="btn btn-warning" onclick="confirmDelete()">🗑️ ล้างข้อมูล</button>
                <button class="btn btn-secondary" onclick="hideDeleteModal()">❌ ยกเลิก</button>
            </div>
        </div>
    </div>

    <!-- Generic Alert Modal -->
    <div class="generic-modal" id="alert-modal">
        <div class="generic-modal-content">
            <div class="generic-modal-header">
                <div class="generic-modal-title" id="alert-modal-title">แจ้งเตือน</div>
            </div>
            <div class="generic-modal-message" id="alert-modal-message"></div>
            <div class="generic-modal-actions">
                <button class="btn btn-primary" id="alert-modal-ok">ตกลง</button>
            </div>
        </div>
    </div>

    <!-- Generic Confirm Modal -->
    <div class="generic-modal" id="confirm-modal">
        <div class="generic-modal-content">
            <div class="generic-modal-header">
                <div class="generic-modal-title warning" id="confirm-modal-title">ยืนยันการดำเนินการ</div>
            </div>
            <div class="generic-modal-message" id="confirm-modal-message"></div>
            <div class="generic-modal-actions">
                <button class="btn btn-danger" id="confirm-modal-yes">ยืนยัน</button>
                <button class="btn btn-secondary" id="confirm-modal-no">ยกเลิก</button>
            </div>
        </div>
    </div>

    <script type="text/javascript" src="/eel.js"></script>
    <script>
        let currentConnection = null;
        let currentDatabase = null;
        let currentCollection = null;
        let currentFields = [];
        let currentEditingDocumentId = null;
        let currentDocumentData = null;

        // โหลดข้อมูลเมื่อหน้าเว็บโหลดเสร็จ
        document.addEventListener('DOMContentLoaded', function () {
            loadConnectionInfo();
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

                // โหลดรายการฐานข้อมูลหลังจาก currentConnection ถูกเซ็ตแล้ว
                loadDatabases();
            } else {
                // ถ้าไม่มีข้อมูลการเชื่อมต่อ ให้กลับไปหน้าแรก
                goBack();
            }
        }

        // โหลดรายการฐานข้อมูล
        async function loadDatabases() {
            if (!currentConnection) return;

            try {
                const result = await eel.get_databases(currentConnection.name)();

                if (result.success) {
                    displayDatabases(result.databases);
                    
                    // ปิดหน้า Edit 
                    document.getElementById('editor-section').style.display = 'none';
                    document.querySelector('.data-section').style.display = 'block';
                } else {
                    document.getElementById('databases-container').innerHTML = `
                        <div class="alert alert-danger">${result.message}</div>
                    `;
                }
            } catch (error) {
                document.getElementById('databases-container').innerHTML = `
                    <div class="alert alert-danger">เกิดข้อผิดพลาดในการโหลดฐานข้อมูล: ${error}</div>
                `;
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }

        // แสดงรายการฐานข้อมูล
        function displayDatabases(databases) {
            const container = document.getElementById('databases-container');

            if (databases.length === 0) {
                container.innerHTML = '<div class="no-data">ไม่พบฐานข้อมูล</div>';
                return;
            }

            container.innerHTML = databases.map(db => `
                <div class="database-item" onclick="selectDatabase('${db}')">
                    <span class="database-name-label">🗄️ ${db}</span>
                </div>
            `).join('');
        }

        // เลือกฐานข้อมูล
        async function selectDatabase(databaseName) {
            currentDatabase = databaseName;
            currentCollection = null;

            // อัปเดต active state
            document.querySelectorAll('.database-item').forEach(item => {
                item.classList.remove('active');
            });
            event.currentTarget.classList.add('active');

            // รีเซ็ต data section
            document.getElementById('data-title').textContent = `ฐานข้อมูล: ${databaseName}`;
            document.getElementById('data-stats').textContent = '';
            document.getElementById('search-form').style.display = 'none';
            document.getElementById('delete-btn').style.display = 'none';

            // โหลด collections แสดงที่ content area
            await loadCollections();
        }

        // โหลด collections
        async function loadCollections() {
            if (!currentDatabase) return;

            const container = document.getElementById('data-content');
            container.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    กำลังโหลด collections...
                </div>
            `;

            try {
                const result = await eel.get_collections(currentConnection.name, currentDatabase)();

                if (result.success) {
                    displayCollections(result.collections);
                } else {
                    container.innerHTML = `<div class="alert alert-danger">${result.message}</div>`;
                }
            } catch (error) {
                container.innerHTML = '<div class="alert alert-danger">เกิดข้อผิดพลาดในการโหลด collections</div>';
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }

        // แสดง collections
        function displayCollections(collections) {
            const container = document.getElementById('data-content');

            if (collections.length === 0) {
                container.innerHTML = '<div class="no-data">ไม่มี collections ในฐานข้อมูลนี้</div>';
                return;
            }

            document.getElementById('data-stats').textContent = `${collections.length} collections`;

            const header = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <div>
                        <button class="btn btn-success" onclick="importCollection()">📥 Import</button>
                        <button class="btn btn-primary" onclick="exportSelectedCollections()" style="margin-left: 5px;">📤 Export</button>
                    </div>
                    <button class="btn-del" id="btn-del-collections" onclick="deleteSelectedCollections()">🗑️ Del</button>
                </div>
            `;

            const collectionsList = collections.map(collection => `
                <tr style="cursor: pointer;" onclick="if(event.target.type !== 'checkbox') selectCollection('${collection}')">
                    <td style="width: 50px; text-align: center;">
                        <input type="checkbox" class="collection-checkbox" data-collection="${collection}" onclick="onCheckboxChange(event)">
                    </td>
                    <td>
                        <span class="collection-name" style="display: flex; align-items: center; gap: 8px;">
                            📄 ${collection}
                        </span>
                    </td>
                </tr>
            `).join('');

            const tableHTML = `
                <div style="overflow-y: auto; max-height: calc(100vh - 260px); border: 1px solid #e9ecef; border-radius: 5px;">
                    <table class="data-table" style="background: white; margin: 0; width: 100%;">
                        <thead style="position: sticky; top: 0; background: #f8f9fa; z-index: 10; box-shadow: 0 2px 2px -1px rgba(0, 0, 0, 0.1);">
                            <tr>
                                <th style="width: 50px; text-align: center;">
                                    <input type="checkbox" id="select-all-collections" onclick="toggleAllCollections(event)" title="เลือกทั้งหมด">
                                </th>
                                <th>ชื่อ Collection</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${collectionsList}
                        </tbody>
                    </table>
                </div>
            `;

            container.innerHTML = header + tableHTML;
        }

        // เลือก/ยกเลิกเลือก ทั้งหมด
        function toggleAllCollections(event) {
            const isChecked = event.target.checked;
            const checkboxes = document.querySelectorAll('.collection-checkbox');
            checkboxes.forEach(cb => {
                cb.checked = isChecked;
            });
            updateDelButton();
        }

        // จัดการเมื่อ checkbox เปลี่ยนสถานะ
        function onCheckboxChange(event) {
            event.stopPropagation();
            updateDelButton();
        }

        // อัปเดตการแสดงปุ่ม Del
        function updateDelButton() {
            const checked = document.querySelectorAll('.collection-checkbox:checked');
            const delBtn = document.getElementById('btn-del-collections');
            if (checked.length > 0) {
                delBtn.classList.add('show');
                delBtn.textContent = `🗑️ Del (${checked.length})`;
            } else {
                delBtn.classList.remove('show');
                delBtn.textContent = '🗑️ Del';
            }
        }

        // ลบ collections ที่เลือก
        async function deleteSelectedCollections() {
            const checked = document.querySelectorAll('.collection-checkbox:checked');
            if (checked.length === 0) {
                showAlert('กรุณาเลือก collection ที่ต้องการลบ', 'แจ้งเตือน', 'warning');
                return;
            }

            const names = Array.from(checked).map(cb => cb.dataset.collection);
            const confirmMsg = `คุณแน่ใจหรือไม่ที่จะลบ ${names.length} collections?\n\n${names.join('\n')}\n\nการดำเนินการนี้ไม่สามารถยกเลิกได้!`;

            if (!await showConfirm(confirmMsg, '⚠️ ยืนยันการลบ Collections')) return;

            try {
                const result = await eel.drop_collections(currentConnection.name, currentDatabase, names)();

                if (result.success) {
                    showAlert(result.message, 'สำเร็จ', 'success');
                    // รีเซ็ต current collection ถ้าถูกลบ
                    if (currentCollection && names.includes(currentCollection)) {
                        currentCollection = null;
                        document.getElementById('data-title').textContent = `ฐานข้อมูล: ${currentDatabase}`;
                        document.getElementById('data-stats').textContent = '';
                        document.getElementById('search-form').style.display = 'none';
                        document.getElementById('delete-btn').style.display = 'none';
                    }
                    // โหลด collections ใหม่
                    await loadCollections();
                } else {
                    showAlert(result.message, 'ผิดพลาด', 'error');
                }
            } catch (error) {
                showAlert('เกิดข้อผิดพลาดในการลบ collections', 'ผิดพลาด', 'error');
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }

        // เลือก collection
        async function selectCollection(collectionName) {
            try {
                // อัปเดต active state
                document.querySelectorAll('.collection-item').forEach(item => {
                    item.classList.remove('active');
                });
                event.currentTarget.classList.add('active');

                currentCollection = collectionName;
                
                // ปิดหน้า Edit
                document.getElementById('editor-section').style.display = 'none';
                document.querySelector('.data-section').style.display = 'block';

                // แสดง loading
                document.getElementById('data-title').textContent = `${currentDatabase} / ${collectionName}`;
                document.getElementById('data-content').innerHTML = `
                    <div class="loading">
                        <div class="spinner"></div>
                        กำลังโหลดข้อมูล...
                    </div>
                `;

                // ซ่อน search form และปุ่ม Delete
                document.getElementById('search-form').style.display = 'none';
                document.getElementById('delete-btn').style.display = 'none';

                // โหลดข้อมูล
                const result = await eel.get_collection_data(currentConnection.name, currentDatabase, collectionName, 50)();

                if (result.success) {
                    displayData(result.data);
                    // โหลด fields สำหรับ search
                    await loadCollectionFields(collectionName);
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
                // ซ่อนปุ่ม Delete เมื่อไม่มีข้อมูล
                document.getElementById('delete-btn').style.display = 'none';
                return;
            }

            // แสดงสถิติ
            document.getElementById('data-stats').textContent = `${data.length} เอกสาร (แสดง 50 รายการแรก)`;

            // แสดง search form และปุ่ม Delete
            document.getElementById('search-form').style.display = 'block';
            document.getElementById('delete-btn').style.display = 'inline-block';

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
                                <tr ondblclick="editDocument('${doc._id}')" style="cursor: pointer;" title="ดับเบิลคลิกเพื่อดู/แก้ไขข้อมูล">
                                    ${fields.map(field => `<td>${formatValue(doc[field])}</td>`).join('')}
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                `;

                container.innerHTML = tableHTML;
            }
        }



        // เปิด Editor เพื่อแก้ไข Document
        async function editDocument(documentId) {
            try {
                // สลับ UI ทันที
                document.querySelector('.data-section').style.display = 'none';
                const editorSection = document.getElementById('editor-section');
                editorSection.style.display = 'flex';
                
                // แสดง loading ใน editor container
                document.getElementById('editor-fields-container').innerHTML = `
                    <div class="loading">
                        <div class="spinner"></div>
                        กำลังโหลดข้อมูล Document...
                    </div>
                `;

                // เรียก Python backend เพื่อดึงข้อมูลเต็มของ Document นี้
                const result = await eel.get_document(currentConnection.name, currentDatabase, currentCollection, documentId)();

                if (result.success) {
                    currentEditingDocumentId = documentId;
                    
                    document.getElementById('editor-subtitle').textContent = `Collection: ${currentCollection} | ID: ${documentId}`;
                    
                    // Parse JSON แล้วสร้าง field rows
                    currentDocumentData = JSON.parse(result.document_json);
                    renderEditorFields(currentDocumentData);
                    
                } else {
                    document.getElementById('editor-fields-container').innerHTML = `
                        <div class="alert alert-danger">${result.message}</div>
                    `;
                }
            } catch (error) {
                console.error('เกิดข้อผิดพลาดในการโหลด Document:', error);
                document.getElementById('editor-fields-container').innerHTML = `
                    <div class="alert alert-danger">เกิดข้อผิดพลาดในการดึงข้อมูล Document</div>
                `;
            }
        }

        // Render field rows ใน Editor
        function renderEditorFields(docData) {
            const container = document.getElementById('editor-fields-container');
            let html = '';

            for (const [key, value] of Object.entries(docData)) {
                const isId = (key === '_id');
                const valueStr = (typeof value === 'object' && value !== null)
                    ? JSON.stringify(value, null, 2)
                    : String(value ?? '');
                const isMultiline = (typeof value === 'object' && value !== null) || valueStr.length > 80;
                const escapedValue = valueStr.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
                const escapedKey = key.replace(/'/g, "'").replace(/"/g, '&quot;');

                html += `<div class="editor-field-row">`;
                html += `  <div class="editor-field-key" title="${key}">${key}</div>`;
                html += `  <div class="editor-field-value">`;

                if (isId) {
                    // _id เป็น read-only
                    html += `<div class="field-readonly">${escapedValue}</div>`;
                } else if (isMultiline) {
                    html += `<textarea id="field-${escapedKey}" rows="4">${escapedValue}</textarea>`;
                } else {
                    html += `<input type="text" id="field-${escapedKey}" value="${escapedValue}">`;
                }

                html += `  </div>`;
                html += `  <div class="editor-field-actions">`;

                if (!isId) {
                    html += `<button class="btn-update-field" onclick="updateField('${escapedKey}', this)">💾 Update</button>`;
                }

                html += `  </div>`;
                html += `</div>`;
            }

            container.innerHTML = html;
        }

        // เรียงลำดับฟิลด์ A-Z
        function sortEditorFields() {
            if (!currentDocumentData) return;
            
            // สร้าง object ใหม่ที่เรียงลำดับ key แล้ว
            const sortedData = {};
            // _id ควรอยู่บนสุดเสมอ
            if (currentDocumentData._id) {
                sortedData._id = currentDocumentData._id;
            }
            
            Object.keys(currentDocumentData)
                .filter(key => key !== '_id')
                .sort()
                .forEach(key => {
                    sortedData[key] = currentDocumentData[key];
                });
            
            // เก็บข้อมูลที่เรียงแล้วไว้ใช้ต่อ
            currentDocumentData = sortedData;
            renderEditorFields(currentDocumentData);
        }

        // เรียงลำดับฟิลด์ Z-A
        function sortEditorFieldsZA() {
            if (!currentDocumentData) return;
            
            const sortedData = {};
            // _id ควรอยู่บนสุดเสมอ
            if (currentDocumentData._id) {
                sortedData._id = currentDocumentData._id;
            }
            
            Object.keys(currentDocumentData)
                .filter(key => key !== '_id')
                .sort()
                .reverse()
                .forEach(key => {
                    sortedData[key] = currentDocumentData[key];
                });
            
            currentDocumentData = sortedData;
            renderEditorFields(currentDocumentData);
        }

        // อัปเดตเฉพาะ field เดียว
        async function updateField(fieldKey, btnElement) {
            if (!currentEditingDocumentId) return;

            const inputEl = document.getElementById('field-' + fieldKey);
            if (!inputEl) return;

            const rawValue = inputEl.value;

            // ลองแปลง JSON ก่อน ถ้าไม่ได้ก็ใช้เป็น string
            let valueJsonStr;
            try {
                JSON.parse(rawValue);
                valueJsonStr = rawValue;
            } catch {
                // เป็น string ธรรมดา
                valueJsonStr = JSON.stringify(rawValue);
            }

            const originalText = btnElement.innerHTML;
            btnElement.innerHTML = '⏳...';
            btnElement.disabled = true;

            try {
                const result = await eel.update_document_field(
                    currentConnection.name,
                    currentDatabase,
                    currentCollection,
                    currentEditingDocumentId,
                    fieldKey,
                    valueJsonStr
                )();

                if (result.success) {
                    // อัปเดตข้อมูลใน currentDocumentData ด้วย
                    try {
                        currentDocumentData[fieldKey] = JSON.parse(valueJsonStr);
                    } catch {
                        currentDocumentData[fieldKey] = rawValue;
                    }

                    btnElement.innerHTML = '✅';
                    btnElement.classList.add('success');
                    setTimeout(() => {
                        btnElement.innerHTML = originalText;
                        btnElement.classList.remove('success');
                        btnElement.disabled = false;
                    }, 1500);
                } else {
                    btnElement.innerHTML = originalText;
                    btnElement.disabled = false;
                    showAlert('ล้มเหลว: ' + result.message, 'ผิดพลาด', 'error');
                }
            } catch (error) {
                console.error('เกิดข้อผิดพลาดในการอัปเดต field:', error);
                btnElement.innerHTML = originalText;
                btnElement.disabled = false;
                showAlert('เกิดข้อผิดพลาด: ' + String(error.message || error), 'ผิดพลาด', 'error');
            }
        }

        // ปิด Editor
        function closeEditor() {
            document.getElementById('editor-section').style.display = 'none';
            document.querySelector('.data-section').style.display = 'block';
            currentEditingDocumentId = null;
            currentDocumentData = null;
            document.getElementById('editor-fields-container').innerHTML = '';
        }

        // จัดรูปแบบค่า
        function formatValue(value) {
            if (value === null || value === undefined) {
                return '<em>null</em>';
            }

            if (Array.isArray(value)) {
                return '<span style="color: #6c757d; font-style: italic;">[array]</span>';
            }

            if (typeof value === 'object') {
                return '<span style="color: #6c757d; font-style: italic;">[object]</span>';
            }

            if (typeof value === 'string' && value.length > 100) {
                return value.substring(0, 100) + '...';
            }

            return String(value);
        }

        // โหลด fields ของ collection
        async function loadCollectionFields(collectionName) {
            try {
                const result = await eel.get_collection_fields(currentConnection.name, currentDatabase, collectionName)();

                if (result.success) {
                    currentFields = result.fields;
                    populateSearchFields(result.fields);
                }
            } catch (error) {
                console.error('เกิดข้อผิดพลาดในการโหลด fields:', error);
            }
        }

        // เติมข้อมูล fields ใน dropdown
        function populateSearchFields(fields) {
            const fieldSelect = document.getElementById('search-field');
            fieldSelect.innerHTML = '<option value="">เลือกฟิลด์</option>';

            fields.forEach(field => {
                const option = document.createElement('option');
                option.value = field;
                option.textContent = field;
                fieldSelect.appendChild(option);
            });
        }

        // ดำเนินการค้นหา
        async function performSearch() {
            const field = document.getElementById('search-field').value;
            const operator = document.getElementById('search-operator').value;
            const value = document.getElementById('search-value').value;

            if (!field || !operator || !value) {
                showAlert('กรุณากรอกข้อมูลการค้นหาให้ครบถ้วน', 'แจ้งเตือน', 'warning');
                return;
            }

            try {
                // แสดง loading
                document.getElementById('data-content').innerHTML = `
                    <div class="loading">
                        <div class="spinner"></div>
                        กำลังค้นหาข้อมูล...
                    </div>
                `;

                const result = await eel.get_collection_data(
                    currentConnection.name,
                    currentDatabase,
                    currentCollection,
                    50,
                    field,
                    operator,
                    value
                )();

                if (result.success) {
                    displayData(result.data);
                } else {
                    document.getElementById('data-content').innerHTML = `
                        <div class="alert alert-danger">${result.message}</div>
                    `;
                }
            } catch (error) {
                document.getElementById('data-content').innerHTML = `
                    <div class="alert alert-danger">เกิดข้อผิดพลาดในการค้นหา</div>
                `;
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }

        // ล้างการค้นหา
        async function clearSearch() {
            // รีเซ็ตฟอร์ม
            document.getElementById('search-field').value = '';
            document.getElementById('search-operator').value = '';
            document.getElementById('search-value').value = '';

            try {
                // แสดง loading
                document.getElementById('data-content').innerHTML = `
                    <div class="loading">
                        <div class="spinner"></div>
                        กำลังโหลดข้อมูล...
                    </div>
                `;

                // โหลดข้อมูลทั้งหมดใหม่
                const result = await eel.get_collection_data(currentConnection.name, currentDatabase, currentCollection, 50)();

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

        // นำเข้า collection จากไฟล์ JSON
        async function importCollection() {
            if (!currentConnection || !currentDatabase) {
                showAlert('กรุณาเลือกฐานข้อมูลก่อน', 'แจ้งเตือน', 'warning');
                return;
            }

            try {
                const result = await eel.import_collection(currentConnection.name, currentDatabase)();

                if (result.success) {
                    showAlert(result.message, 'นำเข้าสำเร็จ', 'success');
                    // โหลด collections ใหม่
                    await loadCollections();
                } else {
                    if (result.message !== 'ไม่ได้เลือกไฟล์') {
                        showAlert(result.message, 'แจ้งเตือน', 'error');
                    }
                }
            } catch (error) {
                showAlert('เกิดข้อผิดพลาดในการนำเข้า collection', 'ผิดพลาด', 'error');
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }

        // ส่งออก collections ที่เลือกเป็นไฟล์ JSON
        async function exportSelectedCollections() {
            const checked = document.querySelectorAll('.collection-checkbox:checked');
            if (checked.length === 0) {
                showAlert('กรุณาเลือก collection ที่ต้องการส่งออก', 'แจ้งเตือน', 'warning');
                return;
            }

            const names = Array.from(checked).map(cb => cb.dataset.collection);

            try {
                const result = await eel.export_collections(currentConnection.name, currentDatabase, names)();

                if (result.success) {
                    showAlert(result.message, 'ส่งออกสำเร็จ', 'success');
                } else {
                    if (result.message !== 'ยกเลิกการส่งออก' && result.message !== 'ไม่ได้เลือกโฟลเดอร์') {
                        showAlert(result.message, 'ผิดพลาด', 'error');
                    }
                }
            } catch (error) {
                showAlert('เกิดข้อผิดพลาดในการส่งออก collections', 'ผิดพลาด', 'error');
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }

        // กลับไปหน้าแรก
        function goBack() {
            sessionStorage.removeItem('currentConnection');
            window.location.href = 'index.html?v=' + new Date().getTime();
        }

        // แสดง modal ล้างข้อมูล
        function showDeleteModal() {
            if (!currentCollection) return;

            document.getElementById('modal-collection-name').textContent = currentCollection;
            document.getElementById('confirm-collection-name').value = '';
            document.getElementById('delete-modal').style.display = 'flex';
            document.getElementById('confirm-collection-name').focus();
        }

        // ซ่อน modal ล้างข้อมูล
        function hideDeleteModal() {
            document.getElementById('delete-modal').style.display = 'none';
        }

        // ยืนยันการล้างข้อมูล
        async function confirmDelete() {
            if (!currentCollection || !currentConnection || !currentDatabase) return;

            const confirmCollectionName = document.getElementById('confirm-collection-name').value.trim();

            if (!confirmCollectionName) {
                showAlert('กรุณากรอกชื่อ collection เพื่อยืนยัน', 'แจ้งเตือน', 'warning');
                return;
            }

            try {
                const result = await eel.clear_collection(
                    currentConnection.name,
                    currentDatabase,
                    currentCollection,
                    confirmCollectionName
                )();

                if (result.success) {
                    showAlert(result.message, 'สำเร็จ', 'success');
                    hideDeleteModal();
                    // โหลดข้อมูลใหม่
                    await selectCollection(currentCollection);
                } else {
                    showAlert(result.message, 'ผิดพลาด', 'error');
                }
            } catch (error) {
                showAlert('เกิดข้อผิดพลาดในการล้างข้อมูล', 'ผิดพลาด', 'error');
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }

        // ปิด modal เมื่อคลิกพื้นหลัง
        document.addEventListener('DOMContentLoaded', function () {
            document.getElementById('delete-modal').addEventListener('click', function (e) {
                if (e.target === this) {
                    hideDeleteModal();
                }
            });

            // เพิ่ม event listener สำหรับ Enter key ใน input
            document.getElementById('confirm-collection-name').addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    confirmDelete();
                }
            });
        });

        // ------------------ Alert & Confirm Logic ------------------ //
        function showAlert(message, title = 'แจ้งเตือน', type = 'info') {
            const modal = document.getElementById('alert-modal');
            const titleEl = document.getElementById('alert-modal-title');
            const msgEl = document.getElementById('alert-modal-message');
            const okBtn = document.getElementById('alert-modal-ok');

            titleEl.textContent = title;
            titleEl.className = 'generic-modal-title ' + type;
            msgEl.textContent = message;

            modal.classList.add('show');

            // ใช้ Promise สำหรับ wait ให้คนคลิก (แม้ไม่ต้องการค่าส่งกลับ มักมีประโยชน์)
            return new Promise(resolve => {
                const closeAlert = () => {
                    modal.classList.remove('show');
                    okBtn.removeEventListener('click', closeAlert);
                    resolve();
                };
                okBtn.addEventListener('click', closeAlert);
            });
        }

        function showConfirm(message, title = 'ยืนยันการดำเนินการ') {
            const modal = document.getElementById('confirm-modal');
            const titleEl = document.getElementById('confirm-modal-title');
            const msgEl = document.getElementById('confirm-modal-message');
            const yesBtn = document.getElementById('confirm-modal-yes');
            const noBtn = document.getElementById('confirm-modal-no');

            titleEl.textContent = title;
            msgEl.textContent = message;

            modal.classList.add('show');

            return new Promise(resolve => {
                const cleanup = () => {
                    modal.classList.remove('show');
                    yesBtn.removeEventListener('click', onYes);
                    noBtn.removeEventListener('click', onNo);
                };

                const onYes = () => { cleanup(); resolve(true); };
                const onNo = () => { cleanup(); resolve(false); };

                yesBtn.addEventListener('click', onYes);
                noBtn.addEventListener('click', onNo);
            });
        }
    </script>
</body>

</html>"""
