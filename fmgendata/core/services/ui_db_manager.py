import os
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QListWidget
from pathlib import Path
from typing import List
from fmgendata.ui.dialogs.choose_file import choose_file
from fmgendata.config.settings import HTML_FILTER
from .db_manager import bulk_upsert, create_db
from .data_manipulation import fm_create_dataframe
import pandas as pd
from fmgendata.ui.widgets.files_list import FileList


class UiDbManager(QObject):
    
    files_changed = Signal(list)
    
    def __init__(self) -> None:
        super().__init__()
        self.temp_html_files = {}
        self._files_on_db = []
        self._selected_files = []
    
    def select_files(self, widget_list: FileList) -> None:
        
        list_files = widget_list
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
                list_files.loaded_files.append(file_name)
                
                self.files_changed.emit(self._files_on_db)
                
            else:

                pass
    
    def clear_all_files(self, widget_list: FileList):

        list_files = widget_list
        
        self.temp_html_files.clear()
        self._files_on_db.clear()
        list_files.loaded_files.clear()
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

    def _has_data_file(self) -> bool:
        
        root = Path(__file__).resolve().parents[2]
        path_data = root/'data'/'db'/'data.db'
        
        return Path.is_file(path_data)
    
    def create_db(self) -> None:
        
        files = self._selected_files
        
        if not self._has_data_file():
            create_db()
            
        elif files:
            
            df = pd.DataFrame()
            for file in files:
                path = self.temp_html_files[file.removesuffix(".html")]['path']
                df = fm_create_dataframe(path)
                bulk_upsert(df)
              
            
    