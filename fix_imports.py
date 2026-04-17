# fix_imports.py
import os
import re

def fix_imports_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Reemplazar importaciones relativas
    content = re.sub(r'from \.\.database', 'from database', content)
    content = re.sub(r'from \.\.auth', 'from auth', content)
    content = re.sub(r'from \.\.models', 'from models', content)
    content = re.sub(r'from \.\.schemas', 'from schemas', content)
    content = re.sub(r'from \.\.repositories', 'from repositories', content)
    content = re.sub(r'from \.\.services', 'from services', content)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Fixed: {filepath}")

# Recorrer todos los archivos Python
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            fix_imports_in_file(filepath)

print("✅ Todas las importaciones han sido corregidas")