import os
import glob

template_dir = r'd:\Escritorio\GESTION ESCOLAR\gestion\templates\gestion'

for filepath in glob.glob(os.path.join(template_dir, '**', '*.html'), recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if table is present but not already responsive
    if '<table' in content and 'class="table-responsive"' not in content:
        # Wrap table with div
        content = content.replace('<table', '<div class="table-responsive">\n<table')
        content = content.replace('</table>', '</table>\n</div>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Patched {os.path.basename(filepath)}')
