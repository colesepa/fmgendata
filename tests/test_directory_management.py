from fmgendata.infra.storage.directory_manager import DirectoryManager
import pytest
from pathlib import Path


@pytest.fixture
def dm(tmp_path: Path) -> DirectoryManager: #tmp_path é uma fixture padrão
    
    base = tmp_path/ "FMGenData" # definição do diretório base de teste
    return DirectoryManager(app_name="FMGenData", base_dir=base)

@pytest.fixture
def dm_portable(tmp_path: Path) -> DirectoryManager: #tmp_path é uma fixture padrão
    
    base = tmp_path/ "FMGenData" # definição do diretório base de teste
    return DirectoryManager(app_name="FMGenData",portable=True, base_dir=base)

def test_base_dir_forced(dm: DirectoryManager, tmp_path: Path) -> None:
    assert dm.base_dir == tmp_path/ "FMGenData"
    
def test_ensure_structure_creates_dirs(dm: DirectoryManager) -> None:
    
    dm.ensure_structure()
    
    assert dm.base_dir.is_dir()
    assert dm.db_dir.is_dir()
    assert dm.log_dir.is_dir()
    assert dm.export_dir.is_dir()
    
def test_db_path(dm: DirectoryManager) -> None:
    
    assert dm.db_path() == dm.db_dir/"data.db"
    assert dm.db_path("test.db") == dm.db_dir/"test.db"
    
def test_can_write_base_dir(dm: DirectoryManager) -> None:
    
    assert dm.can_write() is True
    
def test_can_write_specific_path(dm: DirectoryManager, tmp_path: Path) -> None:
    
    other_path = tmp_path/"other"
    assert dm.can_write(other_path) is True
    

