import datetime
import random
import sqlite3
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QInputDialog, QLabel, \
    QComboBox, QListWidget, QTextEdit, QMainWindow


class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 550, 250)
        self.setWindowTitle('Главное меню')

        # Картинка на заднем плане
        self.pixmap = QPixmap('Images/main_bg.jpeg')
        self.image = QLabel(self)
        self.image.setScaledContents(True)
        self.image.setGeometry(0, 0, 550, 250)
        self.image.setPixmap(self.pixmap)

        # получаем имя пользователя (чтоб по приличнее общаться). Пользователей немного, так что можно без пароля<)
        name = QInputDialog.getText(self, "Введите имя", "Как вас зовут?")

        self.Tip_for_today_label = QLabel(self)
        self.Tip_for_today_label.setText(f"Добро пожаловать, {name[0]}!\nЧего желаете?")
        self.Tip_for_today_label.setStyleSheet("color: white;"
                                               "font-size: 24px;"
                                               "font-weight: bold;")
        self.Tip_for_today_label.setGeometry(20, 20, 511, 61)

        # выбор программы
        self.go_to_tips_btn = QPushButton('Получить совет', self)
        self.go_to_tips_btn.setGeometry(30, 120, 181, 71)
        self.go_to_tips_btn.clicked.connect(self.go_to_tips)

        self.go_to_horoscope_btn = QPushButton('Гороскоп', self)
        self.go_to_horoscope_btn.setGeometry(340, 120, 181, 71)
        self.go_to_horoscope_btn.clicked.connect(self.go_to_horoscope)

    def go_to_tips(self):  # переходим в приложение tips
        self.tip_app = Tip_app()
        self.tip_app.show()

    def go_to_horoscope(self):  # переходим в приложение horoscope
        self.horoscope_pp = Horoscope_app()
        self.horoscope_pp.show()


# приложение с советами
class Tip_app(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # настраиваем экран
        self.setGeometry(200, 200, 801, 534)
        self.setWindowTitle('Совет на день')

        # Картинка на заднем плане
        self.pixmap = QPixmap('Images/TIPS_bg.jpg')
        self.image = QLabel(self)
        self.image.setScaledContents(True)
        self.image.setGeometry(0, 0, 801, 534)
        self.image.setPixmap(self.pixmap)

        # label'ы
        self.Tip_for_today_label = QLabel(self)
        self.Tip_for_today_label.setText("~Какой же совет ты ждешь от меня сегодня?")
        self.Tip_for_today_label.setStyleSheet("color: white;"
                                               "font-size: 26px;"
                                               "font-weight: bold;")
        self.Tip_for_today_label.setGeometry(100, 60, 591, 41)

        self.choose_categories_label = QLabel(self)
        self.choose_categories_label.setText("Выбери интересующую тебя категорию")
        self.choose_categories_label.setStyleSheet("color: white;"
                                                   "font-size: 18px;")
        self.choose_categories_label.setGeometry(230, 110, 341, 21)

        # Combobox для более конкретного выбора
        self.genre_combobox = QComboBox(self)
        self.genre_combobox.addItems(('Совет', 'Мотивация', 'Цитаты великих людей', 'Народная мудрость'))
        self.genre_combobox.setGeometry(270, 140, 261, 35)

        # результаты - label и сам результат в QTextEdit
        self.result_tip_label = QLabel(self)
        self.result_tip_label.setText("Накопленные знания:")
        self.result_tip_label.setStyleSheet("color: white;"
                                            "font-size: 16px;")
        self.result_tip_label.setGeometry(100, 225, 171, 20)
        self.result_tip_label.hide()  # прячем, так как пользователь не просит совета во время запуска программы

        # список полученных советов
        self.result_tip = QListWidget(self)
        self.result_tip.setGeometry(100, 250, 581, 211)
        self.result_tip.hide()  # прячем, так как пользователь не просит совета во время запуска программы

        # записываем данные, которые уже были в файле
        with open('Tips_list.txt', "rt", encoding="utf8") as records:
            for day_tip in records.readlines():
                self.result_tip.insertItem(0,
                                           f"{day_tip.split(';')[0]}: {day_tip.split(';')[1]}")  # добавляем в список

        # сообщение о том, что уже получали совет
        self.wait_tip_label = QLabel(self)
        self.wait_tip_label.setText('Вы уже получили свой совет. Дождитесь завтра')
        self.wait_tip_label.setStyleSheet("color: white;")
        self.wait_tip_label.setGeometry(100, 465, 311, 16)
        self.wait_tip_label.hide()  # прячем

        # QPushButton, при нажатии на которую сгенерируется ответ
        self.get_answer_btn = QPushButton('Получить благословение богов', self)
        self.get_answer_btn.setGeometry(280, 185, 231, 41)
        self.get_answer_btn.clicked.connect(self.get_answer)

        # 'инструкция' о том, как выйти из программы
        self.instruction_text = QLabel(self)
        self.instruction_text.setText("Чтобы закрыть услугу, просто нажмите на крестик в левом верхнем углу")
        self.instruction_text.setStyleSheet("color: rgb(85,85,85);"
                                            "font-size: 8px;")
        self.instruction_text.setGeometry(10, 497, 381, 16)

    def get_answer(self):  # получаем совет

        # отображаем поле ответа
        self.result_tip_label.show()
        self.result_tip.show()

        attempt = False  # можно ли получить сегодня совет

        with open('Tips_list.txt', "rt",
                  encoding="utf8") as records:  # проверка на наличие попыток для получение совета
            for day_tip in records.readlines():
                if day_tip.split(";")[0] == str(
                        datetime.datetime.now().date()):  # проверяем, получали ли мы уже совет
                    self.wait_tip_label.show()  # показываем сообщение о том, что сегодня уже получили совет
                    break
            else:
                attempt = True  # можно получить совет
                self.wait_tip_label.hide()  # скрываем надпись, потому что уже не нужна

        if attempt:
            Type = self.genre_combobox.currentText()
            with open('Tips_list.txt', "wt", encoding="utf8") as records:  # Записываем совет в файл
                with sqlite3.connect('Database.db') as con:  # Подключение к БД
                    cur = con.cursor()  # Создание курсора
                    advices = cur.execute(
                        f"""select Tip from Tips where Type = '{Type}'""").fetchall()  # Выполнение запроса
                    advice = random.choice(advices)  # получаем один рандомный совет из подходящих
                    self.result_tip.insertItem(0, f"{datetime.datetime.now().date()}: {advice[0]}")
                records.write(f"{datetime.datetime.now().date()};{advice[0]}")  # Записываем в файл

        # Выводим советы
        self.result_tip.show()


# приложение с гороскопом
class Horoscope_app(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # настраиваем экран
        self.setGeometry(200, 200, 801, 534)
        self.setWindowTitle('Гороскоп')

        # Картинка на заднем плане
        self.pixmap = QPixmap('Images/Horoscope_bg.jpeg')
        self.image = QLabel(self)
        self.image.setScaledContents(True)
        self.image.setGeometry(0, 0, 801, 534)
        self.image.setPixmap(self.pixmap)

        # label'ы
        self.Tip_for_today_label = QLabel(self)
        self.Tip_for_today_label.setText("Ну чтож, усторим тебе гадание!")
        self.Tip_for_today_label.setStyleSheet("color: white;"
                                               "font-size: 26px;"
                                               "font-weight: bold;")
        self.Tip_for_today_label.setGeometry(215, 10, 415, 31)

        self.choose_categories_label = QLabel(self)
        self.choose_categories_label.setText("Выбери свой знак зодиака")
        self.choose_categories_label.setStyleSheet("color: white;"
                                                   "font-size: 18px;"
                                                   "font-weight: bold;")
        self.choose_categories_label.setGeometry(284, 56, 245, 20)

        # QPushButton'ы, при нажатии на которые сгенерируется ответ
        self.Aries_btn = QPushButton('Овен', self)
        self.Aries_btn.setGeometry(10, 110, 111, 61)
        self.Aries_btn.setStyleSheet("background: rgb(0,255,255);")
        self.Aries_btn.clicked.connect(self.get_prognoz)

        self.Taurus_btn = QPushButton('Телец', self)
        self.Taurus_btn.setGeometry(140, 110, 111, 61)
        self.Taurus_btn.setStyleSheet("background: rgb(0,255,255);")
        self.Taurus_btn.clicked.connect(self.get_prognoz)

        self.Gemini_btn = QPushButton('Близнецы', self)
        self.Gemini_btn.setGeometry(270, 110, 111, 61)
        self.Gemini_btn.setStyleSheet("background: rgb(0,255,255);")
        self.Gemini_btn.clicked.connect(self.get_prognoz)

        self.Cancer_btn = QPushButton('Рак', self)
        self.Cancer_btn.setGeometry(400, 110, 111, 61)
        self.Cancer_btn.setStyleSheet("background: rgb(0,255,255);")
        self.Cancer_btn.clicked.connect(self.get_prognoz)

        self.Leo_btn = QPushButton('Лев', self)
        self.Leo_btn.setGeometry(530, 110, 111, 61)
        self.Leo_btn.setStyleSheet("background: rgb(0,255,255);")
        self.Leo_btn.clicked.connect(self.get_prognoz)

        self.Virgo_btn = QPushButton('Дева', self)
        self.Virgo_btn.setGeometry(660, 110, 111, 61)
        self.Virgo_btn.setStyleSheet("background: rgb(0,255,255);")
        self.Virgo_btn.clicked.connect(self.get_prognoz)

        self.Libra_btn = QPushButton('Весы', self)
        self.Libra_btn.setGeometry(10, 190, 111, 61)
        self.Libra_btn.setStyleSheet("background: rgb(0,255,255);")
        self.Libra_btn.clicked.connect(self.get_prognoz)

        self.Scorpio_btn = QPushButton('Скорпион', self)
        self.Scorpio_btn.setGeometry(140, 190, 111, 61)
        self.Scorpio_btn.setStyleSheet("background: rgb(0,255,255);")
        self.Scorpio_btn.clicked.connect(self.get_prognoz)

        self.Sagittarius_btn = QPushButton('Стрелец', self)
        self.Sagittarius_btn.setGeometry(270, 190, 111, 61)
        self.Sagittarius_btn.setStyleSheet("background: rgb(0,255,255);")
        self.Sagittarius_btn.clicked.connect(self.get_prognoz)

        self.Capricorn_btn = QPushButton('Козерог', self)
        self.Capricorn_btn.setGeometry(400, 190, 111, 61)
        self.Capricorn_btn.setStyleSheet("background: rgb(0,255,255);")
        self.Capricorn_btn.clicked.connect(self.get_prognoz)

        self.Aquarius_btn = QPushButton('Водолей', self)
        self.Aquarius_btn.setGeometry(530, 190, 111, 61)
        self.Aquarius_btn.setStyleSheet("background: rgb(0,255,255);")
        self.Aquarius_btn.clicked.connect(self.get_prognoz)

        self.Pisces_btn = QPushButton('Рыбы', self)
        self.Pisces_btn.setGeometry(660, 190, 111, 61)
        self.Pisces_btn.setStyleSheet("background: rgb(0,255,255);")
        self.Pisces_btn.clicked.connect(self.get_prognoz)

        # список полученных советов
        self.result_horoscope = QTextEdit(self)
        self.result_horoscope.setGeometry(10, 270, 761, 201)
        self.result_horoscope.hide()  # прячем, так как пользователь не просит совета во время запуска программы

        # сообщение о том, что уже получали предсказание
        self.wait_horoscope_label = QLabel(self)
        self.wait_horoscope_label.setText('Вы уже получили свое предсказание. Дождитесь завтра')
        self.wait_horoscope_label.setStyleSheet("color: white;")
        self.wait_horoscope_label.setGeometry(10, 480, 361, 16)
        self.wait_horoscope_label.hide()  # прячем

        # 'инструкция' о том, как выйти из программы
        self.instruction_text = QLabel(self)
        self.instruction_text.setText("Чтобы закрыть услугу, просто нажмите на крестик в левом верхнем углу")
        self.instruction_text.setStyleSheet("color: black;"
                                            "font-size: 8px;")
        self.instruction_text.setGeometry(10, 497, 381, 16)

    def get_prognoz(self):  # получаем предсказание

        attempt = False  # можно ли получить сегодня предсказание

        with open('Horoscope_list.txt', "rt",
                  encoding="utf8") as records:  # проверка на наличие попыток для получение предсказания
            for day_tip in records.readlines():
                if day_tip.split(";")[0] == str(
                        datetime.datetime.now().date()):  # проверяем, получали ли мы уже предсказание
                    # показываем сообщение о том, что сегодня уже получили предсказание
                    self.wait_horoscope_label.show()
                    break
            else:
                attempt = True  # можно получить предсказание
                self.wait_horoscope_label.hide()  # скрываем надпись, потому что уже не нужна

        if attempt:
            # Заготовки предложений
            first = ["Сегодня — идеальный день для новых начинаний.",
                     "Оптимальный день для того, чтобы решиться на смелый поступок!",
                     "Будьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.",
                     "Лучшее время для того, чтобы начать новые отношения или разобраться со старыми.",
                     "Плодотворный день для того, чтобы разобраться с накопившимися делами."]

            second = ["Но помните, что даже в этом случае нужно не забывать про",
                      "Если поедете за город, заранее подумайте про",
                      "Те, кто сегодня нацелен выполнить множество дел, должны помнить про",
                      "Если у вас упадок сил, обратите внимание на",
                      "Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про"]

            second_add = ["отношения с друзьями и близкими.",
                          "работу и деловые вопросы, которые могут так некстати помешать планам.",
                          "себя и своё здоровье, иначе к вечеру возможен полный раздрай.",
                          "бытовые вопросы — особенно те, которые вы не доделали вчера.",
                          "отдых, чтобы не превратить себя в загнанную лошадь в конце месяца."]

            third = ["Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.",
                     "Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.",
                     "Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела "
                     "до конца.", "Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.",
                     "Если встретите незнакомца на пути — проявите участие, "
                     "и тогда эта встреча посулит вам приятные хлопоты."]

            horoscope = random.choice(first) + random.choice(second) + random.choice(second_add) + random.choice(
                third)
            self.result_horoscope.setText(horoscope)  # задаем текст
            self.result_horoscope.show()
            with open('Horoscope_list.txt', "wt", encoding="utf8") as records:  # Записываем в файл
                records.write(f"{datetime.datetime.now().date()};{horoscope}")

        # Выводим предсказания
        self.result_horoscope.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_window()
    ex.show()
    sys.exit(app.exec_())
