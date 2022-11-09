from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from PyQt6 import uic
#from controller import Controller
from main import Controller


class View(QMainWindow):

    #Klassenvariablen

    #dspB_amount: QDoubleSpinBox
    #coB_from: QComboBox

    base_layout: QVBoxLayout
    top_layout: QHBoxLayout
    bot_layout: QHBoxLayout
    base_widget: QWidget
    top_widget: QWidget
    bot_widget: QWidget

    betrag_label: QLabel
    waehrung_label: QLabel
    zielwaehrung_label: QLabel
    livedaten_label: QLabel

    betrag_spinbox: QDoubleSpinBox
    waehrung_combobox: QComboBox
    zielwaehrung_listwidget: QListWidget
    livedaten_checkbox: QCheckBox

    umrechnen_pushbutton: QPushButton
    exit_pushbutton: QPushButton
    reset_pushbutton: QPushButton

    output_textedit: QTextEdit

    controller: Controller

    def __init__(self, c: Controller):
        super().__init__()

        self.controller = c

        self.base_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.bot_layout = QHBoxLayout()

        self.base_widget = QWidget()
        self.top_widget = QWidget()
        self.bot_widget = QWidget()

        self.betrag_label = QLabel('Betrag:')
        self.waehrung_label = QLabel('Währung:')
        self.zielwaehrung_label = QLabel('Zielwährungen:')
        self.livedaten_label = QLabel('Live-Daten')

        self.betrag_spinbox = QDoubleSpinBox()
        self.waehrung_combobox = QComboBox()
        self.zielwaehrung_listwidget = QListWidget()
        self.livedaten_checkbox = QCheckBox()

        self.umrechnen_pushbutton = QPushButton('Umrechnen')
        self.exit_pushbutton = QPushButton('Exit')
        self.reset_pushbutton = QPushButton('Zurücksetzen')

        self.umrechnen_pushbutton.clicked.connect(self.convert)
        self.exit_pushbutton.clicked.connect(self.exit)
        self.reset_pushbutton.clicked.connect(self.reset)

        self.output_textedit = QTextEdit()

        self.zielwaehrung_listwidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.output_textedit.setDisabled(True)
        #self.output_textedit.setText('Hallo')

        currencies = list(self.controller.get_currencies())
        self.waehrung_combobox.addItems(currencies)
        self.zielwaehrung_listwidget.addItems(currencies)

        self.base_widget.setLayout(self.base_layout)
        self.top_widget.setLayout(self.top_layout)
        self.bot_widget.setLayout(self.bot_layout)

        self.base_layout.addWidget(self.top_widget)
        self.base_layout.addWidget(self.zielwaehrung_listwidget)
        self.base_layout.addWidget(self.output_textedit)
        self.base_layout.addWidget(self.bot_widget)

        self.top_layout.addWidget(self.betrag_label)
        self.top_layout.addWidget(self.betrag_spinbox)
        self.top_layout.addWidget(self.waehrung_label)
        self.top_layout.addWidget(self.waehrung_combobox)
        self.top_layout.addWidget(self.livedaten_checkbox)
        self.top_layout.addWidget(self.livedaten_label)

        self.bot_layout.addWidget(self.exit_pushbutton)
        self.bot_layout.addWidget(self.umrechnen_pushbutton)
        self.bot_layout.addWidget(self.reset_pushbutton)

        self.setCentralWidget(self.base_widget)
    
    def exit(self):
        self.close()
    
    def reset(self):
        self.betrag_spinbox.setValue(0)
        self.waehrung_combobox.setCurrentIndex(0)
        self.zielwaehrung_listwidget.clearSelection()
        self.zielwaehrung_listwidget.scrollToTop()
        self.output_textedit.clear()

    def convert(self):
        to = str()
        for x in self.zielwaehrung_listwidget.selectedItems():
            to += x.text() + ','
        to = to[:-1]
        result = self.controller.convert(self.betrag_spinbox.value(), self.waehrung_combobox.currentText(), to)
        self.output_textedit.setText(self.dict_to_text(result))
    
    def dict_to_text(self, input: dict) -> str:
        if type(input) != dict:
            return 'input was not a dictionary'
        output = str()
        output += str(input['betrag']) + ' ' + input['src'] + ' entsprechen' + '\n'
        for key in input['converted']:
            output += '\t' + str(input['converted'][key]['betrag_neu']) + ' ' + key + '(Kurs: ' + str(input['converted'][key]['kurs']) + ')' + '\n'
        output += 'Stand: ' + str(input['date'])
        return output