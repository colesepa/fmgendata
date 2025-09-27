from PySide6.QtWidgets import (
    QMainWindow, 
    QLabel, 
    QWidget, 
    QVBoxLayout,
    QStatusBar,
    QFileDialog,
    QFrame,
    QPushButton,
    )
from PySide6.QtGui import QAction
from ..configs import*
from ...utils.data_base_manager import DatabaseManager



#Criação da janela principal, criando uma subclase da classe QMainWindow
class MainWindow(QMainWindow):
    def __init__(self): #Iniciando a subclasse
        super().__init__() #Iniciando todos os métodos da classe pai
        self.setWindowTitle("FM GenData") #Título da janela
        #Configuraçao do tamanho inicial da janela
        self.resize(WINDOW_GEOMETRY[0],WINDOW_GEOMETRY[1]) 
        self.setMinimumSize(WINDOW_MIN_SIZE[0], WINDOW_MIN_SIZE[1])
        self.db_manager = DatabaseManager()
        self.btn_import_html = QPushButton("Import HTML")
        self.btn_add_html = QPushButton("Add HTML to DB")
        self.btn_remove_html = QPushButton("Remove HTML to DB")

        
        
        #Conteúdo central

        container = QWidget() #Criaçcão do container principal 
        container_layout = QVBoxLayout() #Definição do Layout da janela principal
        #Frame dos botoes
        
        btn_frame = QFrame()
        btn_frame.setFixedSize(130, 300)
        btn_frame_layout = QVBoxLayout()
        btn_frame.setLayout(btn_frame_layout)
        btn_frame.setStyleSheet("""
                                QFrame{
                                    border-radius: 15px;
                                    background-color: red;}
                                """)
        
        #Adicionar as widgets dos labels dentro do layout
        btn_frame_layout.addWidget(self.btn_import_html) 
        btn_frame_layout.addWidget(self.btn_add_html) 
        btn_frame_layout.addWidget(self.btn_remove_html) 
        
        container_layout.addWidget(btn_frame)
        container.setLayout(container_layout) #Definir o layout do container
        self.setCentralWidget(container)

        self.btn_import_html.clicked.connect(self.db_manager.select_html_files)
        
    