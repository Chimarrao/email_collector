import io
import re
import math
import packs
import datetime
import requests
import threading
from PyQt5 import QtCore
from bs4 import BeautifulSoup
from googlesearch import search

packs = packs.packs()

class buscador(QtCore.QThread):
    # Variáveis do script
    nomesComuns = []
    todosEmails = []
    emailsAtuais = []
    dominiosLista = []
    dominiosBusca = ""
    limiteAtingido = False
    mensagemLimite = "Limite de e-mails impressos em tela"
    mensagemTxt = "Mas você ainda pode gerar o arquivo de texto normalmente"
    
    # Variável responsável pelo sinal
    sinal = QtCore.pyqtSignal(object, str)

    def __init__(self):
        self.nomesComuns = packs.getNomes()
        QtCore.QThread.__init__(self)

    # Filtra os emails encontrados
    def filtraEmails(self, emailsAtuais):
        for email in emailsAtuais:
            
            # Impede a entrada de emails duplicados
            if email in self.todosEmails:
                continue
            
            # Impede a entrada de emails que não estão nos domínios conhecidos
            dominioOk = False
            for dominio in self.dominiosLista:
                dominioAtual = email.split("@")[1]
                if dominioAtual in dominio:
                    dominioOk = True
                    break
                
            if not dominioOk:
                continue

            # Impede a entrada de emails muito curtos ou muito longos
            if len(email) < 12 or len(email) > 50:
                continue

            # Impede a entrada de e-mails que não são brasileiros
            if len(self.nomesComuns) > 0:
                emailBrasileiro = False
                for nome in self.nomesComuns:
                    if nome in email and len(nome) > 2:
                        emailBrasileiro = True
                        break

                if not emailBrasileiro:
                    continue

            # Adiciona na lista de todos os emails
            self.todosEmails.append(email)

            # Se o limite de emails impressos em tela não for atingido
            if len(self.todosEmails) < 300:
                self.sinal.emit("addEmail", email.strip())

            # Caso o limite já tenha sido atingido
            elif not self.limiteAtingido:
                self.limiteAtingido = True
                self.sinal.emit("addEmail", ".")
                self.sinal.emit("addEmail", ".")
                self.sinal.emit("addEmail", ".")
                self.sinal.emit("addEmail", self.mensagemLimite)
                self.sinal.emit("addEmail", self.mensagemTxt)

    # Grava informações em um arquivo txt
    def salvarTxt(self, divisor):
        divisorTxt = "\n"
        
        # Seta o tipo de divisor do texto
        if divisor == "Linha":
            divisorTxt = "\n"
        elif divisor == "Dois pontos":
            divisorTxt = ":"
        elif divisor == "Vírgula":
            divisorTxt = ","
            
        d = datetime.datetime.now()
        data = '{}-{}-{} {}-{}-{}'.format(d.day, d.month, d.year, d.hour, d.minute, d.second)

        try:
            with io.open("resultado/Emails " + data + ".txt", "a+", encoding="utf-8") as txt:
                for email in self.todosEmails:
                    txt.write(email + divisorTxt)

            txt.close()
        except Exception as e:
            pass
        
    def setaVariaveis(self, brasileiros, conhecidos):
        # Reza as variáveis do sistema
        self.limiteAtingido = False
        self.nomesComuns = []
        self.todosEmails = []
        self.emailsAtuais = []
        self.dominiosLista = []
        self.dominiosBusca = ""
        
        # Apaga a lista antiga
        if len(self.todosEmails) > 0:
            self.todosEmails = []

        # Carrega os principais nomes brasileiros na lista
        if brasileiros.isChecked():
            self.nomesComuns = packs.getNomes()

        # Carrega os domínios de emails nas listas
        if conhecidos.isChecked():
            self.dominiosBusca = packs.getPrincipaisDominios()
            self.dominiosLista = packs.getPrincipaisDominiosLista()
        else:
            self.dominiosBusca = packs.getDominiosString()
            self.dominiosLista = packs.getDominiosLista()
            
        # Zera o progresso
        self.sinal.emit("setProgresso", str(0))

    # Inicia a busca pelos emails
    def buscaEmails(self, nicho, brasileiros, conhecidos):
        self.setaVariaveis(brasileiros, conhecidos)

        # Realiza a busca de emails
        def busca():
            progresso = 0
            self.sinal.emit("inicioBusca", "Buscando...")

            for resultado in search(nicho + self.dominiosBusca, stop=13):
                try:
                    html = requests.get(resultado).content
                    soup = BeautifulSoup(html, "html.parser")
                    dados = soup.prettify()

                    emails = re.findall(r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+', dados)
                    self.filtraEmails(emails)

                    if len(emailsAtuais) > 0:
                        emailsAtuais.clear()
                except Exception as e:
                    pass

                progresso += 7.69230769
                self.sinal.emit("setProgresso", str(math.ceil(progresso)))

            self.sinal.emit("addEmail", ".")
            self.sinal.emit("addEmail", ".")
            self.sinal.emit("addEmail", ".")
            self.sinal.emit("addEmail", "Fim")
            self.sinal.emit("setProgresso", str(100))

        # Thread responsável pela busca dos emails
        threadBusca = threading.Thread(target=busca)
        threadBusca.start()
