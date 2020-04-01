from Stages_constructor import Amplifier
import Component_manager
from Transistor_manager import TransistorManager
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout, QPushButton, QGroupBox, QWidget, QDialog, QPlainTextEdit
from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QMessageBox
from PyQt5.QtGui import QIcon, QFont
import sys


class Parameters(QDialog):
    def __init__(self):
        super().__init__()
        self.top = 400
        self.left = 300
        self.height = 200
        self.width = 200
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon("Transistor.png"))
        self.setWindowTitle("Constructor de Amplificadores")
        self.parameters = {}
        self.InitWindow()

    def InitWindow(self):
        RS_Panel = QGroupBox("Introduzca RS")
        RL_Panel = QGroupBox("Introduzca RL")
        AV_Panel = QGroupBox("Introduzca AV")
        self.RL_CC_Panel = QGroupBox("Introduzca RL de etapa de corriente")
        F_Panel = QGroupBox("Introduzca F")

        hbox_RS = QHBoxLayout()
        hbox_RL = QHBoxLayout()
        hbox_AV = QHBoxLayout()
        hbox_F = QHBoxLayout()
        hbox_RL_CC = QHBoxLayout()

        self.MainParametersInput = QVBoxLayout()

        self.RS_label = QLabel("RS")
        self.RS_textedit = QLineEdit()
        hbox_RS.addWidget(self.RS_label)
        hbox_RS.addWidget(self.RS_textedit)
        RS_Panel.setLayout(hbox_RS)

        self.RL_CC_label = QLabel("RL CC")
        self.RL_CC_textedit = QLineEdit()
        hbox_RL_CC.addWidget(self.RL_CC_label)
        hbox_RL_CC.addWidget(self.RL_CC_textedit)
        self.RL_CC_Panel.setLayout(hbox_RL_CC)

        self.RL_label = QLabel("RL")
        self.RL_textedit = QLineEdit()
        hbox_RL.addWidget(self.RL_label)
        hbox_RL.addWidget(self.RL_textedit)
        RL_Panel.setLayout(hbox_RL)

        self.AV_label = QLabel("AV")
        self.AV_textedit = QLineEdit()
        hbox_AV.addWidget(self.AV_label)
        hbox_AV.addWidget(self.AV_textedit)
        AV_Panel.setLayout(hbox_AV)

        self.F_label = QLabel("F")
        self.F_textedit = QLineEdit()
        hbox_F.addWidget(self.F_label)
        hbox_F.addWidget(self.F_textedit)
        F_Panel.setLayout(hbox_F)

        self.btn_Introducir_Datos = QPushButton("Aceptar")
        self.btn_Introducir_Datos.clicked.connect(self.btn_accept)

        self.MainParametersInput.addWidget(RS_Panel)
        self.MainParametersInput.addWidget(RL_Panel)
        self.MainParametersInput.addWidget(AV_Panel)
        self.MainParametersInput.addWidget(F_Panel)
    def CC(self, Condition):
        self.CC_condition = Condition
        if self.CC_condition:
            self.MainParametersInput.addWidget(self.RL_CC_Panel)
        self.MainParametersInput.addWidget(self.btn_Introducir_Datos)
        self.setLayout(self.MainParametersInput)


    def btn_accept(self):
        if self.RS_textedit.text() != '' and self.test_syntax(self.RS_textedit.text()):
            if self.RL_textedit.text() != '' and self.test_syntax(self.RL_textedit.text()):
                if self.AV_textedit.text() != '' and self.test_syntax(self.AV_textedit.text()):
                    if self.F_textedit.text() != '' and self.test_syntax(self.F_textedit.text()):
                        self.parameters['RS'] = self.to_float(self.RS_textedit.text())
                        self.parameters['RL'] = self.to_float(self.RL_textedit.text())
                        self.parameters['AV'] = self.to_float(self.AV_textedit.text())
                        self.parameters['F'] = self.to_float(self.F_textedit.text())
                        if self.CC_condition:
                            if self.RL_CC_textedit.text() != '' and self.test_syntax(self.RL_CC_textedit.text()):
                                self.parameters['RL_CC'] = self.to_float(self.RL_CC_textedit.text())
                                self.close()
                            else:
                                QMessageBox.about(self, "Error RL_CC", "Valor RL_CC invalido o no ingresado")
                        else:
                            self.close()
                    else:
                        QMessageBox.about(self, "Error F ", "Valor F invalido o no ingresado")
                else:
                    QMessageBox.about(self, "Error AV", "Valor AV invalido o no ingresado")
            else:
                QMessageBox.about(self, "Error RL", "Valor RL invalido o no ingresado")
        else:
            QMessageBox.about(self, "Error RS", "Valor RS invalido o no ingresado")

    def test_syntax(self, value):
        dot = 0
        mul = 0
        for index in range(len(value)):
            if value[index].lower() in "0123456789.km":
                if value[index] == '.':
                    dot += 1
                elif value[index].lower() in 'km':
                    mul += 1
                if mul > 1 or dot > 1:
                    return False
            else:
                return False
        return True

    def to_float(self, value):
        tmp = ''
        mul = 0
        for index in range(len(value)):
            if value[index] in "0987654321.":
                tmp += value[index]
            else:
                mul = value[index]
        tmp = float(tmp)
        if mul != 0:
            if mul.lower() == 'k':
                 tmp *= 1000
            elif mul.lower() == 'm':
                 tmp *= 1000000
        return tmp

    def clear(self):
        self.RL_textedit.setText('')
        self.RS_textedit.setText('')
        self.AV_textedit.setText('')
        self.F_textedit.setText('')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.top = 400
        self.left = 300
        self.height = 300
        self.width = 400
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon("Transistor.png"))
        self.setWindowTitle("Constructor de Amplificadores")
        self.state = 0
        self.Transistor_UI = Transistors()
        self.Parameters_UI = Parameters()
        self.InitWindow()

    def InitWindow(self):
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        self.Display = QPlainTextEdit()
        self.Display.setReadOnly(True)
        self.Display.setPlaceholderText("Here are going to appear some specs if you push the botton below jeje XD")


        self.btn = QPushButton("Select transistors for the amplifier")
        self.btn.clicked.connect(self.take_parameters)

        hbox.addWidget(self.btn)

        vbox.addWidget(self.Display)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def take_parameters(self):
        if self.state == 0:
            self.Transistor_UI.clear()
            self.Parameters_UI.clear()
            self.Display.setPlainText('')
            self.btn.setText("Introduce RS-RL-AV-FrecuencyBand")
            self.Transistor_UI.show()
            self.state += 1
        elif self.state == 1:
            if self.Transistor_UI.CC_amount > 0:
                self.Parameters_UI.CC(True)
                self.Parameters_UI.show()
            else:
                self.Parameters_UI.CC(False)
                self.Parameters_UI.show()
            self.btn.setText("Show Configuration")
            self.state += 1
        elif self.state == 2:
            A = Amplifier(self.Parameters_UI.parameters['RL'], self.Parameters_UI.parameters['RS'], self.Parameters_UI.parameters['AV'],self.Parameters_UI.parameters['F'])
            model = self.Transistor_UI.get_names()
            A = A.Power_amplifier(model, True)
            tmp = ''
            if self.Transistor_UI.CC_amount > 0:
                values = A(self.Parameters_UI.parameters['RL_CC'])
                Component_manager.To_comercial_parameters(values)
            else:
                values = A
                Component_manager.To_comercial_parameters(values)
            for index in values:
                tmp += f'\n\n{index}\n{values[index]}'
            self.Display.setPlainText(tmp)

            self.btn.setText("Select transistors for the amplifier")
            self.state = 0

class Transistors(QWidget):
    def __init__(self):
        super().__init__()
        #listas de transistores
        self.Transistor_CC = QListWidget()
        self.Transistor_EC = QListWidget()
        self.Transistor_List = QListWidget()

        self.CC_amount = 0
        self.transistor_names = []

        self.transistor_models_avaliables = TransistorManager('show')
        self.transistor_models_avaliables = self.transistor_models_avaliables.show_transitors_avaliables()

        self.setWindowTitle("Transistors_selection")
        self.setGeometry(300, 300, 500, 400)
        self.setWindowIcon(QIcon("Transistor.png"))

        Transistors = QHBoxLayout()
        Transistors_Conf = QVBoxLayout()
        Main_vbox = QVBoxLayout()

        #botones
        btn_accept = QPushButton("Accept")
        btn_accept.clicked.connect(self.accept)
        btn_reset = QPushButton("Reset")
        btn_reset.clicked.connect(self.reset)

        #Configuracion de listas
        self.Transistor_CC.setViewMode(QListWidget.IconMode)
        self.Transistor_CC.setAcceptDrops(True)

        self.Transistor_EC.setViewMode(QListWidget.IconMode)
        self.Transistor_EC.setAcceptDrops(True)

        self.Transistor_List.setDragEnabled(True)

        #Labels
        EC = QLabel("EC")
        CC = QLabel("CC")

        Transistors_Conf.addWidget(EC)
        Transistors_Conf.addWidget(self.Transistor_EC)
        Transistors_Conf.addWidget(CC)
        Transistors_Conf.addWidget(self.Transistor_CC)

        Transistors.addWidget(self.Transistor_List)
        Transistors.addLayout(Transistors_Conf)

        Main_vbox.addLayout(Transistors)
        Main_vbox.addWidget(btn_accept)
        Main_vbox.addWidget(btn_reset)


        for index in range(len(self.transistor_models_avaliables)):
            l = QListWidgetItem(QIcon("Transistor.png"), self.transistor_models_avaliables[index])
            self.Transistor_List.insertItem(index, l)

        self.setLayout(Main_vbox)

    def accept(self):
        index = 0
        if self.Transistor_EC.item(0) != None:
            while self.Transistor_EC.item(index) != None:
                tmp = self.Transistor_EC.item(index).text()
                self.transistor_names.append(f'ec:{tmp}')
                index += 1
            index=0
            while self.Transistor_CC.item(index) != None:
                tmp = self.Transistor_CC.item(index).text()
                self.transistor_names.append(f'cc:{tmp}')
                self.CC_amount += 1
                index += 1
            self.close()


    def reset(self):
        index = 0
        while self.Transistor_EC.item(index) != None:
            tmp = self.Transistor_EC.takeItem(0)
            del tmp
            index+=1
        index = 0
        while self.Transistor_CC.item(index) != None:
            tmp = self.Transistor_CC.takeItem(0)
            del tmp
            index += 1

    def get_names(self):
        return self.transistor_names

    def clear(self):
        self.reset()
        self.transistor_names = []

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(App.exec())
