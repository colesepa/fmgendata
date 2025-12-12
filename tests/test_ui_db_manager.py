from app.core.ui_db_manager import*

ui_manager = UiDbManager()

def test_has_data_file():
    assert ui_manager._has_data_file() == True