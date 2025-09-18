#!/usr/bin/env python
"""
Deployment check script for LOCKSMITH project.
Checks if the project is ready for deployment.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (MISSING)")
        return False

def check_command_exists(command, description):
    """Check if a command exists."""
    try:
        subprocess.run([command, "--version"], capture_output=True, check=True)
        print(f"✅ {description}: Available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ {description}: Not available")
        return False

def check_python_version():
    """Check Python version."""
    try:
        result = subprocess.run(["python", "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"📋 Python version: {version}")
        
        # Check if Python version is compatible (3.8+)
        version_parts = version.replace("Python ", "").split(".")
        major, minor = int(version_parts[0]), int(version_parts[1])
        
        if major > 3 or (major == 3 and minor >= 8):
            print("✅ Python version is compatible")
            return True
        else:
            print("❌ Python version is not compatible (requires 3.8+)")
            return False
    except Exception as e:
        print(f"❌ Error checking Python version: {e}")
        return False

def check_django_installation():
    """Check if Django is properly installed."""
    try:
        result = subprocess.run(["python", "-c", "import django; print(django.VERSION)"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Django installation: {version}")
            return True
        else:
            print("❌ Django is not properly installed")
            return False
    except Exception as e:
        print(f"❌ Error checking Django installation: {e}")
        return False

def check_git_setup():
    """Check Git setup."""
    try:
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git is properly set up")
            return True
        else:
            print("❌ Git is not set up or not available")
            return False
    except Exception as e:
        print(f"❌ Error checking Git setup: {e}")
        return False

def check_required_files():
    """Check if all required files exist."""
    print("\n📁 Checking required files...")
    
    required_files = [
        ("manage.py", "Django management script"),
        ("requirements.txt", "Python dependencies"),
        (".env.example", "Environment variables template"),
        (".gitignore", "Git ignore file"),
        ("README.md", "Project documentation"),
        ("DEPLOYMENT.md", "Deployment guide"),
        ("locksmith_project/settings/base.py", "Base settings"),
        ("core/templates/base.html", "Base template"),
        ("core/templates/home.html", "Home template"),
        ("core/static/css/main.css", "Main CSS"),
        ("core/static/js/main.js", "Main JavaScript"),
        ("scripts/setup_git.py", "Git setup script"),
        ("scripts/deploy_check.py", "Deployment check script"),
    ]
    
    missing_files = []
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            missing_files.append(filepath)
    
    return len(missing_files) == 0

def check_environment_variables():
    """Check environment variables."""
    print("\n🔧 Checking environment variables...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found (create from .env.example)")
        return False
    
    print("✅ .env file exists")
    return True

def check_database_settings():
    """Check database settings."""
    print("\n💾 Checking database settings...")
    
    settings_file = Path("locksmith_project/settings/base.py")
    if not settings_file.exists():
        print("❌ Base settings file not found")
        return False
    
    try:
        with open(settings_file, 'r') as f:
            content = f.read()
            if 'sqlite3' in content:
                print("✅ Database configuration: SQLite (development)")
                return True
            elif 'postgresql' in content:
                print("✅ Database configuration: PostgreSQL (production)")
                return True
            else:
                print("⚠️  Database configuration not recognized")
                return False
    except Exception as e:
        print(f"❌ Error checking database settings: {e}")
        return False

def check_static_files():
    """Check static files configuration."""
    print("\n🎨 Checking static files...")
    
    settings_file = Path("locksmith_project/settings/base.py")
    if not settings_file.exists():
        print("❌ Base settings file not found")
        return False
    
    try:
        with open(settings_file, 'r') as f:
            content = f.read()
            if 'STATIC_URL' in content and 'STATIC_ROOT' in content:
                print("✅ Static files configuration is present")
                return True
            else:
                print("❌ Static files configuration missing")
                return False
    except Exception as e:
        print(f"❌ Error checking static files configuration: {e}")
        return False

def generate_deployment_report():
    """Generate a deployment readiness report."""
    print("\n📊 Deployment Readiness Report")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Django Installation", check_django_installation),
        ("Git Setup", check_git_setup),
        ("Required Files", check_required_files),
        ("Environment Variables", check_environment_variables),
        ("Database Settings", check_database_settings),
        ("Static Files", check_static_files),
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        try:
            if check_func():
                passed += 1
        except Exception as e:
            print(f"❌ Error in {check_name}: {e}")
    
    print(f"\n📈 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Your project is ready for deployment!")
        print("\n🚀 Next steps:")
        print("1. Run: python scripts/setup_git.py")
        print("2. Create repository on GitHub/GitLab")
        print("3. Follow DEPLOYMENT.md guide")
        return True
    else:
        print(f"\n⚠️  {total - passed} checks failed. Please fix them before deploying.")
        return False

if __name__ == "__main__":
    print("🔍 Deployment Readiness Checker")
    print("=" * 40)
    
    ready = generate_deployment_report()
    
    if ready:
        print("\n✅ Your project is deployment ready!")
        sys.exit(0)
    else:
        print("\n❌ Your project needs fixes before deployment.")
        sys.exit(1)