#!/usr/bin/env python
"""
Project backup script for LOCKSNITH project.
Creates a complete backup of the project structure.
"""

import os
import sys
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

def create_project_backup():
    """Create a complete backup of the project."""
    try:
        # Get the project base directory
        project_dir = Path(__file__).resolve().parent.parent
        backups_dir = project_dir / 'backups' / 'project'
        
        # Create backups directory if it doesn't exist
        backups_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'locksmith_project_backup_{timestamp}.zip'
        backup_path = backups_dir / backup_filename
        
        # List of files and directories to backup
        backup_items = [
            'core',
            'locksmith_project',
            'templates',
            'media',
            'requirements.txt',
            '.env.example',
            'README.md'
        ]
        
        # Create zip file
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in backup_items:
                item_path = project_dir / item
                if item_path.exists():
                    if item_path.is_file():
                        zipf.write(item_path, item)
                    else:
                        for root, dirs, files in os.walk(item_path):
                            for file in files:
                                file_path = Path(root) / file
                                arcname = str(file_path.relative_to(project_dir))
                                zipf.write(file_path, arcname)
        
        # Keep only the last 3 project backups
        backup_files = sorted(backups_dir.glob('locksmith_project_backup_*.zip'), 
                            key=lambda x: x.stat().st_ctime, reverse=True)
        
        for old_backup in backup_files[3:]:
            old_backup.unlink()
        
        print(f"✅ Project backup created successfully: {backup_path}")
        print(f"📁 Backup location: {backups_dir}")
        print(f"🗑️  Older backups removed (kept last 3)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating project backup: {e}")
        return False

if __name__ == '__main__':
    print("🔄 Starting project backup...")
    success = create_project_backup()
    sys.exit(0 if success else 1)