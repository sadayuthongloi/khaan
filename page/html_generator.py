"""
HTML Generator
สร้างไฟล์ HTML สำหรับ interface ของแอปพลิเคชัน
"""

import os


class HTMLGenerator:
    """สร้างไฟล์ HTML สำหรับ interface"""
    
    def __init__(self, html_dir: str = 'html'):
        self.html_dir = html_dir
        self._ensure_html_directory()
    
    def _ensure_html_directory(self):
        """สร้างโฟลเดอร์ html ถ้ายังไม่มี"""
        if not os.path.exists(self.html_dir):
            os.makedirs(self.html_dir)
    
    def generate_index_html(self):
        """สร้างไฟล์ index.html"""
        html_content = self._get_index_html_content()
        self._write_html_file('index.html', html_content)
    
    def generate_main_html(self):
        """สร้างไฟล์ main.html"""
        html_content = self._get_main_html_content()
        self._write_html_file('main.html', html_content)
    
    def _write_html_file(self, filename: str, content: str):
        """เขียนไฟล์ HTML"""
        filepath = os.path.join(self.html_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
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
                    window.location.href = 'main.html';
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
        # อ่านจากไฟล์ main.html ที่มีอยู่แล้ว
        main_html_path = os.path.join(self.html_dir, 'main.html')
        if os.path.exists(main_html_path):
            with open(main_html_path, 'r', encoding='utf-8') as f:
                return f.read()
        return """
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
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #5a6268;
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
        
        .collections-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
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
            padding: 12px 15px;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            background: #f8f9fa;
            display: flex;
            align-items: center;
            gap: 10px;
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
        
        .collection-checkbox {
            width: 16px;
            height: 16px;
            cursor: pointer;
            accent-color: #667eea;
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
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
            display: flex;
            flex-direction: column;
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
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
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
        
        .search-form {
            background: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
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
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }
        
        .search-actions {
            display: flex;
            gap: 10px;
            align-items: end;
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
                <div class="collections-header">
                    <h3>Collections</h3>
                    <button class="btn-del" id="btn-del-collections" onclick="deleteSelectedCollections()">🗑️ Del</button>
                </div>
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
                    <div>
                        <div class="data-title" id="data-title">เลือก Collection เพื่อดูข้อมูล</div>
                        <div class="data-stats" id="data-stats"></div>
                    </div>
                    <div class="data-header-right">
                        <button class="btn btn-danger" id="delete-btn" onclick="showDeleteModal()" style="display: none;">
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
                            <button class="btn btn-secondary" onclick="clearSearch()">🗑️ ล้าง</button>
                        </div>
                    </div>
                </div>
                
                <div class="data-content" id="data-content">
                    <div class="no-data">เลือก Collection จากรายการด้านซ้ายเพื่อดูข้อมูล</div>
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

    <script type="text/javascript" src="/eel.js"></script>
    <script>
        let currentConnection = null;
        let currentCollection = null;
        let currentFields = [];
        
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
                document.getElementById('btn-del-collections').classList.remove('show');
                return;
            }
            
            const collectionsList = collections.map(collection => `
                <div class="collection-item" onclick="selectCollection('${collection}')">
                    <input type="checkbox" class="collection-checkbox" data-collection="${collection}" onclick="onCheckboxChange(event)">
                    <span class="collection-name">📄 ${collection}</span>
                </div>
            `).join('');
            
            container.innerHTML = collectionsList;
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
                alert('กรุณาเลือก collection ที่ต้องการลบ');
                return;
            }
            
            const names = Array.from(checked).map(cb => cb.dataset.collection);
            const confirmMsg = '\u0e04\u0e38\u0e13\u0e41\u0e19\u0e48\u0e43\u0e08\u0e2b\u0e23\u0e37\u0e2d\u0e44\u0e21\u0e48\u0e17\u0e35\u0e48\u0e08\u0e30\u0e25\u0e1a ' + names.length + ' collections?\\n\\n' + names.join('\\n') + '\\n\\n\u0e01\u0e32\u0e23\u0e14\u0e33\u0e40\u0e19\u0e34\u0e19\u0e01\u0e32\u0e23\u0e19\u0e35\u0e49\u0e44\u0e21\u0e48\u0e2a\u0e32\u0e21\u0e32\u0e23\u0e16\u0e22\u0e01\u0e40\u0e25\u0e34\u0e01\u0e44\u0e14\u0e49!';
            
            if (!confirm(confirmMsg)) return;
            
            try {
                const result = await eel.drop_collections(currentConnection.name, names)();
                
                if (result.success) {
                    alert(result.message);
                    // รีเซ็ต current collection ถ้าถูกลบ
                    if (currentCollection && names.includes(currentCollection)) {
                        currentCollection = null;
                        document.getElementById('data-title').textContent = 'เลือก Collection เพื่อดูข้อมูล';
                        document.getElementById('data-stats').textContent = '';
                        document.getElementById('data-content').innerHTML = '<div class="no-data">เลือก Collection จากรายการด้านซ้ายเพื่อดูข้อมูล</div>';
                        document.getElementById('search-form').style.display = 'none';
                        document.getElementById('delete-btn').style.display = 'none';
                    }
                    // โหลด collections ใหม่
                    await loadCollections();
                } else {
                    alert(result.message);
                }
            } catch (error) {
                alert('เกิดข้อผิดพลาดในการลบ collections');
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
                
                // ซ่อน search form และปุ่ม Delete
                document.getElementById('search-form').style.display = 'none';
                document.getElementById('delete-btn').style.display = 'none';
                
                // โหลดข้อมูล
                const result = await eel.get_collection_data(currentConnection.name, collectionName, 50)();
                
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
        
        // โหลด fields ของ collection
        async function loadCollectionFields(collectionName) {
            try {
                const result = await eel.get_collection_fields(currentConnection.name, collectionName)();
                
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
                alert('กรุณากรอกข้อมูลการค้นหาให้ครบถ้วน');
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
                const result = await eel.get_collection_data(currentConnection.name, currentCollection, 50)();
                
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
            if (!currentCollection || !currentConnection) return;
            
            const confirmCollectionName = document.getElementById('confirm-collection-name').value.trim();
            
            if (!confirmCollectionName) {
                alert('กรุณากรอกชื่อ collection เพื่อยืนยัน');
                return;
            }
            
            try {
                const result = await eel.clear_collection(
                    currentConnection.name, 
                    currentCollection, 
                    confirmCollectionName
                )();
                
                if (result.success) {
                    alert(result.message);
                    hideDeleteModal();
                    // โหลดข้อมูลใหม่
                    await selectCollection(currentCollection);
                } else {
                    alert(result.message);
                }
            } catch (error) {
                alert('เกิดข้อผิดพลาดในการล้างข้อมูล');
                console.error('เกิดข้อผิดพลาด:', error);
            }
        }
        
        // ปิด modal เมื่อคลิกพื้นหลัง
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('delete-modal').addEventListener('click', function(e) {
                if (e.target === this) {
                    hideDeleteModal();
                }
            });
            
            // เพิ่ม event listener สำหรับ Enter key ใน input
            document.getElementById('confirm-collection-name').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    confirmDelete();
                }
            });
        });
    </script>
</body>
</html>
        """ 