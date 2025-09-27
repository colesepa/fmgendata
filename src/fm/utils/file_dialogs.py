from ..app.configs import DEFAULT_PATH, ALL_FILES_FILTER
from typing import Tuple, Optional
from PySide6.QtWidgets import QFileDialog, QWidget

def choose_html_file(
    parent: Optional[QWidget] = None,
    start_dir: str = DEFAULT_PATH,
    file_filter: str = ALL_FILES_FILTER) -> Tuple[Optional[str], Optional[str]]:
    
    """
    Abre um QFileDialog para selecionar um HTML e retorna (path, selected_filter).
    - parent: normalmente self (MainWindow)
    - start_dir: diretório inicial (se None, usa Documentos do usuário)
    - file_filter: filtro para o diálogo
    Retorna (None, None) se o usuário cancelar.
    """
     
    path, used_filter = QFileDialog.getOpenFileName(
        parent = parent,
        dir = start_dir,
        filter=file_filter,
        selectedFilter = file_filter
    )
    
    if not path:
        return None, None
    
    return path, used_filter