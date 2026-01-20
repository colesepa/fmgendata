import os 
import sys
from pathlib import Path

"""
    Clase de manejo e controle dos diretórios necessários para funcionamneto do
    app. 
    
    Principais objetivos:

       Fornecer o caminho base de diretórios do sistema para criação de pastas do app para
       salvamento/importações de arquivos necessários para o funcionamento do app.
        
        Verificar a existência desse caminho base de diretórios. 
    
"""

class DirectoryManager:
    
    def __init__(self, 
                 app_name: str, 
                 portable: bool = False, 
                 base_dir: Path | None = None)  -> None:
        """
        app_name: nome do aplicativo (ex: "FMGenData)
        portable: se True, salva os diretórios dentro da pasta raiz do projeto,
            ao lado do Script/exe (modo pendrive).
        base_dir: se passar um valor, força um diretório específico para o proj. 
        """
        
        self.app_name = app_name
        self.portable = portable
        self._base_dir = base_dir


    def get_base_dir(self) -> Path:

        """
        Função que retorna a base para criação da estrutura básica de diretórios
        requeridas pelo app, com base no sistema operacional que o app esteja
        rodando.
        """

        #força um diretório específico
        if self._base_dir is not None:
            return self._base_dir
        
        
        # caso True, cria a estrutura de pasta ao lado da pasta do app. (dev)
        if self.portable:
            return Path.cwd()/"userdata"

        platform = sys.platform # verificador de qual SO está rodando

        if platform.startswith("win"):
            
            local = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
            
            if not local:
                return Path.home()/"AppData"/"Local"/self.app_name
            
            return Path(local)/self.app_name

        if platform == "darwin":
            return Path.home()/"Library"/"Application Support"/self.app_name

       
      # verificações para sistema Unix 
        
        xdg_data_home = os.environ.get("XDG_DATA_HOME")

        if xdg_data_home:
            return Path(xdg_data_home)/self.app_name 
            
        else:
            return Path.home()/".local"/"share"/self.app_name

    
    # garantindo que o diretório base esteja sempre atualizado  
    @property
    def base_dir(self) -> Path:
        return self.get_base_dir()

    @property
    def db_dir(self) -> Path:
        return self.base_dir /"data"
    
    @property
    def log_dir(self) -> Path:
        return self.base_dir / "logs"

    @property
    def export_dir(self) -> Path:
        return self.base_dir / "exports"
    
    @property
    def import_data_dir(self) -> Path:
        return self.base_dir/"imports"/"raw_data"
    
    def ensure_structure(self) -> None:
                
        """
        Função que certifica a existência da estrutura de diretório padrão de modo
        a garantir o padrão de importação e exportação.  
        """

        for d in (
            self.base_dir,
            self.db_dir,
            self.log_dir,
            self.export_dir,
            self.import_data_dir):
            
            d.mkdir(parents=True, exist_ok=True)

    def can_write(self, path:Path | None = None) -> bool:

        """
        Teste de validação de possibilidade de escritura dentro do diretório criado 
        (criando um arquivo temporário).
        """

        target = path or self.base_dir
        
        try:
            
            target.mkdir(parents=True, exist_ok=True)
            test_file = target/".write_text"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink(missing_ok=True)
            
            return True
        
        except Exception:
            return False
        
    def db_path(self, file_name: str = "data.db") -> Path:
        return self.db_dir/ file_name

        
        
# if __name__ == "__main__":
#     dm = DirectoryManager('fmgendata', portable=True)
#     dm.ensure_structure()
    
#     print("Base:", dm.base_dir)
#     print("DB", dm.db_path())
#     print("Pode escrever ?", dm.can_write())
   