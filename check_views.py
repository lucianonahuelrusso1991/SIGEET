import ast

with open('gestion/views.py', 'r', encoding='utf-8') as f:
    source = f.read()

tree = ast.parse(source)

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        # check if 'es_solo_tutor' is called in the body
        calls_tutor = False
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and child.func.id == 'es_solo_tutor':
                calls_tutor = True
        
        if calls_tutor:
            decorators = [ast.unparse(d) for d in node.decorator_list]
            print(f"Function: {node.name}")
            print(f"Decorators: {decorators}")
            print("---")
