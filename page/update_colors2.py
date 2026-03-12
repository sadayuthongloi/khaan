import os
import re

files = [r"d:\khaan\html\main.html", r"d:\khaan\page\html_generator.py"]

for file in files:
    if not os.path.exists(file):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Header from purple dark grey to standard dark #2c3e50 (bootstrap dark)
    content = content.replace("background: linear-gradient(135deg, #0a58ca 0%, #764ba2 100%);", "background: #2c3e50;")
    content = content.replace("background: linear-gradient(135deg, #0a58ca 0%, #764ba2 100%)", "background: #2c3e50;")
    
    # Body background from light gray to slightly lighter gray standard
    content = content.replace("background: #f5f7fa;", "background: #f8f9fa;")
    
    # Button danger from #dc3545 to standard #dc3545 (is already standard)
    # Primary button hover #084298 to standard hover
    content = content.replace("background: #084298;", "background: #0b5ed7;")

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print('Update successful 2.')
