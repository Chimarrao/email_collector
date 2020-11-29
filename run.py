from PyQt5 import QtCore, QtGui, QtWidgets
import buscador
buscador = buscador.buscador()

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(523, 528)
        Dialog.setFixedSize(523, 528)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\icons/icons8-email-open-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.label_nicho = QtWidgets.QLabel(Dialog)
        self.label_nicho.setEnabled(True)
        self.label_nicho.setGeometry(QtCore.QRect(10, 5, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_nicho.setFont(font)
        self.label_nicho.setObjectName("label_nicho")
        self.iniciar = QtWidgets.QPushButton(Dialog)
        self.iniciar.setGeometry(QtCore.QRect(390, 5, 61, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.iniciar.setFont(font)
        self.iniciar.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\icons/play-dentro-de-um-círculo-96.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.iniciar.setIcon(icon)
        self.iniciar.setIconSize(QtCore.QSize(60, 60))
        self.iniciar.setCheckable(False)
        self.iniciar.setFlat(True)
        self.iniciar.setObjectName("iniciar")
        self.emails = QtWidgets.QTextBrowser(Dialog)
        self.emails.setGeometry(QtCore.QRect(10, 70, 501, 401))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.emails.setFont(font)
        self.emails.setObjectName("emails")
        self.salvar = QtWidgets.QPushButton(Dialog)
        self.salvar.setGeometry(QtCore.QRect(450, 5, 61, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.salvar.setFont(font)
        self.salvar.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(".\\icons/icons8-save-96.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.salvar.setIcon(icon1)
        self.salvar.setIconSize(QtCore.QSize(60, 60))
        self.salvar.setCheckable(False)
        self.salvar.setFlat(True)
        self.salvar.setObjectName("salvar")
        self.label_divisor = QtWidgets.QLabel(Dialog)
        self.label_divisor.setEnabled(True)
        self.label_divisor.setGeometry(QtCore.QRect(180, 5, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_divisor.setFont(font)
        self.label_divisor.setObjectName("label_divisor")
        self.divisor = QtWidgets.QComboBox(Dialog)
        self.divisor.setGeometry(QtCore.QRect(180, 30, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.divisor.setFont(font)
        self.divisor.setObjectName("divisor")
        self.divisor.addItem("")
        self.divisor.addItem("")
        self.divisor.addItem("")
        self.nicho = QtWidgets.QLineEdit(Dialog)
        self.nicho.setGeometry(QtCore.QRect(10, 30, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nicho.setFont(font)
        self.nicho.setObjectName("nicho")
        self.progresso = QtWidgets.QProgressBar(Dialog)
        self.progresso.setGeometry(QtCore.QRect(10, 480, 501, 41))
        self.progresso.setProperty("value", 24)
        self.progresso.setObjectName("progresso")
        self.progresso.setValue(0)
        self.label_configuracoes = QtWidgets.QLabel(Dialog)
        self.label_configuracoes.setEnabled(True)
        self.label_configuracoes.setGeometry(QtCore.QRect(270, 5, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_configuracoes.setFont(font)
        self.label_configuracoes.setObjectName("label_configuracoes")
        self.emails_brasileiros = QtWidgets.QCheckBox(Dialog)
        self.emails_brasileiros.setGeometry(QtCore.QRect(270, 30, 120, 13))
        self.emails_brasileiros.setObjectName("emails_brasileiros")
        self.emails_conhecidos = QtWidgets.QCheckBox(Dialog)
        self.emails_conhecidos.setGeometry(QtCore.QRect(270, 45, 120, 13))
        self.emails_conhecidos.setObjectName("emails_conhecidos")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        def receberSinal(comando, valor):
            if comando == "addEmail":
                self.emails.append(valor)
                
            elif comando == "inicioBusca":
                self.emails.setText(valor)
                
            elif comando == "setProgresso":
                self.progresso.setValue(int(valor))
                
            else:
                pass
        
        # Seta a função para recebimento de sinais
        buscador.sinal.connect(receberSinal)

        # Seta as funções para botões
        self.iniciar.clicked.connect(self.iniciarBusca)
        self.salvar.clicked.connect(self.salvarTxt)
        
    def iniciarBusca(self):
        buscador.buscaEmails(self.nicho.text(), self.emails_brasileiros, self.emails_conhecidos)
        
    def salvarTxt(self):
        buscador.salvarTxt(self.divisor.currentText())
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "E-mail Collector - Art Software"))
        self.label_nicho.setText(_translate("Dialog", "Nicho:"))
        self.label_divisor.setText(_translate("Dialog", "Divisor:"))
        self.divisor.setItemText(0, _translate("Dialog", "Linha"))
        self.divisor.setItemText(1, _translate("Dialog", "Dois pontos"))
        self.divisor.setItemText(2, _translate("Dialog", "Vírgula"))
        self.label_configuracoes.setText(_translate("Dialog", "Configurações:"))
        self.emails_brasileiros.setText(_translate("Dialog", "E-mails brasileiros"))
        self.emails_conhecidos.setText(_translate("Dialog", "Domínios conhecidos"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
