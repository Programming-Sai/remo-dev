import os
import sys
import random
import string
from pathlib import Path

def random_filename():
    """Generate a unique random filename with timestamp to avoid collisions."""
    timestamp = int(time.time() * 1000) % 100000
    letters = ''.join(random.choices(string.ascii_lowercase, k=6))
    extensions = ['.txt', '.log', '.json', '.py', '.csv']
    return f"{letters}_{timestamp}{random.choice(extensions)}"

def random_content(size_kb):
    """Generate random text content of approx size."""
    size_bytes = int(size_kb * 1024)
    chars = string.ascii_letters + string.digits + ' \n'
    return ''.join(random.choices(chars, k=size_bytes))

def create_nested_path(base, depth):
    """Create nested folder path of given depth."""
    path = base
    for i in range(depth):
        path = path / f"level_{i}"
    path.mkdir(parents=True, exist_ok=True)
    return path

def create_test_files(directory, file_count=15, max_depth=3):
    """Create random test files with variable nesting depth."""
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating {file_count} test files in {target} (max depth: {max_depth})...")
    print("-" * 50)
    
    for i in range(file_count):
        size_kb = random.randint(1, 100)
        filename = random_filename()
        depth = random.randint(0, max_depth)
        
        if depth == 0:
            filepath = target / filename
        else:
            filepath = create_nested_path(target, depth) / filename
        
        # Ensure we don't overwrite existing files
        counter = 1
        original_path = filepath
        while filepath.exists():
            filepath = original_path.parent / f"{original_path.stem}_{counter}{original_path.suffix}"
            counter += 1
        
        content = random_content(size_kb)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        rel_path = filepath.relative_to(target)
        print(f"  Created: {rel_path} ({size_kb} KB)")
    
    print("-" * 50)
    print(f"Done! Check {target}")

if __name__ == '__main__':
    import time  # Added for timestamp in filename
    
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = 'test_dir'
    
    max_depth = 3
    if len(sys.argv) > 2:
        max_depth = int(sys.argv[2])
    
    create_test_files(test_dir, max_depth=max_depth)