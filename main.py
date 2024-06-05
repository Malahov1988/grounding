import csv
import os
import sys
from calc_book import Book

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QHBoxLayout, \
    QFormLayout, QComboBox, QRadioButton, QPushButton, QFileDialog, QMessageBox


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расчет заземления. Метод коэффициентов использования.")
        self.resize(1300, 500)
        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.widget_1 = Widget_in()
        self.widget_2 = Widget_out()
        self.widget_buttons = Widget_buttons()
        self.gridLayout.addWidget(self.widget_1, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_2, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.widget_buttons, 1, 0, 1, 2)

        self.widget_1.dict_CB['Расположение заземлителя'].activated.connect(self.widget_1.action_QB_rasp)
        self.widget_1.dict_CB['Расположение заземлителя'].activated.connect(self.ation_climat_CB)
        self.widget_1.dict_CB['Климатическая зона'].activated.connect(self.ation_climat_CB)

        self.widget_buttons.calc_button.clicked.connect(self.valid)
        self.widget_buttons.save_button.clicked.connect(self.save_file)

        self.setLayout(self.gridLayout)
        self.last_save = os.getcwd()
        self.load_flag_climat = False
        self.count = 0 # счетчик для загрузки параметров
        self.widget_style()

    def ation_climat_CB(self):
        lst = [self.widget_1.dict_LE['Длинна вертикального заземлителя l, м'].text(), self.widget_1.dict_LE['Длина горизонтального заземлителя (сторона 1) a1, м'].text(), self.widget_1.dict_LE['Длина горизонтального заземлителя (сторона 2) a2, м'].text()]
        if self.valid_1(lst):

            l_vert, l_dor1, l_dor2 = [float(i.replace(',', '.', 1)) for i in lst]
        else:
            l_vert, l_dor1, l_dor2 = [-1 for i in lst]
        if self.widget_1.dict_CB['Расположение заземлителя'].currentText() == 'По контуру':
            l_gor = (l_dor1+l_dor2) * 2
        else:
            l_gor = l_dor1

        self.widget_1.action_QB_climat(l_vert, l_gor) if self.load_flag_climat else ''
        self.load_flag_climat = True
        self.widget_2.setText_help_climat(self.widget_1.dict_CB['Климатическая зона'].currentText())

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
                    self.widget_1.set_param([list_in[i] for i in range(len(list_in))])
                    self.last_save = list_in[-1]

            else:
                self.widget_1.set_param([250, 30, 2.5, 10, 0.012, 8, 14, 0.040, 0.8, 2, 1.2, 2.5, 'круглый прокат', 'полосовой прокат', 'по контуру', '1'])

        self.widget_1.action_QB_rasp()
        self.ation_climat_CB()

    def save_file(self):
        list_labels_names = ['Удельное сопротивление верхнего слоя грунта p1, Ом*м',
                             'Удельное сопротивление нижнего слоя грунта p2, Ом*м',
                             'Толщина верхнего слоя грунта h, м',
                             'Длинна вертикального заземлителя l, м',
                             'Размер вертикального заземлителя d*, м',
                             'Длина горизонтального заземлителя (сторона 1) a1, м',
                             'Длина горизонтального заземлителя (сторона 2) a2, м',
                             'Размер горизонтального заземлителя b',
                             'Глубина укладки горизонтального заземлителя t, м',
                             'Количество заземлителей при "ручном" расчете m, шт.',
                             'Сезонный климатический коэф. верт. заземлитель',
                             'Сезонный климатический коэф. гор. заземлитель',
                             'Тип вертикального заземлителя',
                             'Тип горизонтального заземлителя',
                             'Расположение заземлителя',
                             'Климатическая зона',
                             ]
        result_list = ['Эквив. удельное сопротивление грунта для вертик. зазем., Ом*м',
                       'Сопротивление одиночного вертикального заземлителя, Ом',
                       'Проводимость одиночного вертикального заземлителя, См',
                       'Коэффициент использования заземлителя',
                       'Эквив. удельное сопр. грунта, гор. зазем. сторона 1, Ом*м',
                             'Сопротивление горизонтального заземлителя сторона 1, Ом',
                       'Проводимость горизонтального заземлителя сторона 1, См',
                             'Эквив. удельное сопр. грунта, гор. зазем. сторона 2, Ом*м',
                             'Сопротивление горизонтального заземлителя сторона 2, Ом',
                       'Проводимость горизонтального заземлителя сторона 2, См',
                             'Количество вертикальных заземлителей, шт.',
                             'Сопротивление заземлителя, Ом',
                             'Среднее расстояние между вертикальными заземлителями, м',
                             'Общая длинна горизонтального заземлителя, м']
        last_save, filetype = QFileDialog.getSaveFileName(self, 'Сохранить проект', self.last_save, "*.csv;;*.xls")
        if last_save != '':
            self.last_save = last_save
            dict_save = dict(zip(list_labels_names, self.list_init_value))
            dict_2 = dict(zip(result_list, self.result))
            dict_save.update(dict_2)
            with open(last_save, 'w') as file:
                if filetype == '*.csv':
                    file_writer = csv.writer(file, delimiter=";", lineterminator="\r", quoting=csv.QUOTE_ALL)
                    for k, v in dict_save.items():
                        file_writer.writerow([k, v])
                else:
                    self.error_func('Ошибка сохранения', 'Не реализовано')

    def valid(self):
        list_in = []
        self.list_init_value = self.widget_1.read_text_LE()
        if self.valid_1(self.list_init_value[0:12]):
            for count in range(len(self.list_init_value)):
                if count <= 11:
                    list_in.append(float(self.list_init_value[count].replace(',', '.', 1)))
                else:
                    list_in.append(self.list_init_value[count].lower())
            flag_result, self.result = Book(*list_in).calc_zazem()
            if flag_result:
                self.widget_2.setText_LE(self.result)
                self.widget_buttons.save_button.setEnabled(True)
            else:
                self.error_func('Превышение ограничений', self.result)
                self.widget_2.setText_LE(['*' for i in range(14)])
                self.widget_buttons.save_button.setDisabled(True)

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
        self.setStyleSheet(
            "QWidget"
            "{"
            "background-color:rgb(115, 115, 115);\n"
            "color: rgb(240, 240, 240);\n"
            "font: 12pt 'DIALux Report Font Light';\n"
            "border-radius: 5px;\n"
            "}"
            "QPushButton"
            "{"
            "background-color: black;\n"
            "border: 1px solid black;\n"
            "}"
            "QPushButton:hover"
            "{"
            "color: rgb(253, 153, 0);\n"
            "border: 1px solid rgb(253, 153, 0);\n"
            "font: 15pt 'Arial Narrow';\n"
            "}"
            "QPushButton:disabled {\n"
            "color: rgb(115, 115, 115);\n"
            "border: 1px solid rgb(115, 115, 115);\n"
            "}\n"
        )

class Widget_in(QGroupBox):
    labels_names = [     'Удельное сопротивление верхнего слоя грунта p1, Ом*м',
                         'Удельное сопротивление нижнего слоя грунта p2, Ом*м',
                         'Толщина верхнего слоя грунта h, м',
                         'Длинна вертикального заземлителя l, м',
                         'Размер вертикального заземлителя d, м',
                         'Длина горизонтального заземлителя (сторона 1) a1, м',
                         'Длина горизонтального заземлителя (сторона 2) a2, м',
                         'Размер горизонтального заземлителя b*',
                         'Глубина укладки горизонтального заземлителя t, м',
                         'Количество заземлителей при "ручном" расчете m, шт.',
                         'Сезонный климатический коэф. верт. заземлитель',
                         'Сезонный климатический коэф. гор. заземлитель',
                         'Тип вертикального заземлителя',
                         'Тип горизонтального заземлителя',
                         'Расположение заземлителя',
                         'Климатическая зона',
                    ]
    lineedit_names = labels_names[0:12]
    combox_name = ['Тип вертикального заземлителя', 'Тип горизонтального заземлителя', 'Расположение заземлителя', 'Климатическая зона']
    sumbol = '*'
    def __init__(self):
        super().__init__()
        self.setTitle('Исходные данные')
        self.formLayout = QFormLayout()
        self.add_label()
        self.add_LE()
        self.setLayout(self.formLayout)
        self.setFixedWidth(650)
        self.widget_style()

    def add_label(self):
        '''Создаем и добавляем labels'''
        count = 0
        self.dict_labels = {i: QLabel() for i in self.labels_names}
        for k, v in self.dict_labels.items():
            self.formLayout.setWidget(count, 0, self.dict_labels[k])
            self.dict_labels[k].setText(k)
            count += 1

    def add_LE(self):
        count = 0
        self.dict_LE = {i: QLineEdit() for i in self.lineedit_names}
        self.dict_CB = {i: QComboBox() for i in self.combox_name}
        for k, v in self.dict_LE.items():
            self.formLayout.setWidget(count, 1, self.dict_LE[k])
            self.dict_LE[k].setText(self.sumbol)
            self.dict_LE[k].setAlignment(Qt.AlignCenter)
            count += 1
        for k, v in self.dict_CB.items():
            self.formLayout.setWidget(count, 1, self.dict_CB[k])
            count += 1
        self.dict_CB['Тип вертикального заземлителя'].addItems(['Круглый прокат', 'Уголок стальной', 'Полосовой прокат'])
        self.dict_CB['Тип горизонтального заземлителя'].addItems(['Круглый прокат', 'Уголок стальной', 'Полосовой прокат'])
        self.dict_CB['Расположение заземлителя'].addItems(['По контуру', 'В ряд'])
        self.dict_CB['Климатическая зона'].addItems(['Зона 1', 'Зона 2', 'Зона 3', 'Зона 4'])

    def set_param(self, list_in):
        count = 0
        for k, v in self.dict_LE.items():
            self.dict_LE[k].setText(str(list_in[count]))
            count += 1
        for k, v in self.dict_CB.items():
            self.dict_CB[k].setCurrentText((list_in[count]))
            count += 1

    def read_text_LE(self):
        '''Чтение параметров'''
        lst_out = []
        for k, v in self.dict_LE.items():
            lst_out.append(self.dict_LE[k].text())
        for k, v in self.dict_CB.items():
            lst_out.append(self.dict_CB[k].currentText())
        return lst_out

    def action_QB_rasp(self):
        if self.dict_CB['Расположение заземлителя'].currentText() == 'По контуру':
            self.dict_labels['Длина горизонтального заземлителя (сторона 1) a1, м'].setText('Длина горизонтального заземлителя (сторона 1) a1, м')
            self.dict_labels['Длина горизонтального заземлителя (сторона 2) a2, м'].setEnabled(True)
            self.dict_LE['Длина горизонтального заземлителя (сторона 2) a2, м'].setEnabled(True)
        else:
            self.dict_labels['Длина горизонтального заземлителя (сторона 1) a1, м'].setText('Длина горизонтального заземлителя, м')
            self.dict_labels['Длина горизонтального заземлителя (сторона 2) a2, м'].setDisabled(True)
            self.dict_LE['Длина горизонтального заземлителя (сторона 2) a2, м'].setDisabled(True)

    def action_QB_climat(self, l_vert, l_gor):
        ration_vetr_clam, ration_gor_clam = 1, 1
        dict_l_vert_climat_wet = {3: ['1.9', '1.7', '1.5', '1.3'], 5: ['1.5', '1.4', '1.3', '1.2']}
        dict_l_gor_climat_wet = {10: ['9.3', '5.9', '4.2', '2.5'], 50: ['7.2', '4.8', '3.2', '2.2']}
        dict_l_vert_climat_normal = {3: ['1.7', '1.5', '1.3', '1.1'], 5: ['1.4', '1.3', '1.2', '1.1']}
        dict_l_gor_climat_normal = {10: ['5.5', '3.5', '2.5', '1.5'], 50: ['4.5', '3.0', '2.0', '1.4']}
        dict_l_vert_climat_dry = {3: ['1.5', '1.3', '1.2', '1.0'], 5: ['1.3', '1.2', '1.1', '1.0']}
        dict_l_gor_climat_dry = {10: ['4.1', '2.6', '2.0', '1.1'], 50: ['3.6', '2.4', '1.6', '1.12']}
        cc = {'Зона 1': 0, 'Зона 2': 1, 'Зона 3': 2, 'Зона 4': 3}
        zona = self.dict_CB['Климатическая зона'].currentText()
        for i in dict_l_vert_climat_normal.keys():
            if l_vert <= i:
                ration_vetr_clam = dict_l_vert_climat_normal[i][cc[zona]]
                break
            elif l_vert > i:
                ration_vetr_clam = dict_l_vert_climat_normal[i][cc[zona]]
        for i in dict_l_gor_climat_normal.keys():
            if l_gor <= i:
                ration_gor_clam = dict_l_gor_climat_normal[i][cc[zona]]
                break
            elif l_gor > i:
                ration_gor_clam = dict_l_gor_climat_normal[i][cc[zona]]
        self.dict_LE['Сезонный климатический коэф. верт. заземлитель'].setText(f'{ration_vetr_clam}')
        self.dict_LE['Сезонный климатический коэф. гор. заземлитель'].setText(f'{ration_gor_clam}')

    def widget_style(self):
        self.setStyleSheet(
            "QGroupBox {\n"
            "border: 1px solid rgb(253, 153, 0);\n"
            "margin-top: 0.5em;\n"
            "background-color: rgb(43, 43, 43);\n"
            "font: 12pt 'Arial Narrow';\n"
            "}\n"
            "QGroupBox:title {\n"
            "background-color: rgba(43, 43, 43, 1);\n"
            "border-radius: 2px;\n"
            "padding: 0px 5px 0px 5px;\n"
            "top: -8px;\n"
            "left: 10px;\n"
            "}\n"
            "QLabel{\n"
            "background-color:rgb(43, 43, 43);}\n"
            "QLabel:disabled {\n"
            "color: rgb(115, 115, 115);\n"
            "}\n"
            "QLineEdit {\n"
            "border: 1px solid rgb(253, 153, 0);\n"
            "background-color:rgb(43, 43, 43);\n"
            # "font: 10pt 'Algerian';\n"
            "selection-background-color: rgb(253, 153, 0);\n"
            "}\n"
            "QLineEdit:disabled {\n"
            "color: rgb(115, 115, 115);\n"
            "border: 1px solid rgb(115, 115, 115);\n"
            "}\n"
            "QLineEdit:hover {\n"
            "background-color:rgb(115, 115, 115);\n"
            "color: rgb(253, 153, 0);\n"
            "}\n"
            
            "QComboBox {\n"
            "border: 1px solid rgb(253, 153, 0);\n"
            "background-color: rgb(43, 43, 43);\n"
            "}\n"
            # 
            "QComboBox:hover {\n"
            "background-color:rgb(115, 115, 115);\n"
            "color: rgb(253, 153, 0);\n"
            "}\n"
            
             "QComboBox:drop-down {\n"
             # "subcontrol-origin: padding;\n"
             # "subcontrol-position: top right;\n"
             # "width: 15px;\n"
             # "border-left-width: 1px;\n"
             "border-left-color: darkgray;\n"
             # "border-left-style: solid;\n"
             # "border-top-right-radius: 2px;\n"
             # "border-bottom-right-radius:10px\n"
             "}\n"
            
             "QComboBox::down-arrow {\n"
             "image: url(arrow.png);\n"
             "}\n"
            #
            "QComboBox QAbstractItemView  {\n"
            "background-color: rgb(43, 43, 43);\n"
            "selection-background-color: rgb(115, 115, 115);\n"
            "selection-color:  rgb(253, 153, 0);\n"
            "border: 1px solid rgb(253, 153, 0);\n"
            "}\n"
            #
            #
            #
            "QRadioButton {\n"
            "background-color: rgb(43, 43, 43);\n"
            "}\n"

            # "QRadioButton:hover {\n"
            # "background-color: rgb(115, 115, 115);\n"
            # 
            # "}\n"

            "QRadioButton:indicator:checked {\n"
            "color: rgb(43, 43, 43);\n"

            "}\n"



        )

class Widget_out(QGroupBox):
    list_labels_names = ['Эквив. удельное сопротивление грунта для вертик. зазем., Ом*м',
                         'Сопротивление одиночного вертикального заземлителя, Ом',
                         'Проводимость одиночного вертикального заземлителя, См',
                         'Коэффициент использования заземлителя',
                         'Эквив. удельное сопр. грунта, гор. зазем. сторона 1, Ом*м',
                         'Сопротивление горизонтального заземлителя сторона 1, Ом',
                         'Проводимость горизонтального заземлителя сторона 1, См',
                         'Эквив. удельное сопр. грунта, гор. зазем. сторона 2, Ом*м',
                         'Сопротивление горизонтального заземлителя сторона 2, Ом',
                         'Проводимость горизонтального заземлителя сторона 2, См',
                         'Количество вертикальных заземлителей, шт.',
                         'Сопротивление заземлителя, Ом',
                         'Среднее расстояние между вертикальными заземлителями, м',
                         'Общая длинна горизонтального заземлителя, м'
                         ]
    sumbol = '*'

    def __init__(self):
        super().__init__()
        self.setTitle('Расчетные данные')
        self.formLayout = QFormLayout()
        self.add_labels()
        self.add_LE()
        self.setLayout(self.formLayout)
        self.setFixedWidth(650)
        self.widget_style()

    def add_labels(self):
        count = 0
        self.dict_labels = {i: QLabel() for i in self.list_labels_names}
        self.dict_labels.update({'Cправка по климату': QLabel()})
        for k, v in self.dict_labels.items():
            self.formLayout.setWidget(count, 0, self.dict_labels[k])
            self.dict_labels[k].setText(k)
            count += 1

    def setText_help_climat(self, text):
        dict_climat = {
                'Зона 1': '''Средняя многолетняя низшая температура (январь), °С: от -20 до -15.\nСредняя многолетняя высшая температура (июль), °С: от +16 до +18.\nСреднегодовое количество осадков, см: ~40.\nПродолжительность замерзания вод, дни: 190..170''',
                'Зона 2': '''Средняя многолетняя низшая температура (январь), °С: от -14 до -10.\nСредняя многолетняя высшая температура (июль), °С: от +18 до +22.\nСреднегодовое количество осадков, см: ~50.\nПродолжительность замерзания вод, дни: ~150`''',
                'Зона 3': '''Средняя многолетняя низшая температура (январь), °С: от -10 до 0.\nСредняя многолетняя высшая температура (июль), °С: от +22 до +24.\nСреднегодовое количество осадков, см: ~40.\nПродолжительность замерзания вод, дни: ~100`''',
                'Зона 4': '''Средняя многолетняя низшая температура (январь), °С: от 0 до +5.\nСредняя многолетняя высшая температура (июль), °С: от +24 до +21.\nСреднегодовое количество осадков, см: ~30..50.\nПродолжительность замерзания вод, дни: 0''',}
        self.dict_labels['Cправка по климату'].setWordWrap(True)
        self.dict_labels['Cправка по климату'].setFixedWidth(650)
        self.dict_labels['Cправка по климату'].setText(dict_climat[text])

    def add_LE(self):
        count = 0
        self.dict_LE = {i: QLineEdit() for i in self.list_labels_names}
        for k, v in self.dict_LE.items():
            self.formLayout.setWidget(count, 1, self.dict_LE[k])
            self.dict_LE[k].setText(self.sumbol)
            self.dict_LE[k].setReadOnly(True)

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

    def widget_style(self):
        self.setStyleSheet(
            "QGroupBox {\n"
            "border: 1px solid rgb(253, 153, 0);\n"
            "margin-top: 0.5em;\n"
            "background-color: rgb(43, 43, 43);\n"
            "font: 10pt 'Arial';\n"
            "}\n"
            "QGroupBox:title {\n"
            "background-color: rgba(43, 43, 43, 1);\n"
            "border-radius: 2px;\n"
            "padding: 0px 5px 0px 5px;\n"
            "top: -8px;\n"
            "left: 10px;\n"
            "}\n"
            "QLabel{\n"
            "background-color:rgb(43, 43, 43);}\n"
            "QLabel:disabled {\n"
            "color: rgb(115, 115, 115);\n"
            "}\n"
            "QLineEdit {\n"
            "border: 1px solid rgb(253, 153, 0);\n"
            "background-color:rgb(43, 43, 43);\n"
            "selection-background-color: rgb(253, 153, 0);\n"
            "}\n"
            "QLineEdit:disabled {\n"
            "color: rgb(115, 115, 115);\n"
            "border: 1px solid rgb(115, 115, 115);\n"
            "}\n"
            "QLineEdit:hover{\n"
            "background-color:rgb(115, 115, 115);\n"
            "color: rgb(253, 153, 0);\n"
            "}\n"

        )

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
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.addWidget(self.calc_button)
        self.verticalLayout.addWidget(self.save_button)
        self.verticalLayout.addWidget(self.save_help)
        self.setLayout(self.verticalLayout)
        # self.widget_style()

    def widget_style(self):
        self.setStyleSheet(
            "QPushButton"
            "{"
            "background-color: black;\n"
            "border: 1px solid black;\n"
            "}"
            "QPushButton:hover"
            "{"
            "color: rgb(253, 153, 0);\n"
            "border: 1px solid rgb(253, 153, 0);\n"
            "font: 15pt 'Arial Narrow';\n"
            "}"
            "QPushButton:disabled {\n"
            "color: rgb(115, 115, 115);\n"
            "border: 1px solid rgb(115, 115, 115);\n"
            "}\n"
        )



if __name__ == '__main__':
    app = QApplication(sys.argv)
    exemplar = MainWidget()
    exemplar.show()
    sys.exit(app.exec_())
