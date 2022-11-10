import os
import sqlite3
import sys
import webbrowser
from random import randint

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QAbstractItemView
from PyQt5.QtWidgets import QWidget, QScrollArea, QPlainTextEdit, QLineEdit, QTableView, QGridLayout
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

class MainWindow(QWidget):
    def __init__(self, allcoun, choisenocountry):
        super().__init__()
        self.setWindowTitle("Main")
        self.setGeometry(300, 300, 300, 300)
        self.label = QLabel("Вы знаете куда хотите отправиться\n \tв путешествие?", self)
        self.label.move(10, 10)
        self.label.resize(300, 50)
        self.label.setFont(QFont("Comic Sans MS", 12))
        self.allcoun = allcoun # экземпляр класса Allcountry(все страны)
        self.choisenocountry = choisenocountry # экземпляр класс choisenocountry (не выбрал страну)

        self.button = QPushButton(self)
        self.button.move(90, 80)
        self.button.resize(100, 100)
        self.button.setStyleSheet("background-image : url(image/yes.png);")
        self.button.clicked.connect(self.yes_action)

        self.button_2 = QPushButton(self)
        self.button_2.move(90, 190)
        self.button_2.resize(100, 100)
        self.button_2.setStyleSheet("background-image : url(image/no.png);")
        self.button_2.clicked.connect(self.no_action)

    def yes_action(self):
        self.allcoun.show()
        self.hide()

    def no_action(self, ):
        self.choisenocountry.show()
        self.hide()


class Allcountry(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('All list country')
        self.setGeometry(300, 300, 680, 650)

        self.gridLayout = QGridLayout(self)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.move(10, 10)
        self.scrollArea.resize(650, 590)

        self.buttons = [] # здесь хранятся все кнопки
        self.w = QWidget()
        self.no_coun = No_Country_Window() # экземпляр класса No_Country_Window(нет моей страны)

        for i in range(9):
            for j in range(4):
                self.pb = QPushButton(self)
                self.pb.setFixedSize(150, 100)
                self.buttons.append(self.pb)
                self.gridLayout.addWidget(self.pb, i, j)
        self.w.setLayout(self.gridLayout)
        self.scrollArea.setWidget(self.w)
        for i in range(37):
            read_blob_data(i)  # достаёт из базы данных фото
        for e in self.buttons:
            e.setStyleSheet(f"background-image : url(flags/im_{self.buttons.index(e) + 1}.png);")
            e.clicked.connect(self.go_to_info)

        self.but_not_my_country = QPushButton("Нет моей страны :(", self)
        self.but_not_my_country.move(10, 600)
        self.but_not_my_country.resize(650, 40)
        self.but_not_my_country.clicked.connect(self.go_to_no_country)

        self.but_back = QPushButton("Вернуться назад", self)
        self.but_back.move(10, 650)
        self.but_back.resize(650, 40)
        self.but_back.clicked.connect(self.show_main)

    def go_to_info(self):
        sender: QPushButton = self.sender()
        index = str(self.buttons.index(sender) + 1)
        self.inform = InfoWidget(index)
        self.inform.show()

    def go_to_no_country(self):
        self.no_coun.show()
        self.hide()

    def show_main(self):
        pass


class Choise_no_country(QWidget):
    def __init__(self, randcountry):
        super().__init__()
        self.setWindowTitle('Choise no country')
        self.setGeometry(300, 300, 320, 200)
        self.label = QLabel("Как вы хотите узнать выбрать страну?", self)
        self.label.move(10, 10)
        self.label.resize(300, 20)
        self.label.setFont(QFont("Comic Sans MS", 12))
        self.randcountry = randcountry

        self.one_var = QPushButton("Таблица стран по посещаемости", self)
        self.one_var.move(30, 40)
        self.one_var.resize(250, 30)
        self.one_var.clicked.connect(tablecountry.show)
        self.one_var.setFont(QFont("Comic Sans MS", 11))

        self.two_var = QPushButton("Пройти тест", self)
        self.two_var.move(30, 80)
        self.two_var.resize(250, 30)
        #self.two_var.clicked.connect(self.test_show)
        self.two_var.setFont(QFont("Comic Sans MS", 11))

        self.three_var = QPushButton("Рандомный выбор страны", self)
        self.three_var.move(30, 120)
        self.three_var.resize(250, 30)
        self.three_var.clicked.connect(randcountry.show)
        self.three_var.setFont(QFont("Comic Sans MS", 11))


class TableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Table')
        self.setGeometry(300, 300, 400, 460)
        self.table_w = QTableView(self)
        self.table_w.move(20, 20)
        self.table_w.resize(370, 400)
        self.table_w.pressed.connect(self.rowselect)

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("project_country")
        db.open()
        model = QSqlTableModel(self, db)
        model.setTable("country")
        model.setFilter("""1=1 ORDER BY count DESC""")
        model.select()
        self.table_w.setModel(model)
        self.table_w.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.but_more = QPushButton("Узнать больше о", self)
        self.but_more.move(20, 430)
        self.but_more.resize(370, 30)
        self.but_more.clicked.connect(self.go_to_info)

    def rowselect(self, index):
        self.index = index.sibling(index.row(), 0).data()
        self.inform = InfoWidget(str(self.index))

    def go_to_info(self):
        self.inform.show()


class RandomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Random country')
        self.setGeometry(300, 300, 300, 250)
        self.but_coun = QPushButton(self)
        self.but_coun.move(70, 30)
        self.but_coun.resize(150, 100)

        self.random = randint(1, 36)
        self.but_coun.setStyleSheet(f"background-image : url(flags/im_{self.random}.png);")
        self.but_coun.clicked.connect(self.go_to_info)

        self.but = QPushButton(self)
        self.but.resize(150, 75)
        self.but.move(70, 140)
        self.but.setStyleSheet("background-image : url(image/go.png);")
        self.but.clicked.connect(self.view)

    def view(self):
        self.random = randint(1, 36)
        self.but_coun.setStyleSheet(f"background-image : url(flags/im_{self.random}.png);")

    def go_to_info(self):
        index = self.random
        self.inform = InfoWidget(index)
        self.inform.show()


class InfoWidget(QWidget):
    def __init__(self, index):
        super().__init__()
        self.setWindowTitle('Info country')
        self.setGeometry(300, 300, 520, 400)
        self.name = QLabel(self)
        self.name.move(20, 10)
        self.name.resize(180, 60)

        # получение названия страны из базы данных
        con = sqlite3.connect("project_country")
        cur = con.cursor()
        name = f"""SELECT * FROM country WHERE id = {index}"""
        cur.execute(name)
        name_coun = cur.fetchall()
        if len(name_coun[0][1]) * 15 < self.name.size().width():
            self.name.setText(name_coun[0][1])
        else:
            replaced_name = name_coun[0][1].replace(" ", "\n    ")
            self.name.setText(replaced_name)
        self.name.setFont(QFont("Comic Sans MS", 13))

        self.label = QLabel(self)
        self.label.move(20, 75)
        self.label.resize(150, 98)
        self.label.setStyleSheet(f"background-image : url(flags/im_{index}.png);")  # поставить картинку

        self.label_2 = QLabel(self)
        self.label_2.move(190, 20)
        self.label_2.resize(150, 150)
        self.label_2.setStyleSheet(f"background-image : url(img_coun/inim_{index}.png);")  # поставить картинку

        self.but = QPushButton(self)
        self.but.move(350, 20)
        self.but.resize(150, 150)
        self.but.setStyleSheet(f"background-image : url(image/avia_ticket.png);")
        #self.but.clicked.connect()

        self.scrollArea = QScrollArea(self)
        self.scrollArea.move(20, 180)
        self.scrollArea.resize(480, 200)

        self.plan_text = QPlainTextEdit(self)
        self.plan_text.move(20, 180)
        self.plan_text.resize(480, 200)
        self.set_info_text(index)
        self.scrollArea.setWidget(self.plan_text)

    def set_info_text(self, index):
        with open(f"info_coun/info_{index}.txt", encoding="utf8") as file:
            self.plan_text.setPlainText(file.read())


def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)


# достаёт картинку из базы данных
def read_blob_data(emp_id):
    try:
        sqlite_connection = sqlite3.connect('project_country')
        cursor = sqlite_connection.cursor()

        sql_fetch_blob_query = """SELECT * from coun_img where id = ?"""
        cursor.execute(sql_fetch_blob_query, (emp_id,))
        record = cursor.fetchall()
        for row in record:
            name = row[0]
            photo = row[1]

            photo_path = os.path.join(f"flags/im_{str(name)}.png")
            write_to_file(photo, photo_path)
        cursor.close()

    except sqlite3.Error as error:
        # print("Ошибка при работе с SQLite", error)
        pass
    finally:
        if sqlite_connection:
            sqlite_connection.close()


class No_Country_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('No Country')
        self.setGeometry(300, 300, 400, 300)
        self.label = QLabel("Напишите название страны:", self)
        self.label.move(10, 10)
        self.label.resize(300, 20)
        self.label.setFont(QFont("Comic Sans MS", 12))

        self.write_coun = QLineEdit(self)
        self.write_coun.resize(300, 30)
        self.write_coun.move(10, 40)

        self.add = QPushButton("Добавить", self)
        self.add.move(320, 40)
        self.add.resize(75, 30)
        self.add.clicked.connect(self.check)
        self.add.setFont(QFont("Comic Sans MS", 11))

        self.label_2 = QLabel(self)
        self.label_2.move(80, 80)
        self.label_2.resize(300, 40)
        self.label_2.setFont(QFont("Comic Sans MS", 12))

        self.go_to_her = QPushButton('Перейти к ней!', self)
        self.go_to_her.move(70, 110)
        self.go_to_her.resize(250, 30)
        self.go_to_her.setFont(QFont("Comic Sans MS", 12))
        self.go_to_her.hide()
        self.go_to_her.clicked.connect(self.go_to_info)

        self.fin_label = QLabel(self)
        self.fin_label.move(70, 150)
        self.fin_label.resize(250, 140)

    def check(self):
        name = self.write_coun.text().capitalize()
        con = sqlite3.connect("project_country")
        cur = con.cursor()
        check_id_name = f"""SELECT id FROM country WHERE name = '{name}'"""
        cur.execute(check_id_name)
        self.x = cur.fetchall()
        if self.x:
            self.label_2.setText('Ура, эта страна у нас есть!')
            self.go_to_her.show()
            self.fin_label.setStyleSheet("background-image : url(image/yra.jpg);")
        else:
            self.label_2.setText(" Спасибо, что сообщили,\n мы обязательно её добавим!")
            self.go_to_her.hide()
            self.fin_label.setStyleSheet("background-image : url(image/senks.jpg);")
            id_name = f"""SELECT id FROM country WHERE name = '{name}'"""
            if cur.execute(id_name).fetchall() != '[]':
                add_name = f"""INSERT INTO no_country (name) VALUES('{name}')"""
                print(add_name)
                new = cur.execute(add_name)
                con.commit()

    def go_to_info(self):
        self.inform = InfoWidget(self.x[0][0])
        self.inform.show()


def expert_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    allcountry = Allcountry()
    randcountry = RandomWidget()
    tablecountry = TableWindow()
    # testcountry = TestWindow()
    choisenocountry = Choise_no_country(randcountry)
    main = MainWindow(allcountry, choisenocountry)
    main.show()
    sys.excepthook = expert_hook
    sys.exit(app.exec())