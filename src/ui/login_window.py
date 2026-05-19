from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from src.database.db_manager import DatabaseManager
from src.utils.security import PasswordManager

class LoginWindow(QMainWindow):
    """نافذة الدخول"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.security = PasswordManager()
        self.init_ui()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("مكتب أحمد عبدالمحسن المحامي")
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        # Widget مركزي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # العنوان
        title_label = QLabel("مكتب أحمد عبدالمحسن المحامي")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # البيانات الاتصالية
        contact_label = QLabel("☎ 01112809072  |  01288441428")
        contact_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(contact_label)
        
        main_layout.addSpacing(20)
        
        # حقل اسم المستخدم
        username_label = QLabel("اسم المستخدم:")
        main_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("أدخل اسم المستخدم")
        main_layout.addWidget(self.username_input)
        
        # حقل كلمة المرور
        password_label = QLabel("كلمة المرور:")
        main_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("أدخل كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        main_layout.addWidget(self.password_input)
        
        main_layout.addSpacing(20)
        
        # زر الدخول
        login_button = QPushButton("دخول")
        login_button.clicked.connect(self.login)
        main_layout.addWidget(login_button)
        
        # زر إنشاء حساب جديد
        register_button = QPushButton("إنشاء حساب جديد")
        register_button.clicked.connect(self.register)
        main_layout.addWidget(register_button)
        
        central_widget.setLayout(main_layout)
    
    def login(self):
        """التحقق من بيانات الدخول"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال جميع البيانات!")
            return
        
        user = self.db.get_user(username)
        if user and self.security.verify_password(password, user['password']):
            QMessageBox.information(self, "نجاح", "تم تسجيل الدخول بنجاح!")
            # سيتم فتح الشاشة الرئيسية هنا لاحقاً
            self.close()
        else:
            QMessageBox.critical(self, "خطأ", "بيانات الدخول غير صحيحة!")
    
    def register(self):
        """إنشاء حساب جديد"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال جميع البيانات!")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "تحذير", "كلمة المرور يجب أن تكون 6 أحرف على الأقل!")
            return
        
        encrypted_password = self.security.encrypt_password(password)
        if self.db.add_user(username, encrypted_password):
            QMessageBox.information(self, "نجاح", "تم إنشاء الحساب بنجاح!")
            self.username_input.clear()
            self.password_input.clear()
        else:
            QMessageBox.critical(self, "خطأ", "اسم المستخدم موجود بالفعل!")
