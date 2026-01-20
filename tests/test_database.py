from fmgendata.infra.storage.database import Database
from fmgendata.core.services.data_manipulation import fm_create_dataframe, df_to_slq_inject


def test_injenct_data_on_database(db: Database) -> None:
    
    path = 'userdata/imports/raw_data/foggia_2024.html'
    db = Database(":memory:")
    df = fm_create_dataframe(path)
    df = df_to_slq_inject(df)
    db.bulk_upsert(df)
    
    assert db.len_db > 0
    
def test_init_database(empyty_db: Database) -> None:
    assert isinstance(empyty_db, Database)
    
def test_len_data(empyty_db: Database) -> None:
    assert empyty_db.len_db == 0
    assert empyty_db.sources == []
    
