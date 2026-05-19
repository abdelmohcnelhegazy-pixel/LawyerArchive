from cryptography.fernet import Fernet
import os

class PasswordManager:
    """مدير تشفير كلمات المرور"""
    
    def __init__(self):
        self.key_file = "data/secret.key"
        self.cipher = None
        self._load_or_create_key()
    
    def _load_or_create_key(self):
        """تحميل أو إنشاء مفتاح التشفير"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            os.makedirs("data", exist_ok=True)
            with open(self.key_file, 'wb') as f:
                f.write(key)
        
        self.cipher = Fernet(key)
    
    def encrypt_password(self, password: str) -> str:
        """تشفير كلمة المرور"""
        encrypted = self.cipher.encrypt(password.encode())
        return encrypted.decode()
    
    def decrypt_password(self, encrypted_password: str) -> str:
        """فك تشفير كلمة المرور"""
        try:
            decrypted = self.cipher.decrypt(encrypted_password.encode())
            return decrypted.decode()
        except Exception as e:
            print(f"خطأ في فك التشفير: {e}")
            return None
    
    def verify_password(self, plain_password: str, encrypted_password: str) -> bool:
        """التحقق من كلمة المرور"""
        return plain_password == self.decrypt_password(encrypted_password)
