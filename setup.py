import os
import sqlite3
import subprocess

def run_command(cmd):
    print(f"➜ Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ Warning: {result.stderr}")
    return result

def auto_setup():
    print("🚀 Starting E-Learn PDF System Setup...\n")
    
    # 1. Make migrations
    print("📦 Creating migrations...")
    run_command("python manage.py makemigrations")
    
    # 2. Migrate
    print("\n🗄️  Applying migrations...")
    run_command("python manage.py migrate")
    
    # 3. Create superuser with a direct SQL approach (bypass prompt)
    print("\n👤 Setting up admin user...")
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Minor.settings')
        django.setup()

        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("✅ Admin user created: username='admin', password='admin123'")
        else:
            print("✅ Admin user already exists")
    except Exception as e:
        print(f"⚠️ Could not auto-create superuser: {e}")
        print("Please run: python manage.py createsuperuser")
    # 4. Add initial branches and semesters
    print("\n📚 Adding branches and semesters...")
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        branches = [
            ('CS', 'Computer Science Engineering'),
            ('ME', 'Mechanical Engineering'),
            ('Civil', 'Civil Engineering'),
            ('ET', 'Electronics Engineering')
        ]
        
        for code, name in branches:
            # Insert branch
            cursor.execute("INSERT OR IGNORE INTO myapp_branch (code, name) VALUES (?, ?)", [code, name])
            
            # Get branch id
            cursor.execute("SELECT id FROM myapp_branch WHERE code = ?", [code])
            branch_row = cursor.fetchone()
            if branch_row:
                branch_id = branch_row[0]
                # Insert semesters 1-6
                for sem in range(1, 7):
                    cursor.execute("INSERT OR IGNORE INTO myapp_semester (branch_id, semester_number) VALUES (?, ?)", [branch_id, sem])
        
        conn.commit()
        conn.close()
        print("✅ Branches and Semesters added successfully!")
    except Exception as e:
        print(f"⚠️ Note: {e}")
        print("You can add branches manually from admin panel.")
    
    print("\n" + "="*50)
    print("✅ SETUP COMPLETE!")
    print("="*50)
    print("\n📌 Next steps:")
    print("1. Start server: python manage.py runserver")
    print("2. Open browser: http://127.0.0.1:8000")
    print("3. Admin panel: http://127.0.0.1:8000/admin")
    print("4. Login: username='admin', password='admin123'")
    print("5. Add Subjects and Upload PDFs from admin panel\n")

if __name__ == '__main__':
    auto_setup()