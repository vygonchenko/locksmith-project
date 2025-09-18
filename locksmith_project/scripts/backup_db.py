#!/usr/bin/env python
"""
Database backup script for LOCKSNITH project.
Creates backups of the SQLite database.
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

def create_database_backup():
    """Create a backup of the SQLite database."""
    try:
        # Get the project base directory
        project_dir = Path(__file__).resolve().parent.parent
        db_path = project_dir / 'db.sqlite3'
        backups_dir = project_dir / 'backups' / 'database'
        
        # Create backups directory if it doesn't exist
        backups_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'locksmith_db_backup_{timestamp}.sqlite3'
        backup_path = backups_dir / backup_filename
        
        # Copy the database file
        shutil.copy2(db_path, backup_path)
        
        # Keep only the last 5 backups
        backup_files = sorted(backups_dir.glob('locksmith_db_backup_*.sqlite3'), 
                            key=lambda x: x.stat().st_ctime, reverse=True)
        
        for old_backup in backup_files[5:]:
            old_backup.unlink()
        
        print(f"✅ Database backup created successfully: {backup_path}")
        print(f"📁 Backup location: {backups_dir}")
        print(f"🗑️  Older backups removed (kept last 5)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating database backup: {e}")
        return False

if __name__ == '__main__':
    print("🔄 Starting database backup...")
    success = create_database_backup()
    sys.exit(0 if success else 1)