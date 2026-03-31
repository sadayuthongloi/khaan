import os
import sys

# PyInstaller --windowed sets stdout/stderr to None; Bottle (used by eel) expects .write()
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")

import eel
from database_manager import MongoDBConnectionManager, MongoDBClient


# Configure Eel
eel.init('html')

# Create manager instances
connection_manager = MongoDBConnectionManager()


# Eel functions for JavaScript
@eel.expose
def get_connections():
    """Return all connections to JavaScript"""
    # Do not expose usernames/passwords to the UI
    sanitized = []
    for conn in connection_manager.connections:
        if not isinstance(conn, dict):
            sanitized.append(conn)
            continue
        public_conn = dict(conn)
        public_conn.pop("username", None)
        public_conn.pop("password", None)
        sanitized.append(public_conn)
    return sanitized


@eel.expose
def add_new_connection(name: str, host: str, port: int, 
                      username: str = "", password: str = ""):
    """Add new connection from JavaScript"""
    success = connection_manager.add_connection(name, host, port, username, password)
    return {
        'success': success,
        'message': 'Connection added successfully' if success else 'Error adding connection'
    }


@eel.expose
def delete_connection(name: str):
    """Delete connection from JavaScript"""
    success = connection_manager.remove_connection(name)
    return {
        'success': success,
        'message': 'Connection deleted successfully' if success else 'Error deleting connection'
    }


@eel.expose
def test_connection(name: str):
    """Test MongoDB connection"""
    try:
        connection = connection_manager.get_connection(name)
        
        if not connection:
            return {'success': False, 'message': '❌ Connection not found'}
        
        client = MongoDBClient(connection)
        result = client.test_connection()
        
        if result['success']:
            return {
                'success': True, 
                'message': f'✅ Connected to {name}\n📍 {connection["host"]}:{connection["port"]}\n🗄️ Database: {connection["database"]}'
            }
        else:
            return {'success': False, 'message': f'❌ Connection failed\n📍 {connection["host"]}:{connection["port"]}\n🔍 Error: {result["message"]}'}
            
    except Exception as e:
        return {'success': False, 'message': f'❌ Error testing connection: {str(e)}'}


@eel.expose
def use_connection(name: str):
    """Use connection and navigate to main page"""
    try:
        connection = connection_manager.get_connection(name)
        
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
        
        client = MongoDBClient(connection)
        result = client.test_connection()
        
        if result['success']:
            return {
                'success': True, 
                'connection': connection,
                'message': 'Connected successfully'
            }
        else:
            return {'success': False, 'message': f'Could not connect: {result["message"]}'}
            
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


@eel.expose
def get_databases(connection_name: str):
    """Get list of all databases"""
    try:
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
        
        client = MongoDBClient(connection)
        return client.list_databases()
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


@eel.expose
def get_collections(connection_name: str, database_name: str):
    """Get list of collections in database"""
    try:
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
        
        client = MongoDBClient(connection)
        return client.get_collections(database_name)
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


@eel.expose
def get_collection_data(connection_name: str, database_name: str, collection_name: str, limit: int = 50,
                        skip: int = 0,
                        search_field: str = "", search_operator: str = "", search_value: str = ""):
    """Get collection data with optional search and pagination"""
    try:
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
        
        client = MongoDBClient(connection)
        return client.get_collection_data(database_name, collection_name, limit, skip, search_field, search_operator, search_value)
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}

@eel.expose
def get_document(connection_name: str, database_name: str, collection_name: str, document_id: str):
    """Get single document by _id"""
    try:
        connection = connection_manager.get_connection(connection_name)
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
            
        client = MongoDBClient(connection)
        return client.get_document(database_name, collection_name, document_id)
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}

@eel.expose
def update_document(connection_name: str, database_name: str, collection_name: str, document_id: str, document_json_str: str):
    """Update single document"""
    try:
        connection = connection_manager.get_connection(connection_name)
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
            
        client = MongoDBClient(connection)
        return client.update_document(database_name, collection_name, document_id, document_json_str)
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


@eel.expose
def update_document_field(connection_name: str, database_name: str, collection_name: str, document_id: str, field_key: str, field_value_json_str: str):
    """Update single field of document"""
    try:
        connection = connection_manager.get_connection(connection_name)
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
            
        client = MongoDBClient(connection)
        return client.update_document_field(database_name, collection_name, document_id, field_key, field_value_json_str)
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


@eel.expose
def unset_document_field(connection_name: str, database_name: str, collection_name: str, document_id: str, field_key: str):
    """Remove single field from document"""
    try:
        connection = connection_manager.get_connection(connection_name)
        if not connection:
            return {'success': False, 'message': 'Connection not found'}

        client = MongoDBClient(connection)
        return client.unset_document_field(database_name, collection_name, document_id, field_key)

    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


@eel.expose
def get_collection_fields(connection_name: str, database_name: str, collection_name: str):
    """Get list of fields in collection"""
    try:
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
        
        client = MongoDBClient(connection)
        return client.get_collection_fields(database_name, collection_name)
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}



@eel.expose
def create_database(connection_name: str, database_name: str, collection_name: str):
    """Create a new database wrapper"""
    try:
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
        
        client = MongoDBClient(connection)
        return client.create_database(database_name, collection_name)
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


@eel.expose
def clear_collection(connection_name: str, database_name: str, collection_name: str, confirm_collection_name: str):
    """Clear all data in collection"""
    try:
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
        
        client = MongoDBClient(connection)
        return client.clear_collection(database_name, collection_name, confirm_collection_name)
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


@eel.expose
def drop_collections(connection_name: str, database_name: str, collection_names: list):
    """Drop selected collections"""
    try:
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
        
        client = MongoDBClient(connection)
        return client.drop_collections(database_name, collection_names)
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


@eel.expose
def import_collection(connection_name: str, database_name: str):
    """Import collection(s) from JSON file(s)"""
    import json
    import os
    import tkinter as tk
    from tkinter import filedialog
    from bson import json_util
    
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        file_paths = filedialog.askopenfilenames(
            title='Select JSON file(s) to import',
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')]
        )
        
        root.destroy()
        
        if not file_paths:
            return {'success': False, 'message': 'No file selected'}
        
        connection = connection_manager.get_connection(connection_name)
        
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
        
        results = []
        errors = []
        
        for file_path in file_paths:
            try:
                collection_name = os.path.splitext(os.path.basename(file_path))[0]
                
                documents = []
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                    if content.startswith('['):
                        documents = json_util.loads(content)
                    else:
                        for line in content.split('\n'):
                            line = line.strip()
                            if line:
                                documents.append(json_util.loads(line))
                
                client = MongoDBClient(connection)
                result = client.import_collection(database_name, collection_name, documents)
                
                if result['success']:
                    results.append(f'{collection_name}: {result["count"]} items')
                else:
                    errors.append(f'{collection_name}: {result["message"]}')
                    
            except json.JSONDecodeError as e:
                errors.append(f'{os.path.basename(file_path)}: Invalid JSON file')
            except Exception as e:
                errors.append(f'{os.path.basename(file_path)}: {str(e)}')
        
        message_parts = []
        if results:
            message_parts.append(f'Import success {len(results)} file(s):\n' + '\n'.join(results))
        if errors:
            message_parts.append(f'Failed {len(errors)} file(s):\n' + '\n'.join(errors))
        
        return {
            'success': len(results) > 0,
            'message': '\n\n'.join(message_parts),
            'imported': len(results),
            'failed': len(errors)
        }
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}

@eel.expose
def export_collections(connection_name: str, database_name: str, collection_names: list):
    """Export collections to JSON files"""
    import tkinter as tk
    from tkinter import filedialog
    import os
    
    try:
        connection = connection_manager.get_connection(connection_name)
        if not connection:
            return {'success': False, 'message': 'Connection not found'}
            
        if not collection_names:
            return {'success': False, 'message': 'No collections selected for export'}
            
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        export_dir = filedialog.askdirectory(
            title=f'Select folder to save {len(collection_names)} collections'
        )
        
        root.destroy()
        
        if not export_dir:
            return {'success': False, 'message': 'Export cancelled'}
            
        client = MongoDBClient(connection)
        return client.export_collections(database_name, collection_names, export_dir)
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}

@eel.expose
def open_mongodb_folder():
    """Open MongoDB Server folder in Windows Explorer"""
    import os
    import platform
    import subprocess
    
    path = r"C:\Program Files\MongoDB\Server"
    try:
        if platform.system() == "Windows":
            if os.path.exists(path):
                os.startfile(path)
                return {'success': True, 'message': 'Folder opened successfully'}
            else:
                return {'success': False, 'message': f'Folder not found: {path}'}
        else:
            return {'success': False, 'message': 'This feature is only supported on Windows'}
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


def main():
    """Main entry point for the application"""
    print("Starting MongoDB Connection Manager...")
    print("Open browser at: http://localhost:8000")

    try:
        eel.start('index.html', size=(1200, 800), port=8000, disable_cache=True)
    except (SystemExit, MemoryError, KeyboardInterrupt):
        print("Closing application...")



if __name__ == "__main__":
    main()
