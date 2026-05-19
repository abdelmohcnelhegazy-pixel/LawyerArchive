import sys
from PyQt6.QtWidgets import QApplication
from src.ui.login_window import LoginWindow

def main():
    """البرنامج الرئيسي"""
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
