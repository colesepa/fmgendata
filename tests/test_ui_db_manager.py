from fmgendata.core.services.ui_db_manager import*
import pytest

ui_manager = UiDbManager()

@pytest.fixture
def has_data(tmp_path: Path) -> Path:
    
    path_witch_data = tmp_path/"data.db"
    return path_witch_data

@pytest.fixture
def no_data(tmp_path: Path) -> Path:
    
    path_no_data = tmp_path
    return path_no_data


def test_has_data_file():
    assert ui_manager._has_data_file() == False