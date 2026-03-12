import os

files = [r"d:\khaan\page\html\main.html", r"d:\khaan\page\html_generator.py"]

for file in files:
    if not os.path.exists(file):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Backgrounds
    content = content.replace("background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);", "background: #f4f6f9;")
    content = content.replace("background: #f5f7fa;", "background: #f8f9fa;")
    
    # 2. Header
    content = content.replace("linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "#343a40")
    
    # 3. Main Primary Button Colors
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
    content = content.replace("border-bottom: 2px solid #667eea;", "border-bottom: 2px solid #0a58ca;")
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print('Replacement complete.')
