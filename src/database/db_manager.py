import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    """مدير قاعدة البيانات SQLite"""
    
    def __init__(self, db_path="data/lawyer_archive.db"):
        self.db_path = db_path
        os.makedirs("data", exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """الاتصال بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الموكلين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_number INTEGER UNIQUE,
                name TEXT NOT NULL,
                address TEXT,
                status TEXT,
                phone TEXT,
                start_date DATE NOT NULL,
                power_number TEXT,
                power_letter TEXT,
                power_date DATE,
                power_type TEXT,
                power_notarized TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الخصوم
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS opponents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                serial_number INTEGER,
                name TEXT NOT NULL,
                address TEXT,
                status TEXT,
                phone TEXT,
                lawyer TEXT,
                FOREIGN KEY(client_id) REFERENCES clients(id)
            )
        ''')
        
        # جدول القضايا
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                serial_number INTEGER,
                case_number TEXT,
                case_year TEXT,
                case_type TEXT,
                subject TEXT,
                court TEXT,
                final_judgment TEXT,
                FOREIGN KEY(client_id) REFERENCES clients(id)
            )
        ''')
        
        # جدول الجلسات والقرارات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER NOT NULL,
                session_date DATE,
                decision TEXT,
                FOREIGN KEY(case_id) REFERENCES cases(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, username: str, encrypted_password: str):
        """إضافة مستخدم جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (username, encrypted_password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user(self, username: str):
        """الحصول على بيانات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def add_client(self, client_data: dict):
        """إضافة موكل جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO clients (serial_number, name, address, status, phone, 
                                    start_date, power_number, power_letter, power_date, 
                                    power_type, power_notarized)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(client_data.values()))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"خطأ في إضافة الموكل: {e}")
            return None
        finally:
            conn.close()
    
    def get_all_clients(self):
        """الحصول على جميع الموكلين"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients ORDER BY serial_number')
        clients = cursor.fetchall()
        conn.close()
        return clients
    
    def get_client(self, client_id: int):
        """الحصول على بيانات موكل معين"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
        client = cursor.fetchone()
        conn.close()
        return client
    
    def update_client(self, client_id: int, client_data: dict):
        """تحديث بيانات الموكل"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            update_query = f'''
                UPDATE clients SET 
                {', '.join([f'{key} = ?' for key in client_data.keys()])},
                updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            '''
            cursor.execute(update_query, list(client_data.values()) + [client_id])
            conn.commit()
            return True
        except Exception as e:
            print(f"خطأ في تحديث الموكل: {e}")
            return False
        finally:
            conn.close()
    
    def search_clients(self, search_criteria: dict):
        """البحث عن الموكلين"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM clients WHERE 1=1'
        params = []
        
        for key, value in search_criteria.items():
            if value:
                query += f' AND {key} LIKE ?'
                params.append(f'%{value}%')
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
