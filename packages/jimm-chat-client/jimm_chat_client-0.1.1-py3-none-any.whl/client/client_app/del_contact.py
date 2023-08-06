import sys
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QApplication
from PyQt5.QtCore import Qt


class DelContactDialog(QDialog):
    """
    Диалог удаления контакта. Предлагает текущий список контактов,
    не имеет обработчиков для действий.
    """
    def __init__(self, database):
        super().__init__()
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Удаление контакта')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 30)
        self.selector.move(10, 30)
        # заполнитель контактов для удаления
        self.selector.addItems(sorted(self.database.get_contacts()))

        self.btn_ok = QPushButton('Удалить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    from client_db import ClientDatabase
    database = ClientDatabase('test1')
    window = DelContactDialog(database)
    database.add_contact('test1')
    database.add_contact('test2')
    print(database.get_contacts())
    window.selector.addItems(sorted(database.get_contacts()))
    window.show()
    app.exec_()
