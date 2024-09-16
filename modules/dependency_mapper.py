import os

def parse_requirements(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def map_dependencies(repo_dir):
    dependencies = []
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    imports = [line for line in content.split('\n') if line.startswith('import') or line.startswith('from')]
                    for imp in imports:
                        dependencies.append((file_path, imp))
    return dependencies
