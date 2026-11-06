import os

class Config:
    # Секретний ключ для сесій та безпеки
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-pc-store-2026'
    
    # Підключення до локальної БД MySQL у XAMPP
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 
        'mysql+pymysql://root:@localhost/pc_hardware_store?charset=utf8mb4'
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    