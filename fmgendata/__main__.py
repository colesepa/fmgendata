import sys
from PySide6.QtWidgets import QApplication
from fmgendata.ui.windows.main_window import MainWindow
from fmgendata.infra.storage.directory_manager import DirectoryManager

 
   
   
def main() -> int:
     
    app = QApplication(sys.argv)
    
    
    
    dm = DirectoryManager(app_name="FmGenData", portable=False)
    dm.ensure_structure()
    
    
    
    window = MainWindow()
    window.show()
    
    
    return sys.exit(app.exec())   

