from PySide6.QtWidgets import QListWidget, QAbstractItemView


class FileList (QListWidget):
    
    def __init__(self) -> None:
        super().__init__()
        self.selected_files = []
        self.loaded_files = []
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        
        self.itemSelectionChanged.connect(self.update_selected_files)
    
    def update_selected_files(self) -> None:
        
        self.selected_files = [item.text() for item in self.selectedItems()]
        print("Carregados: ", self.loaded_files)
        print("Selecionados: ", self.selected_files)
        
        