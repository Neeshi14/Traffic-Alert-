from app import app, db  # Import both app and db

# Ensure the app context is pushed
with app.app_context():
    db.create_all()
    print("Database created successfully!")
