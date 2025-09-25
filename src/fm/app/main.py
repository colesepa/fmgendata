import sys
from PySide6.QtWidgets import QApplication
from .views.main_window import MainWindow #Importação da Janela principal


if __name__ == "__main__":
    app = QApplication() #Criando a aplicaçao QT no sistema 
    window = MainWindow() #importando o container que vai agrupar o app
    window.show() #Mostando o aplicativo
    sys.exit(app.exec()) #roda o envent loop
    
    