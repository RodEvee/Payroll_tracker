"""
Database Service
Handles SQLite connection, schema, and CRUD operations.
"""

import sqlite3
import os
import bcrypt
from datetime import datetime

DB_PATH = 'payroll_data.db'

def get_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database schemas"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')
    
    # Time Entries Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS time_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        clock_in TEXT NOT NULL,
        clock_out TEXT,
        hours REAL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # User Settings Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_settings (
        user_id INTEGER PRIMARY KEY,
        hourly_rate REAL DEFAULT 25.00,
        overtime_threshold REAL DEFAULT 40.0,
        overtime_multiplier REAL DEFAULT 1.5,
        health_insurance_employee REAL DEFAULT 150.00,
        health_insurance_employer REAL DEFAULT 300.00,
        dental_insurance REAL DEFAULT 25.00,
        vision_insurance REAL DEFAULT 15.00,
        retirement_401k_type TEXT DEFAULT 'percentage',
        retirement_401k_amount REAL DEFAULT 5.0,
        biometric_enabled BOOLEAN DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# --- Auth Operations ---

def create_user(username, password):
    """Create a new user and populate default settings"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "Username already exists"
    
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    now = datetime.now().isoformat()
    
    try:
        cursor.execute("INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)", 
                       (username, password_hash, now))
        user_id = cursor.lastrowid
        # Populate default settings for the new user
        cursor.execute("INSERT INTO user_settings (user_id) VALUES (?)", (user_id,))
        conn.commit()
        return True, "User created successfully"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def verify_user(username, password):
    """Verify user credentials and return user_id if successful"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return True, user['id']
    return False, None

# --- Time Entry Operations ---

def add_time_entry(user_id, clock_in, clock_out, hours, date):
    """Add a completed time entry"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO time_entries (user_id, clock_in, clock_out, hours, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, clock_in, clock_out, hours, date))
    conn.commit()
    conn.close()

def get_user_entries(user_id):
    """Get all time entries for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, clock_in, clock_out, hours, date FROM time_entries WHERE user_id = ? ORDER BY clock_in DESC", (user_id,))
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return entries

# --- Settings Operations ---

def get_user_settings(user_id):
    """Get full settings dictionary for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        settings = dict(row)
        # Convert sqlite booleans to python bools
        settings['biometric_enabled'] = bool(settings.get('biometric_enabled', True))
        return settings
    return None

def update_user_settings(user_id, settings_dict):
    """Update settings for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        UPDATE user_settings 
        SET hourly_rate=?, overtime_threshold=?, overtime_multiplier=?,
            health_insurance_employee=?, health_insurance_employer=?,
            dental_insurance=?, vision_insurance=?,
            retirement_401k_type=?, retirement_401k_amount=?,
            biometric_enabled=?
        WHERE user_id=?
    '''
    
    values = (
        settings_dict.get('hourly_rate', 25.00),
        settings_dict.get('overtime_threshold', 40.0),
        settings_dict.get('overtime_multiplier', 1.5),
        settings_dict.get('health_insurance_employee', 150.00),
        settings_dict.get('health_insurance_employer', 300.00),
        settings_dict.get('dental_insurance', 25.00),
        settings_dict.get('vision_insurance', 15.00),
        settings_dict.get('retirement_401k_type', 'percentage'),
        settings_dict.get('retirement_401k_amount', 5.0),
        1 if settings_dict.get('biometric_enabled', True) else 0,
        user_id
    )
    
    cursor.execute(query, values)
    conn.commit()
    conn.close()
