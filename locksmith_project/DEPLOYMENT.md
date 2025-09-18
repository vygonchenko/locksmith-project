# Deployment Guide

This guide will help you deploy your Locksmith project to PythonAnywhere.

## Prerequisites

1. PythonAnywhere account (free or paid)
2. GitHub account
3. Domain name (optional, recommended for production)

## Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository

```bash
# Navigate to your project directory
cd /path/to/locksmith_project

# Initialize Git
git init

# Add all files to git
git add .

# Make initial commit
git commit -m "Initial commit: Locksmith project setup"

# Add remote repository (replace with your GitHub URL)
git remote add origin https://github.com/yourusername/locksmith-project.git

# Push to GitHub
git push -u origin main
```

### 1.2 Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name it `locksmith-project`
4. Choose Public/Private
5. Don't initialize with README (we already have one)
6. Click "Create repository"
7. Copy the repository URL and use it in the git remote command above

## Step 2: PythonAnywhere Setup

### 2.1 Create PythonAnywhere Account

1. Go to [PythonAnywhere](https://www.pythonanywhere.com/)
2. Sign up for a new account
3. Choose the free plan for testing

### 2.2 Create Web App

1. Log in to PythonAnywhere
2. Go to the "Web" tab
3. Click "Add a new web app"
4. Choose:
   - Python version: 3.10 or higher
   - Web framework: Manual configuration

### 2.3 Configure WSGI File

1. Go to "Web" → "Code" → "WSGI configuration file"
2. Replace the content with:

```python
import os
import sys

# Add your project directory to the Python path
path = '/home/yourusername/locksmith_project'
if path not in sys.path:
    sys.path.append(path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locksmith_project.settings')

# Import Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

3. Replace `yourusername` with your PythonAnywhere username

### 2.4 Set Up Virtual Environment

1. Open Bash console on PythonAnywhere
2. Run:

```bash
# Navigate to home directory
cd

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r locksmith_project/requirements.txt

# Navigate to project directory
cd locksmith_project

# Run migrations
python manage.py migrate

# Create superuser (if needed)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 2.5 Configure Static Files

1. Go to "Web" → "Static files"
2. Click "Add a static file"
3. Fill in:
   - URL: `/static/`
   - Directory: `/home/yourusername/locksmith_project`

### 2.6 Set Up Environment Variables

1. Go to "Web" → "Environment variables"
2. Add your environment variables:
   ```
   DJANGO_ENV=production
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=yourusername.pythonanywhere.com
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   DEFAULT_FROM_EMAIL=your_email@gmail.com
   ```

## Step 3: Upload Your Project

### 3.1 Using Git (Recommended)

```bash
# In PythonAnywhere Bash console
cd

# Clone your repository
git clone https://github.com/yourusername/locksmith-project.git

# Navigate to project
cd locksmith-project

# Set up virtual environment and dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput
```

### 3.2 Using SFTP

1. Use any SFTP client (FileZilla, Cyberduck, etc.)
2. Connect to: `yourusername@ssh.pythonanywhere.com`
3. Navigate to: `/home/yourusername/locksmith_project`
4. Upload all your project files

## Step 4: Final Configuration

### 4.1 Update Settings

Make sure your production settings are correct:

```python
# In locksmith_project/settings/production.py
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'www.yourdomain.com']
```

### 4.2 Restart Web App

1. Go to "Web" tab
2. Click "Reload your web app"

### 4.3 Check Logs

1. Go to "Web" → "Error log"
2. Check for any errors
3. Go to "Web" → "Access log"
4. Check for successful requests

## Step 5: Set Up Custom Domain (Optional)

### 5.1 Configure DNS

1. Go to your domain registrar
2. Add an A record pointing to PythonAnywhere's IP
3. Add a CNAME record for www

### 5.2 Set Up Domain in PythonAnywhere

1. Go to "Web" → "Domain"
2. Add your domain
3. Configure SSL (if using HTTPS)

## Step 6: Maintenance

### 6.1 Updating Your Site

```bash
# SSH to PythonAnywhere
ssh yourusername@ssh.pythonanywhere.com

# Navigate to project
cd locksmith-project

# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart web app
touch /var/www/yourusername_wsgi.py
```

### 6.2 Backups

The project includes backup scripts:

```bash
# Database backup
python scripts/backup_db.py

# Project backup
python scripts/backup_project.py
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure your project path is correct in WSGI file
2. **Static Files Not Loading**: Check static files configuration
3. **Database Error**: Run migrations and check database permissions
4. **Permission Denied**: Check file permissions in your project directory

### Debug Mode

For debugging, temporarily set `DEBUG=True` in settings and check the error log.

## Support

If you encounter any issues:
1. Check the PythonAnywhere documentation
2. Review the error logs
3. Test locally first
4. Contact PythonAnywhere support if needed

---

**Note**: This guide covers deployment to PythonAnywhere. For other hosting providers, please refer to their specific documentation.