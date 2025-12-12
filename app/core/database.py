from pathlib import Path
import sqlite3
import pandas as pd 
from typing import List, Any

class Database():
    
    def __init__(self, path: str | Path | None = None) -> None:
        self.db_name = 'data.db'
        
        if path == None:
            self.db_path = Path(__file__).resolve().parents[2]/'data'/'db'/self.db_name
            
        elif str(path) == ":memory:":
            self.db_path = ":memory:"
            
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
        
        scheme = f"""
            CREATE TABLE IF NOT EXISTS stats (
            id INTEGER,
            nome TEXT,
            nac TEXT,
            idade INTEGER,
            altura TEXT,
            posicao TEXT,
            melhor_pe TEXT,
            person TEXT,
            clube TEXT,
            divisao TEXT,
            salario INTEGER,
            final_contrato TEXT,
            partidas TEXT,
            minutos INTEGER,
            nota_med REAL,
            motm REAL,
            ass REAL,
            gols REAL,
            gk_sg REAL,
            gk_gsof_p90 REAL,
            xG REAL,
            npxG REAL,
            chutes_p90 REAL,
            passe_t_p90 REAL,
            passe_c_p90 REAL,
            chutes_gol_p90 REAL,
            press_t_p90 REAL,
            press_c_p90 REAL,
            poss_g_p90 REAL,
            poss_p_p90 REAL,
            des_c_p100 REAL,
            passe_dec_p90 REAL,
            jg_ar_t_p90 REAL,
            cab_g_p100 REAL,
            int_p90 REAL,
            alivios_p90 REAL,
            ass_p90 REAL,
            bloqueios_p90 REAL,
            cab_dec_p90 REAL,
            cab_g_p90 REAL,
            cab_p_p90 REAL,
            cruz_c_p90 REAL,
            cruz_t_p90 REAL,
            des_dec_p90 REAL,
            fintas_p90 REAL,
            passe_prog_p90 REAL,
            passe_c_p100 REAL,
            xA_p90 REAL,
            npxG_p90 REAL,
            grandes_chances REAL,
            cruz_c_p100 REAL,
            gk_xG_def_p90 REAL,
            gk_xG_def REAL,
            xA REAL,
            gk_def_p90 REAL,
            gk_pen_def_p100 REAL,
            des_g_p90 REAL,
            id_temporada REAL,
            preco_min REAL,
            preco_max REAL,
            coef REAL,
            posicao_analise TEXT,
            salario_anual REAL,
            grandes_chances_p90 REAL,
            aval_cria REAL,
            np_chutes REAL,
            np_chutes_p90 REAL,
            np_chutes_gol REAL,
            np_chutes_gol_p90 REAL,
            np_chutes_gol_p100 REAL,
            xG_p90 REAL,
            npG REAL,
            npG_p90 REAL,
            conv_p100 REAL,
            npG_ae REAL,
            conv_penal_p100 REAL,
            npxG_per_np_chute REAL,
            xPnpG_p90 REAL,
            pnpG_p90 REAL,
            aval_fin REAL,
            aof_p90 REAL,
            faltas_sofridas_p90 REAL,
            erros_decisivos_p90 REAL,
            gk_def_dif_p90 REAL,
            gk_def_segu_p90 REAL,
            gk_def_desv_p90 REAL,
            des_t_p90 REAL,
            duel_t_p90 REAL,
            duel_g_p90 REAL,
            rtg_duel REAL,
            adef_t_p90 REAL,
            adef_c_p90 REAL,
            rtg_adef REAL,
            rtg_jg_ar REAL,
            rtg_des REAL,
            rtg_rec_bola REAL,
            aval_def REAL,
            source TEXT,
            PRIMARY KEY (id, id_temporada)
            );
            """
        
        try:
            cur.execute(scheme)
            self._conn.commit()
        except Exception as e:
            print(f"{e}: Falha ao criar tabela.")
            self._conn.rollback()
    
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
        