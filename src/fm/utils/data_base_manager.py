from typing import List
from .file_dialogs import choose_html_file
import os
from pathlib import Path
from ..app.configs import HTML_FILTER

class DatabaseManager():
    def __init__(self) -> None:
        self.temp_htmls_dicts = {}
        
    
    #Importar os paths dos html 
    
    def select_html_files(self) -> None:
        
        paths, _used_filter = choose_html_file(file_filter=HTML_FILTER)
        
        if paths:
            
            path_obj = Path(paths)
            
            file_name = os.path.basename(paths)
            file_name_ne = path_obj.stem
            
            self.temp_htmls_dicts[file_name_ne] = {"abs_name":file_name,
                                                   "path":paths}
            print(self.temp_htmls_dicts)
            print(_used_filter)
        
        
            
        
    
    