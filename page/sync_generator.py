import os

# Path to files
main_html_path = r'd:\khaan\page\html\main.html'
generator_path = r'd:\khaan\page\html_generator.py'

# Read main.html content
with open(main_html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Read generator content
with open(generator_path, 'r', encoding='utf-8') as f:
    generator_lines = f.readlines()

# Find the start and end of _get_main_html_content return string
start_idx = -1
end_idx = -1
in_method = False
for i, line in enumerate(generator_lines):
    if 'def _get_main_html_content(self) -> str:' in line:
        in_method = True
    if in_method and 'return """' in line:
        start_idx = i
    if in_method and '</html>' in line:
        # Look ahead for the closing quotes
        if i + 1 < len(generator_lines) and '"""' in generator_lines[i+1]:
            end_idx = i + 1
            break
        elif '"""' in line:
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    new_method = [
        '    def _get_main_html_content(self) -> str:\n',
        '        """สร้างเนื้อหา main.html"""\n',
        '        return """' + html_content + '"""\n'
    ]
    
    # We need to find where the method starts exactly
    real_start = -1
    for i in range(start_idx, -1, -1):
        if 'def _get_main_html_content' in generator_lines[i]:
            real_start = i
            break
            
    if real_start != -1:
        new_generator_lines = generator_lines[:real_start] + new_method + generator_lines[end_idx+1:]
        with open(generator_path, 'w', encoding='utf-8') as f:
            f.writelines(new_generator_lines)
        print("Successfully synced html_generator.py with main.html")
    else:
        print("Could not find method start")
else:
    print(f"Indices not found: {start_idx}, {end_idx}")
