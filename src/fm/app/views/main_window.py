from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout

#Criação da janela principal, criando uma subclase da classe QMainWindow
class MainWindow(QMainWindow):
    def __init__(self): #Iniciando a subclasse
        super().__init__() #Iniciando todos os métodos da classe pai
        self.setWindowTitle("FM GenData") #Título da janela
        self.resize(600,400) #Configuraçao do tamanho inicial da janela
        
      
        #Criaçcão do container principal que irá englobar toda estrutura
        container = QWidget()
        
        #Definição do Layout da janela principal
        container_layout = QVBoxLayout()
        
        #Adicionar as widgets dos labels dentro do layout
        container_layout.addWidget(QLabel("Texto 1"))
        container_layout.addWidget(QLabel("Texto 2"))
        
        #Definir o layout do container
        container.setLayout(container_layout)
        self.setCentralWidget(container)
        