import os
import sys
from pprint import pprint
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
        self.map_type = 'map'

        self.image = QLabel(self)
        self.image.move(0, 50)
        self.image.resize(600, 450)

        self.entry = QLineEdit(self)
        self.entry.move(5, 5)

        self.bnt_search = QPushButton(self, text='Искать')
        self.bnt_search.clicked.connect(self.set_pos)
        self.bnt_search.move(150, 5)
        self.existing_points = []

        self.btn_delete = QPushButton(self, text='Сброс поискового результата')
        self.btn_delete.clicked.connect(self.delete_point)
        self.btn_delete.move(400, 5)

        self.switch = QCheckBox(self)
        self.switch.stateChanged.connect(self.switch_index)
        self.switch.move(380, 10)

        self.lbl_switch = QLabel(self)
        self.lbl_switch.setText('Включить индекс: ')
        self.lbl_switch.move(270, 10)


        self.full_address = QLabel(self)
        self.full_address.move(5, 30)

        self.index_state = False
        self.setFocus()
        self.init_ui()

    def switch_index(self):
        self.index_state = not self.index_state

    def delete_point(self):
        if len(self.existing_points) != 0:
            self.existing_points.pop(-1)
            self.set_image()
            self.full_address.setText('')

    def get_image(self):
        map_request = self.get_link()
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
        if -84 < x < 84:
            x += dx
        if -179 < y < 179:
            y += dy
        self.ll = f'{y},{x}'

    def set_l(self, map_type):
        self.map_type = map_type

    def get_link(self):
        if len(self.existing_points) != 0:
            points = []
            for i in range(len(self.existing_points)):
                point = [str(i) for i in (self.existing_points[i] + [i + 1])]
                points.append(','.join(point))
            str_point = '~'.join(points)
            return f'https://static-maps.yandex.ru/1.x/?ll={self.ll}&spn={self.spn}&l={self.map_type}&pt={str_point}'
        else:
            return f'https://static-maps.yandex.ru/1.x/?ll={self.ll}&spn={self.spn}' \
                   f'&l={self.map_type}'

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

    def get_street_info(self, street):
        response = requests.get(
            f"http://geocode-maps.yandex.ru/1.x/?apikey={APIKEY}&geocode={street}&format=json")
        data = response.json()
        try:
            pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')
            fa = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
                'GeocoderMetaData']['text']
            if self.index_state:
                index = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
                    'GeocoderMetaData']['Address']['postal_code']
            else:
                index = ''

            self.existing_points.append(pos)
        except Exception as e:
            print(e)
            pos = self.ll.split(',')
            fa = ''
            index = ''

        return pos, fa, index

    def set_pos(self):
        street = self.entry.text()
        pos, fa, index = self.get_street_info(street)
        self.ll = ','.join(pos)
        self.full_address.setText(fa + ', ' + index)
        self.full_address.adjustSize()
        self.setFocus()
        self.set_image()

    def set_image(self):
        self.get_image()
        self.pixmap = QPixmap('map.png')
        self.image.setPixmap(self.pixmap)

    def init_ui(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.set_image()

    def closeEvent(self, event):
        os.remove(self.map_file)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Example()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
