from PySide6.QtCore import QSize, Qt
from functools import partial
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

from app.core.ui_db_manager import UiDbManager
from app.core.components.files_list import FileList

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # --- 1. Criação da Janela Principal ---
        self.setWindowTitle("FM Dados Generator")
        self.resize(800, 600)
        
        
        # --- 2. Criação dos Widgets ---
        
        self.list_arquivos_carregados = FileList()
        # self.list_arquivos_carregados.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_arquivos_carregados_selected_items = []
        
        self.btn_carregar_html = QPushButton("Carregar HTML")
        
        self.btn_excluir_html = QPushButton("Excluir Seleção")
        
        self.btn_clear_list = QPushButton("Limpar Lista")
        
        self.btn_gerar_bd = QPushButton("Gerar DB")
        
        self.ui_db_manager = UiDbManager()
        
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
        
        self.btn_carregar_html.clicked.connect(
            partial(self.ui_db_manager.select_files, self.list_arquivos_carregados))
        
        self.btn_clear_list.clicked.connect(partial(self.ui_db_manager.clear_all_files, self.list_arquivos_carregados))
        self.btn_excluir_html.clicked.connect(self.update_selected_list_items)
        self.btn_excluir_html.clicked.connect(self.ui_db_manager.remove_selecteds_items)
        self.btn_gerar_bd.clicked.connect(self.ui_db_manager.create_db)
        # self.list_arquivos_carregados.itemSelectionChanged.connect(self.update_selected_list_items)
   
        self.ui_db_manager.files_changed.connect(self.atualizar_lista_widget)


    def update_selected_list_items(self):
        
        self.list_arquivos_carregados_selected_items = self.list_arquivos_carregados.selectedItems()
        
        items = [item.text() for item in self.list_arquivos_carregados.selectedItems()]
        self.ui_db_manager.set_selected_files(items=items)
    
            
    def atualizar_lista_widget(self, lista_de_arquivos):

            self.list_arquivos_carregados.clear()
            self.list_arquivos_carregados.addItems(lista_de_arquivos)
