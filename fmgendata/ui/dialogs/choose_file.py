from typing import Tuple, Optional
from PySide6.QtWidgets import QFileDialog, QWidget
from fmgendata.config.settings import DEFAULT_PATH, ALL_FILES_FILTER


#TODO: Incluir essa funçao em algum management de aruqivos
def choose_file(
    selected_parent: Optional[QWidget] = None,
    start_dir: str = DEFAULT_PATH,
    file_filter: str = ALL_FILES_FILTER,
    *args, 
    **kwargs) -> Tuple[Optional[str], Optional[str]]:
    
    path, used_filter = QFileDialog.getOpenFileName(
        parent = selected_parent,
        caption = "Selecione um arquivo",
        dir = start_dir,
        filter = file_filter,
        selectedFilter= file_filter
        ) 

    if not path:
        return None, None
    
    return path, used_filter