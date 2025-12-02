from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QMainWindow, 
    QLabel, 
    QTabWidget, 
    QWidget,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QAbstractItemView,
    )

from core.db_manager import DbManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # --- 1. Criação da Janela Principal ---
        self.setWindowTitle("FM Dados Generator")
        self.resize(800, 600)
        
        
        # --- 2. Criação dos Widgets ---
        
        self.list_arquivos_carregados = QListWidget()
        self.list_arquivos_carregados.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_arquivos_carregados_selected_items = self.list_arquivos_carregados.selectedItems()
        
        self.btn_carregar_html = QPushButton("Carregar HTML")
        
        self.btn_excluir_html = QPushButton("Excluir Seleção")
        
        self.btn_clear_list = QPushButton("Limpar Lista")
        
        self.btn_gerar_bd = QPushButton("Gerar DB")
        
        self.db_manager = DbManager()
        
        self.statusBar().showMessage("Pronto", 2000)
        
        
        # --- 3. Configuração do Layout inicial
        
        layout_btn = QVBoxLayout()
        layout_btn.addWidget(self.btn_carregar_html)
        layout_btn.addWidget(self.btn_excluir_html)
        layout_btn.addWidget(self.btn_clear_list)
        layout_btn.addWidget(self.btn_gerar_bd)
        layout_btn.addStretch()
        
        layout_principal = QHBoxLayout()
        layout_principal.addWidget(self.list_arquivos_carregados, 3)
        layout_principal.addLayout(layout_btn, 1)
        
        
        container = QWidget()
        container.setLayout(layout_principal)
        self.setCentralWidget(container)
        
        # --- Signals ---
        
        self.btn_carregar_html.clicked.connect(self.db_manager.select_files)
        self.btn_clear_list.clicked.connect(self.db_manager.clear_all_files)
        self.btn_excluir_html.clicked.connect(self.update_selected_list_items)
        self.btn_excluir_html.clicked.connect(self.db_manager.remove_selecteds_items)




        self.db_manager.files_changed.connect(self.atualizar_lista_widget)


    def update_selected_list_items(self):
        
        items = [item.text() for item in self.list_arquivos_carregados.selectedItems()]
        self.db_manager.set_selected_files(items=items)
    
            
    def atualizar_lista_widget(self, lista_de_arquivos):

            self.list_arquivos_carregados.clear()
            self.list_arquivos_carregados.addItems(lista_de_arquivos)
