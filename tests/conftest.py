from typing import Any, Generator
import pytest
from app.core.database import Database
from app.core.data_manipulation import fm_create_dataframe, df_to_slq_inject

@pytest.fixture
def empyty_db() -> Generator[Database, Any, None]:
    db = Database(":memory:")
    yield db
    db.close()
    
@pytest.fixture
def db()  -> Generator[Database, Any, None]:
    
    path = '/home/mjsa/Github/fmgendata/data/raw/Italia_2024.html'
    db = Database(":memory:")
    df = fm_create_dataframe(path)
    df = df_to_slq_inject(df)
    db.bulk_upsert(df)
    
    yield db
    db.close()
