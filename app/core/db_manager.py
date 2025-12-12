from pathlib import Path
import sqlite3
import pandas as pd
from typing import List, Any
from .data_manipulation import concat_positions


def connect_db(db_name: str = 'data.db') -> sqlite3.Connection:
    
    # TODO: Criar verificação se a pasta que armazena a database está criadac
    
    root = Path(__file__).resolve().parents[2]
    path = root/'data'/'db'/db_name
    print(path)
    conn = sqlite3.connect(path)
    # conn = sqlite3.connect(r'D:\matheus\fmgendata\data\raw\db')
    
    
    
    return conn

def create_db(table_name: str = 'stats') -> None:
    
    conn = connect_db()
    cur = conn.cursor()
    
    scheme = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
    
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
        conn.commit()
    
    except Exception as e:
        print(f"{e}")
        conn.rollback()
        
    finally:
        if conn:
            conn.close()
            
def bulk_upsert(
    df: pd.DataFrame, 
    db_name: str = 'data.db', 
    table_name: str = 'stats') -> None:
    
    columns_df = list(df.columns)
    conn = connect_db(db_name=db_name)
    cur = conn.cursor ()
    
    if "posicao_analise" in columns_df:
        df['posicao_analise'] = df['posicao_analise'].apply(concat_positions)
        
    else:
        return
    
    placeholdeer = ", ".join(["?"]*len(columns_df))
    columns_joined = ", ".join(columns_df)
    update_columns = [f'{col}=excluded.{col}' for col in columns_df if col not in ("id", "id_temporada")]
    update_joined = ", ".join(update_columns)
    
    query = f""""?"
    INSERT INTO {table_name} ({columns_joined})
    VALUES ({placeholdeer})
    ON CONFLICT(id, id_temporada) DO UPDATE SET 
    {update_joined};
    """
    
    values = list(df.itertuples(index=False, name=None))
    
    try:
        cur.executemany(query, values)
        conn.commit()
    
    except Exception as e:
        print(f"{e}")
        
        if conn:
            conn.rollback()
    
    finally:
        if conn:
            conn.close()
        
def clear_table(table_name: str = ' stats') -> None:
    
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        
        cur.execute(f"DELETE FROM {table_name}")
        conn.commit()
        
    except Exception as e:
        print(f"{e}")
        
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()

def delete_rows(
    column_name: str,
    list_values: List[Any],
    table_name: str = 'stats') -> None:
    
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        
        placeholders = ", ".join(["?"*len(list_values)])
        
        query = f"""
        DELETE FROM {table_name}
        WHERE {column_name} in ({placeholders})
        """

        cur.execute(query, list_values)
        conn.commit()
        
    except Exception as e:
        print(f"{e}")
        
        if conn:
            conn.rollback()
            
    finally:
        if conn:
            conn.close()