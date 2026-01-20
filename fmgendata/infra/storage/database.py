from pathlib import Path
import sqlite3
import pandas as pd 
from typing import List, Any
from .db_schema import SCHEMA_BASE
# from fmgendata.infra.storage.directory_manager import DirectoryManager


class Database():
    
    def __init__(
        self,
        db_name: str  = "data.db",
        schema: str = SCHEMA_BASE,
        path: str | Path | None = None) -> None:
       
        self.db_name = db_name
        self.schema = schema
        # self.db_path = path
        
        if path is None:
            
            self.db_path = f"/home/mjsa/Github/fmgendata/userdata/data/self.db_name"
                 
            
        elif str(path) == ":memory:":
            self.db_path = ":memory:"
        
    # TODO: Criar verificação se a pasta que armazena a database está criada
        
        else:
            self.db_path = Path(path)


        self._conn = sqlite3.connect(self.db_path)
        self._create_tables()
       
        
    @property
    def len_db(self) -> int:
        return self.count_data()
    
    @property
    def sources(self) -> list:
        
        return self.get_unique_values(column='source')
    
    def _create_tables(self) -> None:
        
        cur = self._conn.cursor()
        
        
        try:
            cur.execute(self.schema)
            self._conn.commit()
        except Exception as e:
            print(f"{e}: Falha ao criar tabela.")
            self._conn.rollback()

        finally:
            self.close()
    
    def bulk_upsert(self, data: pd.DataFrame, table_name: str = 'stats') -> None:
        
        cur = self._conn.cursor()
        
        columns_df = list(data.columns)
        values = list(data.itertuples(index=False, name=None))
        
        placeholders = ", ".join(["?"]*len(columns_df))
        insert_columns = ", ".join(columns_df)
        update_columns = ", ".join(
            [f'{col}=excluded.{col}' 
             for col in columns_df if col not in ("id", "id_temporada")])
        
        query = f"""
        INSERT INTO {table_name} ({insert_columns})
        VALUES ({placeholders})
        ON CONFLICT(id, id_temporada) DO UPDATE SET
        {update_columns};
        """
        try:
            cur.executemany(query, values)
            self._conn.commit()
            print("Dados Adicionado/Atualizados com sucesso.")
        
        except Exception as e:
            print(f"{e}: Erro ao Adicionar/Atualizar dados.")
            self._conn.rollback()
            
    def clear_table(self, table_name: str = 'stats') -> None:

        cur = self._conn.cursor()
        
        try:
            cur.execute(f"DELETE FROM {table_name}")
            print(f'Tabela <{table_name}> limpa com sucesso.')
            self._conn.commit()
        
        except Exception as e:
            print(f'{e}: Erro ao limpar tabela')
            self._conn.rollback()   
    
    def delete_rows(
        self,
        column_name: str,
        values_ref: List[Any],
        table_name: str = 'stats') -> None:
        
        if not values_ref:
            print("Nenhum valor fornecido para exlcusão.")
            return
        
        cur = self._conn.cursor()
        
        placeholders = ", ".join(["?"]*len(values_ref))
        query = f"""
        DELETE FROM {table_name}
        WHERE {column_name} in ({placeholders})
        """
        
        try:
            cur.execute(query, values_ref)
            print("Linhas excluidas com sucesso.")
            self._conn.commit()
        
        except Exception as e:
            print(f"{e}: Erro ao excluir linhas")
            self._conn.rollback()
    
    def count_data(self, table_name: str = "stats") -> int:
        cur = self._conn.cursor()
        
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cur.fetchone()[0]
        
        return count
    
    def get_unique_values(self, column: str, table_name: str = 'stats') -> list:
        cur = self._conn.cursor()
        try:
            cur.execute(f"SELECT DISTINCT {column} FROM {table_name} WHERE {column} IS NOT NULL")
            return [row[0] for row in cur.fetchall()]
        except Exception as e:
            print(f"{e}")
            return []
        
    def close(self) -> None:
        if self._conn:
            self._conn.close()
        