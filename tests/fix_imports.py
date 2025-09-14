#!/usr/bin/env python3
"""
Fix import statements after file reorganization
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix import statements in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # Fix neural imports
        if 'from neural.neural_data_store import' in content:
            content = content.replace('from neural.neural_data_store import', 'from neural.neural_data_store import')
            changes_made.append('neural_data_store import')
        
        if 'import neural.neural_data_store' in content:
            content = content.replace('import neural.neural_data_store', 'import neural.neural_data_store')
            changes_made.append('neural_data_store module import')
            
        # Fix other neural imports
        neural_modules = [
            'neural_api', 'neural_launcher', 'neural_pattern_analyzer', 
            'neural_web_dashboard', 'standalone_neural_dashboard'
        ]
        
        for module in neural_modules:
            if f'from {module} import' in content:
                content = content.replace(f'from {module} import', f'from neural.{module} import')
                changes_made.append(f'{module} import')
            if f'import {module}' in content:
                content = content.replace(f'import {module}', f'import neural.{module}')
                changes_made.append(f'{module} module import')
        
        # Fix core module imports (should be from src.module)
        core_modules = [
            'consciousness_engine', 'memory_manager', 'personality_engine', 
            'database', 'models', 'token_counter', 'neural_monitor', 'web_search'
        ]
        
        for module in core_modules:
            # Only fix if not already using src. prefix
            if f'from {module} import' in content and f'from src.{module} import' not in content:
                content = content.replace(f'from {module} import', f'from src.{module} import')
                changes_made.append(f'{module} import')
            if f'import {module}' in content and f'import src.{module}' not in content:
                content = content.replace(f'import {module}', f'import src.{module}')
                changes_made.append(f'{module} module import')
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes_made
        
        return None
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    """Fix all import statements in the project"""
    print("🔧 Fixing import statements after file reorganization...")
    
    # Files to check and fix
    files_to_check = []
    
    # Root directory Python files
    root_dir = Path('.')
    for file_path in root_dir.glob('*.py'):
        files_to_check.append(file_path)
    
    # Source directory files
    src_dir = root_dir / 'src'
    if src_dir.exists():
        for file_path in src_dir.glob('*.py'):
            files_to_check.append(file_path)
    
    # Test files
    test_dirs = ['tests/unit', 'tests/integration']
    for test_dir in test_dirs:
        test_path = root_dir / test_dir
        if test_path.exists():
            for file_path in test_path.glob('*.py'):
                files_to_check.append(file_path)
    
    # Neural directory files
    neural_dir = root_dir / 'neural'
    if neural_dir.exists():
        for file_path in neural_dir.glob('*.py'):
            files_to_check.append(file_path)
    
    # Examples directory
    examples_dir = root_dir / 'examples'
    if examples_dir.exists():
        for file_path in examples_dir.glob('*.py'):
            files_to_check.append(file_path)
    
    print(f"Checking {len(files_to_check)} Python files...")
    
    total_files_fixed = 0
    for file_path in files_to_check:
        changes = fix_imports_in_file(file_path)
        if changes:
            print(f"✅ Fixed {file_path}: {', '.join(changes)}")
            total_files_fixed += 1
    
    if total_files_fixed == 0:
        print("✅ No additional import fixes needed!")
    else:
        print(f"✅ Fixed imports in {total_files_fixed} files!")

if __name__ == "__main__":
    main()
