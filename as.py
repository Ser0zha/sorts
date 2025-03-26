from PySide6.QtWidgets import (QApplication, QMainWindow, QListView, QAction, 
                              QDialog, QVBoxLayout, QLabel, QLineEdit, 
                              QPushButton, QMenu)
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QDateTime

class Note:
    def __init__(self, text, date):
        self.text = text
        self.date = date

class NotesModel(QAbstractListModel):
    def __init__(self, notes=None):
        super().__init__()
        self.notes = notes or []
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.notes)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        if role == Qt.DisplayRole:
            note = self.notes[index.row()]
            return f"{note.text} ({note.date.toString('dd.MM.yyyy HH:mm')})"
        
        return None
    
    def addNote(self, note):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.notes.append(note)
        self.endInsertRows()
    
    def updateNote(self, index, text):
        if 0 <= index.row() < len(self.notes):
            self.notes[index.row()].text = text
            self.notes[index.row()].date = QDateTime.currentDateTime()
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole and index.isValid():
            self.notes[index.row()].text = value
            self.notes[index.row()].date = QDateTime.currentDateTime()
            self.dataChanged.emit(index, index)
            return True
        return False

class NoteDialog(QDialog):
    def __init__(self, parent=None, note_text=""):
        super().__init__(parent)
        self.setWindowTitle("Редактирование заметки")
        
        layout = QVBoxLayout()
        self.label = QLabel("Текст заметки:")
        self.text_edit = QLineEdit(note_text)
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)
    
    def get_note_text(self):
        return self.text_edit.text()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заметки")
        self.setGeometry(100, 100, 600, 400)
        
        # Модель и представление
        self.model = NotesModel()
        self.list_view = QListView()
        self.list_view.setModel(self.model)
        self.setCentralWidget(self.list_view)
        
        # Контекстное меню
        self.list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.show_context_menu)
        
        # Верхнее меню
        self.create_menus()
    
    def create_menus(self):
        menubar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menubar.addMenu("Файл")
        
        add_action = QAction("Добавить заметку", self)
        add_action.triggered.connect(self.add_note)
        file_menu.addAction(add_action)
        
        edit_action = QAction("Изменить заметку", self)
        edit_action.triggered.connect(self.edit_note)
        file_menu.addAction(edit_action)
    
    def show_context_menu(self, position):
        index = self.list_view.indexAt(position)
        if not index.isValid():
            return
        
        menu = QMenu()
        edit_action = menu.addAction("Изменить")
        edit_action.triggered.connect(self.edit_note)
        menu.exec(self.list_view.viewport().mapToGlobal(position))
    
    def add_note(self):
        dialog = NoteDialog(self)
        if dialog.exec() == QDialog.Accepted:
            text = dialog.get_note_text()
            if text:
                self.model.addNote(Note(text, QDateTime.currentDateTime()))
    
    def edit_note(self):
        index = self.list_view.currentIndex()
        if not index.isValid():
            return
        
        old_text = self.model.notes[index.row()].text
        dialog = NoteDialog(self, old_text)
        if dialog.exec() == QDialog.Accepted:
            new_text = dialog.get_note_text()
            if new_text:
                self.model.setData(index, new_text)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()