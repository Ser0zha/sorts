from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                              QWizard, QWizardPage, QVBoxLayout, QLineEdit, 
                              QCheckBox, QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt

class RegistrationWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация пользователя")
        
        # Страница 1: Логин и пароль
        self.page1 = QWizardPage()
        self.page1.setTitle("Учетные данные")
        
        layout1 = QVBoxLayout()
        self.login_edit = QLineEdit()
        self.login_edit.setPlaceholderText("Логин")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Пароль")
        self.password_edit.setEchoMode(QLineEdit.Password)
        
        layout1.addWidget(self.login_edit)
        layout1.addWidget(self.password_edit)
        self.page1.setLayout(layout1)
        
        # Страница 2: ФИО
        self.page2 = QWizardPage()
        self.page2.setTitle("Персональные данные")
        
        layout2 = QVBoxLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Фамилия")
        self.surname_edit = QLineEdit()
        self.surname_edit.setPlaceholderText("Имя")
        self.patronymic_edit = QLineEdit()
        self.patronymic_edit.setPlaceholderText("Отчество")
        
        layout2.addWidget(self.name_edit)
        layout2.addWidget(self.surname_edit)
        layout2.addWidget(self.patronymic_edit)
        self.page2.setLayout(layout2)
        
        # Страница 3: Интересы
        self.page3 = QWizardPage()
        self.page3.setTitle("Интересы")
        
        layout3 = QVBoxLayout()
        self.interests_list = QListWidget()
        interests = ["Программирование", "Дизайн", "Маркетинг", "Аналитика", "Менеджмент"]
        for interest in interests:
            item = QListWidgetItem(interest)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.interests_list.addItem(item)
        
        self.newsletter_check = QCheckBox("Согласен на рассылку")
        
        layout3.addWidget(self.interests_list)
        layout3.addWidget(self.newsletter_check)
        self.page3.setLayout(layout3)
        
        # Добавляем страницы в Wizard
        self.addPage(self.page1)
        self.addPage(self.page2)
        self.addPage(self.page3)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setGeometry(100, 100, 400, 300)
        
        self.button = QPushButton("Зарегистрироваться", self)
        self.button.setGeometry(150, 100, 150, 30)
        self.button.clicked.connect(self.show_wizard)
        
        self.label = QLabel("Информация о пользователе будет отображена здесь", self)
        self.label.setGeometry(50, 150, 300, 100)
        self.label.setWordWrap(True)
    
    def show_wizard(self):
        wizard = RegistrationWizard(self)
        if wizard.exec() == QWizard.Accepted:
            # Собираем данные из Wizard
            login = wizard.login_edit.text()
            password = wizard.password_edit.text()
            name = f"{wizard.name_edit.text()} {wizard.surname_edit.text()} {wizard.patronymic_edit.text()}"
            
            # Собираем выбранные интересы
            interests = []
            for i in range(wizard.interests_list.count()):
                item = wizard.interests_list.item(i)
                if item.checkState() == Qt.Checked:
                    interests.append(item.text())
            
            newsletter = "да" if wizard.newsletter_check.isChecked() else "нет"
            
            # Формируем информацию для вывода
            info = (f"Логин: {login}\n"
                   f"Пароль: {'*' * len(password)}\n"
                   f"ФИО: {name}\n"
                   f"Интересы: {', '.join(interests)}\n"
                   f"Рассылка: {newsletter}")
            
            self.label.setText(info)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()