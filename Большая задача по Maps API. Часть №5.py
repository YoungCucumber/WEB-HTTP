import os
import sys

import requests
from PyQt5 import QtGui, Qt
from PyQt5.Qt import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 500]
APIKEY = "40d1649f-0493-4b70-98ba-98533de7710b"


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.ll = '135,-30'
        self.spn = '35,35'
        self.l = 'map'

        self.image = QLabel(self)
        self.image.move(0, 50)
        self.image.resize(600, 450)

        self.entry = QLineEdit(self)
        self.entry.move(5, 5)

        self.btn = QPushButton(self, text='Искать')
        self.btn.clicked.connect(self.set_pos)
        self.btn.move(150, 5)

        self.setFocus()
        self.initUI()

    def get_image(self, pt):
        map_request = self.get_link(pt)
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def set_spn(self, val):
        spn = list(map(float, self.spn.split(',')))
        spn[0] = spn[0] + val if spn[0] + val > 1 else spn[0] + val / 10
        spn[1] = spn[1] + val if spn[1] + val > 1 else spn[1] + val / 10
        spn[0] = spn[0] if spn[0] > 0 else 0.0001
        spn[1] = spn[1] if spn[1] > 0 else 0.0001
        self.spn = ','.join(list(map(str, spn)))

    def set_ll(self, dy, dx):
        ll = list(map(float, self.ll.split(',')))
        y, x = ll
        x, y = x + dx, y + dy
        self.ll = f'{y},{x}'

    def set_l(self, l):
        self.l = l

    def get_link(self, pt=False):
        if pt:
            return f'https://static-maps.yandex.ru/1.x/?spn={self.spn}&l={self.l}&pt={self.ll},pmwtm1'
        else:
            return f'https://static-maps.yandex.ru/1.x/?ll={self.ll}&spn={self.spn}&l={self.l}&pt={self.ll},pmwtm1'

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        key = a0.key()

        if key == Qt.Key_PageUp:
            self.set_spn(-1)
        elif key == Qt.Key_PageDown:
            self.set_spn(1)
        elif key == Qt.Key_Up:
            self.set_ll(0, 1)
        elif key == Qt.Key_Down:
            self.set_ll(0, -1)
        elif key == Qt.Key_Left:
            self.set_ll(-1, 0)
        elif key == Qt.Key_Right:
            self.set_ll(1, 0)
        elif key == Qt.Key_1:
            self.set_l('map')
        elif key == Qt.Key_2:
            self.set_l('sat')
        elif key == Qt.Key_3:
            self.set_l('sat,skl')

        self.set_image()

    def get_street_pos(self, street):
        response = requests.get(
            f"http://geocode-maps.yandex.ru/1.x/?apikey={APIKEY}&geocode={street}&format=json")
        data = response.json()
        pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')
        return pos

    def set_pos(self):
        street = self.entry.text()
        pos = self.get_street_pos(street)
        self.ll = ','.join(pos)
        self.set_image(True)

    def set_image(self, pt=False):
        self.get_image(pt)
        self.pixmap = QPixmap('map.png')
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.set_image(False)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
