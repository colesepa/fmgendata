from PySide6.QtWidgets import (
    QMainWindow, 
    QLabel, 
    QWidget, 
    QVBoxLayout,
    QStatusBar
    )
from PySide6.QtGui import QAction

#Criação da janela principal, criando uma subclase da classe QMainWindow
class MainWindow(QMainWindow):
    def __init__(self): #Iniciando a subclasse
        super().__init__() #Iniciando todos os métodos da classe pai
        self.setWindowTitle("FM GenData") #Título da janela
        self.resize(600,400) #Configuraçao do tamanho inicial da janela
        self.setStatusBar(QStatusBar(self)) #adicionando status bar a janela
        self.statusBar().showMessage("Pronto", 2000) #configurando msg
      
        #Conteúdo central
      
        container = QWidget() #Criaçcão do container principal 
        container_layout = QVBoxLayout() #Definição do Layout da janela principal
        container_layout.addWidget( #Adicionar as widgets dos labels dentro do layout
            QLabel("Área principal")) 
        container.setLayout(container_layout) #Definir o layout do container
        self.setCentralWidget(container)
        
        #Criação do menu Arquivo na barra de MenuBar
        menu_bar_arquivo = self.menuBar().addMenu("Arquivo")
        #Adicionando um ação a janela principal
        self.act_importar = QAction("importar HTML...", self)
        #Linkando a acao de importar ao menu de importar do menubar
        menu_bar_arquivo.addAction(self.act_importar)
        
        #Adicionando a ação de sair do menu bar
        self.act_sair = QAction("Sair", self)
        #Adicionando a função "Sair" ao evento do clique do botão sair
        self.act_sair.triggered.connect(self.close)
        menu_bar_arquivo.addAction(self.act_sair)
        
        
        
        