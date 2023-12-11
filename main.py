import os
import sys
from calc_book import Book

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QHBoxLayout, \
    QFormLayout, QComboBox, QRadioButton, QPushButton, QFileDialog, QMessageBox


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заземление")
        self.resize(800, 500)
        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.widget_1 = Widget_in()
        self.widget_2 = Widget_out()
        self.widget_3 = Widget_buttons()
        self.gridLayout.addWidget(self.widget_1, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_2, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.widget_3, 1, 0, 1, 2)

        self.widget_1.dict_LE['Расположение заземлителя'].activated.connect(self.action_QB)
        self.widget_1.dict_LE['Автоматический расчёт'].clicked.connect(self.action_RB)
        self.widget_3.calc_button.clicked.connect(self.valid)
        self.widget_3.save_button.clicked.connect(self.save_file)

        self.setLayout(self.gridLayout)
        self.last_save = os.getcwd()
        self.count = 0 # счетчик для загрузки параметров
        self.widget_style()

    def action_QB(self):
        self.widget_1.action_QB()
        self.widget_2.action_QB(self.widget_1.dict_LE['Расположение заземлителя'].currentText())

    def action_RB(self):
        self.widget_1.action_RB()

    def closeEvent(self, closeEvent):
        '''При корректном закрытии программы, сохраняются исходные параметры'''
        save_init = self.widget_1.read_text_LE()
        with open("init.ini", 'w') as file:
            for value in save_init:
                file.writelines(f'{value}\n')
            file.writelines(self.last_save)

    def showEvent(self, showEvent):
        '''Загрузка параметров и последнего места сохранения при запуске программы'''
        save_initial = f'{os.getcwd()}/init.ini'
        self.count += 1
        if self.count <= 1:
            if os.path.exists(save_initial):
                with open(save_initial) as file:
                    list_in = [i.replace('\n', '') for i in file.readlines()]
                    self.widget_1.set_text_LE([list_in[i] for i in range(len(list_in))])
            else:
                self.widget_1.set_text_LE([250, 30, 2.5, 10, 0.012, 8, 14, 0.040, 0.8, 1, 6, 'круглый прокат', 'полосовой прокат', 'по контуру', False])
        if len(list_in) == 16:
            self.last_save = list_in[15]
        else:
            self.last_save = os.getcwd()
        self.action_QB()
        self.action_RB()

    def save_file(self):
        last_save, filetype = QFileDialog.getSaveFileName(self, 'Сохранить проект', self.last_save, "Excel Files (*.xls)")
        if last_save != '':
            self.last_save = last_save
            # if self.last_save:
            #     with open(self.last_save, 'w') as file:
            #         file.writelines('d')
        else:
            print('asasd')

    def valid(self):
        list_in = []
        self.list_init_value = self.widget_1.read_text_LE()
        if self.valid_1(self.list_init_value[0:11]):
            for count in range(len(self.list_init_value)):
                if count <= 10:
                    list_in.append(float(self.list_init_value[count].replace(',', '.', 1)))
                elif 13 >= count > 10:
                    list_in.append(self.list_init_value[count].lower())
                else:
                    list_in.append(bool(self.list_init_value[count]))
            flag_result, result = Book(*list_in).calc_zazem()
            if flag_result:
                self.widget_2.setText_LE(result)
                self.widget_3.save_button.setEnabled(True)
            else:
                self.error_func('Превышение ограничений', result)
                self.widget_2.setText_LE(['*' for i in range(12)])
                self.widget_3.save_button.setDisabled(True)

    def valid_1(self, list_in):
        list_in = [i.replace(',', '.', 1) for i in list_in]
        if all([i.replace('.', '', 1).isnumeric() for i in list_in]) and all([float(i) > 0 for i in list_in]):
            return True
        else:
            self.error_func('Ошибка исходных данных', 'Не верный формат исходных данных')
            return False


    def error_func(self, type_error, msg_error):
        QMessageBox().warning(self, type_error, msg_error, QMessageBox.StandardButton.Close)


    def widget_style(self):
        self.setStyleSheet(u"QLabel{\n"
                           "	font: 10pt \"MS Shell Dlg 2\";\n"
                           "	color:black;\n"
                           "    padding-left: 2px\n"
                           "}\n"
                           "QLabel:disabled {\n"
                           "color:rgb(154, 154, 154);\n"
                           "}\n"
                           "QLineEdit {\n"
                           "	font: 10pt \"MS Shell Dlg 2\";\n"
                           "	color:black;\n"
                           "    padding-left: 0px\n"
                           "}\n"
                           "QLabel:disabled {\n"
                           "	color:rgb(154, 154, 154);\n"
                           "}\n"
                           "QComboBox{\n"
                           "background-color: rgb(255, 255, 255);\n"
                           "    padding-left: 5px;\n"
                           "}\n"
                           # "QPushButton {\n"
                           # "    text-align: center;\n"
                           # "    padding-left: 50px;\n"
                           # "    padding-right: 50px;\n"
                           # "}\n"
                           "QPushButton:hover {\n"
                           "	background-color: rgb(5, 177, 210);\n"
                           "}\n"
                           "QPushButton:disabled {\n"
                           "	color:rgb(154, 154, 154);\n"
                           "}\n"
                           "QRadioButton{\n"
                           "    padding-left: 5px\n"
                           "}\n"
                           # "QRadioButton:hover{\n"
                           # "	background-color: rgb(5, 177, 210);\n"
                           "}\n"
                           # "QGroupBox {\n"
                           # "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n""stop:0 rgba(42, 41, 34, 10), stop:1 rgba(42, 41, 34, 75));\n"
                           # # "    background-image: url(wall.jpg);\n"  
                           # 
                           # # "    background-attachment: scroll;\n" 
                           # # "    background-position: center;\n"              
                           # 
                           # "    border: 2px solid gray;\n"
                           # "    border-radius: 5px;\n"
                           # "    border-color: rgb(0, 0, 0);\n"
                           # "    margin-top: 2ex; /* leave space at the top for the title */\n"
                           # "}\n"
                           "QGroupBox::title {\n"
                           "    subcontrol-origin: margin;\n"
                           "	font: 25pt \"MS Shell Dlg 2\";\n"
                           "	color: blue;\n"
                           "    subcontrol-position: top center; /* position at the top center */\n"
                           "    padding: 0px 3px;\n"
                           "}\n")

class Widget_in(QGroupBox):
    list_labels_names = ['Удельное сопротивление верхнего слоя грунта p1, Ом*м',
                         'Удельное сопротивление нижнего слоя грунта p2, Ом*м',
                         'Толщина верхнего слоя грунта h, м',
                         'Длинна вертикального заземлителя l, м',
                         'Размер вертикального заземлителя d*, м',
                         'Длина горизонтального заземлителя (сторона 1) a1, м',
                         'Длина горизонтального заземлителя (сторона 2) a2, м',
                         'Размер горизонтального заземлителя b*',
                         'Глубина укладки горизонтального заземлителя t, м',
                         'Нормируемое сопротивление Rнорм, Ом',
                         'Количество заземлителей при "ручном" расчете m, шт.',
                         'Тип вертикального заземлителя',
                         'Тип горизонтального заземлителя',
                         'Расположение заземлителя',
                         'Автоматический расчёт'
                         ]
    sumbol = '*'
    def __init__(self):
        super().__init__()
        self.setTitle('Исходные данные')
        self.formLayout = QFormLayout()
        self.add_label()
        self.add_LE()
        self.setLayout(self.formLayout)
        self.sumbol = '*'


    def add_label(self):
        '''Создаем и добавляем labels'''
        count = 0
        self.dict_labels = {i: QLabel() for i in self.list_labels_names}
        for k, v in self.dict_labels.items():
            self.formLayout.setWidget(count, 0, self.dict_labels[k])
            self.dict_labels[k].setText(k)
            count += 1

    def add_LE(self):
        count = 0
        self.dict_LE = {i: QLineEdit() for i in self.list_labels_names}
        for k, v in self.dict_LE.items():
            if k != 'Тип вертикального заземлителя' and k != 'Тип горизонтального заземлителя' and k != 'Расположение заземлителя' and k != 'Автоматический расчёт':
                self.formLayout.setWidget(count, 1, self.dict_LE[k])
                self.dict_LE[k].setText(self.sumbol)
                self.dict_LE[k].setMinimumSize(QSize(60, 20))
                self.dict_LE[k].setMaximumSize(QSize(60, 20))
                self.dict_LE[k].setAlignment(Qt.AlignCenter)
                count += 1

        self.dict_LE.update({'Тип вертикального заземлителя': QComboBox()})
        self.dict_LE.update({'Тип горизонтального заземлителя': QComboBox()})
        self.dict_LE.update({'Расположение заземлителя': QComboBox()})
        self.dict_LE.update({'Автоматический расчёт': QRadioButton()})
        self.dict_LE['Тип вертикального заземлителя'].addItems(['Круглый прокат', 'Уголок стальной', 'Полосовой прокат'])
        self.dict_LE['Тип горизонтального заземлителя'].addItems(['Круглый прокат', 'Уголок стальной', 'Полосовой прокат'])
        self.dict_LE['Расположение заземлителя'].addItems(['По контуру', 'В ряд'])
        self.formLayout.setWidget(11, 1, self.dict_LE['Тип вертикального заземлителя'])
        self.formLayout.setWidget(12, 1, self.dict_LE['Тип горизонтального заземлителя'])
        self.formLayout.setWidget(13, 1, self.dict_LE['Расположение заземлителя'])
        self.formLayout.setWidget(14, 1, self.dict_LE['Автоматический расчёт'])

    def set_text_LE(self, list_in):
        count = 0
        for k, v in self.dict_LE.items():
            if k != 'Тип вертикального заземлителя' and k != 'Тип горизонтального заземлителя' and k != 'Расположение заземлителя' and k != 'Автоматический расчёт':
                self.dict_LE[k].setText(str(list_in[count]))
                count += 1
        self.dict_LE['Тип вертикального заземлителя'].setCurrentText(list_in[11])
        self.dict_LE['Тип горизонтального заземлителя'].setCurrentText(list_in[12])
        self.dict_LE['Расположение заземлителя'].setCurrentText(list_in[13])
        self.dict_LE['Автоматический расчёт'].setChecked(int(list_in[14]))

    def read_text_LE(self):
        '''Чтение параметров'''
        count = 0
        list1 = []
        for k, v in self.dict_LE.items():
            if k != 'Тип вертикального заземлителя' and k != 'Тип горизонтального заземлителя' and k != 'Расположение заземлителя' and k != 'Автоматический расчёт':
                list1.append(self.dict_LE[k].text())
                count += 1
        list1.append(self.dict_LE['Тип вертикального заземлителя'].currentText())
        list1.append(self.dict_LE['Тип горизонтального заземлителя'].currentText())
        list1.append(self.dict_LE['Расположение заземлителя'].currentText())
        list1.append(int(self.dict_LE['Автоматический расчёт'].isChecked()))
        return list1

    def action_QB(self):
        if self.dict_LE['Расположение заземлителя'].currentText() == 'По контуру':
            self.dict_labels['Длина горизонтального заземлителя (сторона 1) a1, м'].setText('Длина горизонтального заземлителя (сторона 1) a1, м')
            self.dict_labels['Длина горизонтального заземлителя (сторона 2) a2, м'].setEnabled(True)
            self.dict_LE['Длина горизонтального заземлителя (сторона 2) a2, м'].setEnabled(True)
        elif self.dict_LE['Расположение заземлителя'].currentText() == 'В ряд':
            self.dict_labels['Длина горизонтального заземлителя (сторона 1) a1, м'].setText('Длина горизонтального заземлителя, м')
            self.dict_labels['Длина горизонтального заземлителя (сторона 2) a2, м'].setDisabled(True)
            self.dict_LE['Длина горизонтального заземлителя (сторона 2) a2, м'].setDisabled(True)

    def action_RB(self):
        if self.dict_LE['Автоматический расчёт'].isChecked():
            self.dict_labels['Количество заземлителей при "ручном" расчете m, шт.'].setDisabled(True)
            self.dict_LE['Количество заземлителей при "ручном" расчете m, шт.'].setDisabled(True)
        else:
            self.dict_labels['Количество заземлителей при "ручном" расчете m, шт.'].setEnabled(True)
            self.dict_LE['Количество заземлителей при "ручном" расчете m, шт.'].setEnabled(True)


class Widget_out(QGroupBox):
    list_labels_names = ['Эквив. удельное сопротивление грунта для вертик. зазем., Ом*м',
                         'Сопротивление одиночного вертикального заземлителя, Ом',
                         'Коэффициент использования заземлителя',
                         'Эквив. удельное сопр. грунта, гор. зазем. сторона 1, Ом*м',
                         'Сопротивление горизонтального заземлителя сторона 1, Ом',
                         'Эквив. удельное сопр. грунта, гор. зазем. сторона 2, Ом*м',
                         'Сопротивление горизонтального заземлителя сторона 2, Ом',
                         'Количество вертикальных заземлителей, шт.',
                         'Сопротивление заземлителя, Ом',
                         'Среднее расстояние между вертикальными заземлителями, м',
                         'Общая длинна горизонтального заземлителя, м']
    sumbol = '*'

    def __init__(self):
        super().__init__()
        self.setTitle('Расчетные данные')
        self.formLayout = QFormLayout()
        self.add_labels()
        self.add_LE()
        self.setLayout(self.formLayout)


    def add_labels(self):
        count = 0
        self.dict_labels = {i: QLabel() for i in self.list_labels_names}
        for k, v in self.dict_labels.items():
            self.formLayout.setWidget(count, 0, self.dict_labels[k])
            self.dict_labels[k].setText(k)
            count += 1

    def add_LE(self):
        count = 0
        self.dict_LE = {i: QLineEdit() for i in self.list_labels_names}
        for k, v in self.dict_LE.items():
            self.formLayout.setWidget(count, 1, self.dict_LE[k])
            self.dict_LE[k].setText(self.sumbol)
            self.dict_LE[k].setReadOnly(True)
            self.dict_LE[k].setMinimumSize(QSize(60, 20))
            self.dict_LE[k].setMaximumSize(QSize(60, 20))
            self.dict_LE[k].setAlignment(Qt.AlignCenter)
            count += 1

    def setText_LE(self, list_out):
        count = 0
        for k, v in self.dict_LE.items():
            self.formLayout.setWidget(count, 1, self.dict_LE[k])
            self.dict_LE[k].setText(f'{list_out[count]}')
            count += 1

    def action_QB(self, flag_QB):
        if flag_QB == 'По контуру':
            self.dict_labels['Эквив. удельное сопр. грунта, гор. зазем. сторона 2, Ом*м'].setEnabled(True)
            self.dict_labels['Сопротивление горизонтального заземлителя сторона 2, Ом'].setEnabled(True)
            self.dict_LE['Эквив. удельное сопр. грунта, гор. зазем. сторона 2, Ом*м'].setEnabled(True)
            self.dict_LE['Сопротивление горизонтального заземлителя сторона 2, Ом'].setEnabled(True)
        else:
            self.dict_labels['Эквив. удельное сопр. грунта, гор. зазем. сторона 2, Ом*м'].setDisabled(True)
            self.dict_labels['Сопротивление горизонтального заземлителя сторона 2, Ом'].setDisabled(True)
            self.dict_LE['Эквив. удельное сопр. грунта, гор. зазем. сторона 2, Ом*м'].setDisabled(True)
            self.dict_LE['Сопротивление горизонтального заземлителя сторона 2, Ом'].setDisabled(True)

class Widget_buttons(QWidget):
    def __init__(self):
        super().__init__()
        self.calc_button = QPushButton()
        self.calc_button.setText('Выполнить расчет')
        self.save_button = QPushButton()
        self.save_button.setText('Сохранить')
        self.save_button.setDisabled(True)
        self.save_help = QPushButton()
        self.save_help.setText('Справка')
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.calc_button)
        self.verticalLayout.addWidget(self.save_button)
        self.verticalLayout.addWidget(self.save_help)
        self.setLayout(self.verticalLayout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    exemplar = MainWidget()
    exemplar.show()
    sys.exit(app.exec_())
