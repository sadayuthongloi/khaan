import os
import re

files = [r"d:\khaan\html\main.html", r"d:\khaan\page\html_generator.py"]

for file in files:
    if not os.path.exists(file):
        print(f"File not found: {file}")
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Background of the app (from dark gradient to light flat gray)
    content = content.replace("background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);", "background: #f4f6f9;")
    
    # 2. Header (from gradient to standard dark flat)
    content = content.replace("linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "#343a40")
    
    # 3. Main Primary Button Colors (from bright purple/blue to standard bootstrap primary)
    content = content.replace("#667eea", "#0a58ca")
    content = content.replace("#5a6fd8", "#084298")
    
    # 4. Remove heavy box shadows
    content = content.replace("box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);", "box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);")
    content = content.replace("box-shadow: 0 20px 40px rgba(0,0,0,0.1);", "box-shadow: 0 4px 6px rgba(0,0,0,0.1);")
    content = content.replace("box-shadow: 0 20px 40px rgba(0,0,0,0.3);", "box-shadow: 0 4px 6px rgba(0,0,0,0.1);")
    content = content.replace("box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);", "box-shadow: 0 1px 3px rgba(0,0,0,0.05);")
    content = content.replace("box-shadow: 0 10px 25px rgba(0,0,0,0.1);", "box-shadow: 0 4px 12px rgba(0,0,0,0.08);")
    content = content.replace("box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);", "box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);")
    
    # 5. Make headers stand out properly on the new dark background
    content = content.replace("color: #333;\n            margin-bottom: 20px;\n            font-size: 1.5em;\n            border-bottom: 2px solid #667eea;", "color: #333;\n            margin-bottom: 20px;\n            font-size: 1.5em;\n            border-bottom: 2px solid #0a58ca;")
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print('Update successful.')
