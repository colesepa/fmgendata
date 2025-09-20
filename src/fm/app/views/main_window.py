from PySide6.QtWidgets import QMainWindow, QLabel

#Criação da janela principal, criando uma subclase da classe QMainWindow
class MainWindow(QMainWindow):
    def __init__(self): #Iniciando a subclasse
        super().__init__() #Iniciando todos os métodos da classe pai
        self.setWindowTitle("FM GenData") #Título da janela
        self.resize(600,400) #Configuraçao do tamanho inicial da janela
        
        