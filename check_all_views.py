import ast

with open('gestion/views.py', 'r', encoding='utf-8') as f:
    source = f.read()

tree = ast.parse(source)

staff_decorator = 'user_passes_test(lambda u: u.is_staff or u.is_superuser)'
staff_decorator2 = 'user_passes_test(lambda u: u.is_staff)'

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        decorators = [ast.unparse(d) for d in node.decorator_list]
        if 'login_required' in decorators and not any('user_passes_test' in d for d in decorators):
            print(f"{node.name}")
