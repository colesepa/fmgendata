import os

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QListWidget
from pathlib import Path
from typing import List
from core.choose_file import choose_file
from configs import HTML_FILTER


class UiDbManager(QObject):
    
    files_changed = Signal(list)
    
    def __init__(self) -> None:
        super().__init__()
        self.temp_html_files = {}
        self._files_on_db = []
        self._selected_files = []
    
    def select_files(self) -> None:
        
        print(f"Debug: {self.temp_html_files}")
        print(f"Debug: {self._files_on_db}")
        
        paths, _used_filter = choose_file(file_filter=HTML_FILTER)
        
        if paths:
            
            path_obj = Path(paths)
            
            file_name = os.path.basename(paths)
            file_name_non_ext = path_obj.stem
            
            if not file_name_non_ext in self.temp_html_files:
            
                self.temp_html_files[file_name_non_ext] = {
                    "abs_name": file_name,
                    "path":paths}
                
                self._files_on_db.append(file_name)
                
                self.files_changed.emit(self._files_on_db)
                
            else:
                
                print("DEBUG: Arquivo já selecionado.")
                #implantar alertar de arquivo existente
                pass
    
    def clear_all_files(self):

        self.temp_html_files.clear()
        self._files_on_db.clear()
        self.files_changed.emit(self._files_on_db)
        
    def set_selected_files(self, items:list) -> None:
        
        self._selected_files.clear()
        self._selected_files = items
                
        return 
    
    def remove_selecteds_items(self):
        
        items = self._selected_files
        
        for item in items:
            if item in self._files_on_db:
                self._files_on_db.remove(item)
            
            key = item.removesuffix(".html")  
            if key in self.temp_html_files:    
                del  self.temp_html_files[key]
               
            
        self.files_changed.emit(self._files_on_db)
        self._selected_files.clear()
        
        print(f"Debug-Remove: {self.temp_html_files}")
        print(f"Debug-Remove: {self._files_on_db}")
