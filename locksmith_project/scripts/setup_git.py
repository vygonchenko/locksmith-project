#!/usr/bin/env python
"""
Git setup script for LOCKSMITH project.
Automates the initial Git repository setup.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(e.stderr)
        return False

def setup_git():
    """Set up Git repository for the project."""
    project_dir = Path(__file__).resolve().parent.parent
    
    print("🚀 Starting Git setup for LOCKSMITH project...")
    print(f"📁 Project directory: {project_dir}")
    
    # Check if we're in the project directory
    if not (project_dir / "manage.py").exists():
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        return False
    
    # Initialize Git repository
    if not run_command("git init", "Initializing Git repository"):
        return False
    
    # Add .gitignore
    gitignore_path = project_dir / ".gitignore"
    if gitignore_path.exists():
        run_command("git add .gitignore", "Adding .gitignore")
    
    # Add all project files
    run_command("git add .", "Adding project files")
    
    # Make initial commit
    if not run_command("git commit -m \"Initial commit: Locksmith project setup\"", "Making initial commit"):
        return False
    
    print("\n🎉 Git repository setup completed!")
    print("\n📋 Next steps:")
    print("1. Create a new repository on GitHub or GitLab")
    print("2. Copy the repository URL")
    print("3. Run: git remote add origin <your-repo-url>")
    print("4. Run: git push -u origin main")
    print("\n📖 For detailed instructions, see DEPLOYMENT.md")
    
    return True

def check_git_status():
    """Check current Git status."""
    try:
        result = subprocess.run("git status --porcelain", shell=True, 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print("\n📝 Git status:")
            print(result.stdout)
        else:
            print("\n✅ Working directory is clean")
    except subprocess.CalledProcessError:
        print("\n⚠️  Git is not initialized or not available")

if __name__ == "__main__":
    print("🔧 Git Setup Script for LOCKSMITH Project")
    print("=" * 50)
    
    # Check Git status before setup
    check_git_status()
    
    # Run setup
    success = setup_git()
    
    if success:
        print("\n🎊 Setup completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Setup failed!")
        sys.exit(1)