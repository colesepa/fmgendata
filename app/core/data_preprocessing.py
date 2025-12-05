import pandas as pd
import re
import data_manipulation as dm
import json
import numpy as np
from unidecode import unidecode

# def _initialize_fm_dataframe(path:str|None = None) -> pd.DataFrame:
    
#     if path is None:
#         files = get_selected_files_paths()
#         path = files[0]
        
#     df = dm.fm_initialize_dataframe(path)
    
#     file_name = get_selected_files_names(path)
#     season = re.search(r'([0-9]+)', file_name)
    
#     if season:
#         df['id_temporada'] = int(season.group(1))
#     else:
#         raise ImportError('O nome do arquivo importado não é valido. O nome deve ser xxxx_2024.xxx')
    
#     return df

def _initialize_dataframe(path:str) -> pd.DataFrame|None:
    
    try:
        dados = pd.read_html(path, encoding='utf-8', decimal='.')
        if dados:
            df = dados[0]
            df.dropna(how='all', inplace=True)
            return df
        
    except Exception as e:
        print(f'Erro: {e}')

def _drop_fm_dataframe_columns(df: pd.DataFrame, columns:list) -> pd.DataFrame:
    
    # df = df.drop(columns=[col for col in columns if col in df.columns], errors='ignore')
    for col in columns:
        if col in df.columns:
            try:
                df = df.drop(columns=col)
            except:
                raise KeyError(print(f'Erro ao apagar a coluna: {col}'))
    
    return df

def _normalize_values(df:pd.DataFrame) -> pd.DataFrame:
    
    if 'salario' in df.columns:
        df['salario'] = df['salario'].apply(dm.fm_normalize_wage_values)
        
    if 'minutos' in df.columns:    
        df['minutos'] = df['minutos'].apply(dm.fm_normalize_minutes_values)
    
    if 'valor_estimado' in df.columns:
        df['valor_estimado'] = df['valor_estimado'].apply(dm.fm_normalize_estimated_values)
        df = dm.fm_create_max_min_estimated_column(df)
        df = df.drop(columns='valor_estimado', errors='ignore')
        
    df = dm.fm_remove_percent_symbol_from_dataframe(df)
    
    return df        
        
def _str_to_numeric_values(df:pd.DataFrame) -> pd.DataFrame:
    
    return dm.fm_convert_str_to_numeric(df) 
      
def _fillna_with_default(df: pd.DataFrame, column: str | list |tuple , default_value:any) -> pd.DataFrame:
    
    """
    Preenche valores nulos nas colunas especificadas com um valor padrão.

    Args:
        df (pd.DataFrame): DataFrame que será modificado.
        column (str | list | tuple): Nome da coluna, lista ou tuple de colunas a serem preenchidas.
        default_value (any): Valor que será usado para preencher os valores nulos.

    Returns:
        pd.DataFrame: DataFrame com os valores nulos preenchidos.
    """
    
    if isinstance(column, (list, tuple)):
        for col in column:
            if col in df.columns:
                df[col] = df[col].fillna(default_value)
                
    else:
        if column in df.columns:
            df[column] = df[column].fillna(default_value)
                
    return df

def _replace_hyphen_with_zero(df:pd.DataFrame) -> pd.DataFrame:
    
    df = df.replace('-', 0)
    df['person'] = df['person'].replace(0,'-')
                
    return df

def _create_new_position_column(df:pd.DataFrame) -> pd.DataFrame:
    
    df = dm.fm_create_extracted_position_column(df)
    
    return df

def _add_custom_metrics_columns(df:pd.DataFrame) -> pd.DataFrame:
    
    df = dm.fm_create_new_parameters(df)
    
    return df

def _set_reputation(df:pd.DataFrame) -> pd.DataFrame:
    
    with open('ligas.json', "r", encoding="utf-8") as f:
        data = json.load(f)
        
    df = df    
    df_ligas = pd.DataFrame(data['ligas'])
    
    coef_map = df_ligas.set_index('nome')['coeficiente'].to_dict()
    ligas_cadastradas = list(df_ligas['nome'].unique())
    
    
    df['coef'] = df['divisao'].apply(lambda x: round(coef_map[unidecode(x)], 2) if unidecode(x) in ligas_cadastradas else np.nan)
                                    
    return df
   



"""def _rename_columns_names(df:pd.DataFrame) -> pd.DataFrame:

    names_columns_replace = {
    'IDU': 'id_unico', 
    'Nome': 'nome', 
    'Nac': 'nacionalidade', 
    'Idade': 'idade', 
    'Altura': 'altura', 
    'Peso': 'peso', 
    'Posição': 'posicao', 
    'Pé Preferido': 'pe_preferido', 
    'Personalidade': 'personalidade', 
    'Clube': 'clube_atual', 
    'Divisão': 'divisao_atual', 
    'Salário': 'salario', 
    'Expira': 'final_do_contrato', 
    'Jogos': 'partidas_jogadas', 
    'Mins': 'minutos', 
    'Cl Med': 'nota_media', 
    'HdJ': 'homem_do_jogo', 
    'Amr': 'cartoes_amarelos', 
    'Vermelhos': 'cartoes_vermelhos', 
    'Ast': 'assistencias', 
    'Gls': 'gols', 
    'xA': 'assistencias_esperadas', 
    'xA/90': 'assistencias_esperadas_p90', 
    'Gls/90': 'gols_p90',
    'xG AcE': 'gols_acima_do_esperado', 
    'Remates fora da área/90': 'chutes_de_fora_da_area_p90', 
    'Golos fora da área': 'gols_de_fora_da_area_p100', 
    'FC': 'faltas_sofridas', 
    'Fls': 'faltas_cometidas', 
    'Pens': 'penaltis_batidos', 
    'Pens M': 'penaltis_convertidos', 
    'Remates': 'chutes_totais',
    'Remt/90': 'chutes_p90', 
    'Rem %': 'chutes_no_gol', 
    'Remt/90.1': 'chutes_no_gol_p90', 
    'Conv %': 'taxa_de_conversao_p100', 
    'xG/remate': 'gols_esperados_por_chute', 
    'Ps A/90': 'passes_tentados_p90', 
    'Ps C/90': 'passes_completados_p90', 
    'PD-JC/90': 'passes_decisivos_p90', 
    '% Passe': 'acerto_de_passes_p100', 
    'Passes Pr/90': 'passes_longos_p90', 
    'OCG': 'oportunidades_de_gols_criadas', 
    'CT-JA/90': 'cruzamentos_tentados_p90', 
    'CC-JA/90': 'cruzamentos_completos_p90', 
    '% Cr T': 'precisao_nos_cruzamentos_p100', 
    'Pr T/90': 'pressoes_tentadas_p90', 
    'Pr C/90': 'pressoes_completadas_p90', 
    'Poss Con/90': 'posse_ganha_p90', 
    'Poss Perd/90': 'posse_perdida_p90', 
    'T Desa': 'desarmes_tentados', 
    'Des/90': 'desarmes_feitos_p90', 
    'M Des': 'desarmes_feitos_p100', 
    'Des Dec/90': 'desarmes_decisivos_p90', 
    'Int/90': 'interceptcoes_feitas_p90', 
    'Alí/90': 'alivios_feitos_p90', 
    'Rems Bloq/90': 'bloqueio_de_chutes_p90',
    'Blq/90': 'bloqueios_de_acoes_do_adversario_p90', 
    'JAr T/90': 'disputa_aerea_tentadas_p90', 
    'Cab G/90': 'cabeceios_ganhos_p90', 
    'Cab P/90': 'cabeceios_perdidos_p90', 
    'Cab Dec/90': 'cabeceios_decisivos_p90', 
    'Cab %': 'cabeceios_ganhos_p100', 
    'Fnt/90': 'fintas_feitas_p90', 
    'Fj': 'impedimentos', 
    'Sprints/90': 'tiros_de_velocidade_p90',
    'Gl Err': 'erros_decisivos', 
    'Sem golos sofridos': 'jogos_sem_sofrer_gols', 
    'FL/90': 'sem_sofrer_gols_p90', 
    'Sof/90': 'gols_sofridos_p90',
    'xGD': 'gols_esperados_defendidos', 
    'xGP/90': 'gols_esperados_defendidos_p90',
    'Defesas/90': 'defesas_feitas_p90',
    'Dft': 'defesas_dificeis', 
    'Ds':'defesas_seguras',
    'Dfa': 'defesas_desviadas', 
    'xG SP': 'gols_esperados_sem_penaltis',
    'xG SP/90': 'gols_esperados_sem_penaltis_p90',
    '% de Pen. Def.': 'penaltis_defendidos_p100', 
    '% Dfp': 'taxa_de_defesas_previstas_p100'
    }
    
    df = df.rename(columns=names_columns_replace)

    return df """

"""def _reorganize_columns_df(df:pd.DataFrame) -> pd.DataFrame:
    
    list_sorted_columns = [
    
                        #1. INFORMAÇÕES GERAIS
                        
                        'id_unico',
                        'id_temporada',    
                        'nome',
                        'nacionalidade',
                        'idade',
                        'altura',
                        'peso',
                        'posicao',
                        'posicao_analise',
                        'pe_preferido',
                        'personalidade',
                        
                        #2. INFORMAÇÕES CONTRATUAIS/FINANCEIRAS
                        
                        'clube_atual',
                        'divisao_atual',
                        'salario',
                        'salario_anual',
                        'final_do_contrato',
                        'preco_minimo',
                        'preco_maximo',
                        
                        #3. INFORMAÇÕES GERAIS DE JOGO
                        
                        'partidas_jogadas',
                        'nota_media',
                        'homem_do_jogo',
                        'minutos',
                        
                        #4. RESUMO DAS AVALIAÇÕES GERAIS
                        
                        'avaliacao_defensiva',
                        'qualidade_das_criacoes',
                        'perigo_das_finalizacoes',
                        
                        #5. METRICAS DE AVALIAÇÃO DAS FINALIZAÇÕES/CHUTES/GOLS
                        
                        'gols',
                        'gols_p90',
                        'gols_esperados',
                        'gols_esperados_p90',
                        'gols_sem_penaltis',
                        'gols_sem_penaltis_p90',
                        'gols_esperados_sem_penaltis',
                        'gols_esperados_sem_penaltis_p90',
                        'gols_sem_penaltis_acima_do_esperado',
                        'gols_sem_penaltis_por_acoes_ofensivas',
                        'chutes_de_fora_da_area_p90',
                        'gols_de_fora_da_area_p100',
                        'chutes_sem_penaltis_p90', #Chutes Gerais
                        'chutes_no_gol_sem_penalti_p90', #Chutes enquadrados no alvo
                        'gols_esperados_sem_penalti_por_chutes_sem_penalti',
                        'taxa_de_chutes_no_gol_p100', #Porcentagem de Chutes totais que foram no alvo
                        'taxa_de_conversao_de_gols_p100', #Porcentagem de Chutes enquadrados que viraram gols
                        'conversao_de_penaltis_p100',
                        'participacoes_em_gols_sem_penaltis_p90',
                        'participacoes_esperadas_em_gols_sem_penaltis_p90',
                        'minutos_para_marcar_gols_sem_penaltis',
                        'minutos_para_participar_gols_sem_penaltis',
                        
                        #6. METRICAS DE AVALIAÇÃO DAS CRIAÇÕES/PASSES/CRUZAMENTOS
                        
                        'assistencias',
                        'assistencias_p90',
                        'assistencias_esperadas',
                        'assistencias_esperadas_p90',
                        'passes_tentados_p90',
                        'passes_completados_p90',
                        'acerto_de_passes_p100',
                        'passes_decisivos_p90',
                        'passes_longos_p90',
                        'cruzamentos_tentados_p90',
                        'cruzamentos_completos_p90',
                        'cruzamentos_completos_p100',
                        'grande_chances_criadas_p90',
                        'oportunidades_criadas_por_acoes_ofensivas',
                        'assistencias_por_acoes_ofensivas',
                        'fintas_feitas_p90',
                        'acoes_ofensivas_p90',
                        'faltas_sofridas_p90',
                        
                        #7. METRICAS DE AVALIAÇÃO DAS AÇÕES DEFENSIVAS
                        
                        'rating_das_acoes_defensivas',
                        'rating_dos_duelos_no_chao',
                        'rating_dos_desarmes',
                        'rating_jogo_aereo',
                        'pressao_efetiva',
                        'posse_ganha_por_pressao_feita',
                        'duelos_no_chao_ganhos_p90',
                        'acoes_defensivas_completas_p90',
                        'posse_ganha_p90',
                        'pressoes_completadas_p90',
                        'desarmes_feitos_p90',
                        'cabeceios_ganhos_p90',
                        'cabeceios_decisivos_p90',
                        'desarmes_decisivos_p90',
                        'bloqueios_de_acoes_do_adversario_p90',
                        'bloqueio_de_chutes_p90',
                        'interceptcoes_feitas_p90',
                        'alivios_feitos_p90',
                        'desarmes_feitos_p100',
                        'cabeceios_ganhos_p100',
                        'posse_ganha_por_perdida_p90',
                        'duelos_no_chao_tentados_p90',
                        'acoes_defensivas_tentadas_p90',
                        'disputa_aerea_tentadas_p90',
                        'desarmes_tentados_p90',
                        'cabeceios_perdidos_p90',
                        'pressoes_tentadas_p90',
                        'posse_perdida_p90',
                        'faltas_cometidas_p90',
                        'faltas_por_acoes_defensivas_completas_p90',
                        'erros_decisivos_p90',
                            
                        #8. METRICAS DE AVALIAÇÃO DAS AÇÕES DOS GOLEIROS
                        
                        'jogos_sem_sofrer_gols',
                        'gols_esperados_defendidos_p90',
                        'sem_sofrer_gols_p90',
                        'defesas_feitas_p90',
                        'defesas_dificeis_p90',
                        'defesas_seguras_p90',
                        'defesas_desviadas_p90',
                        'penaltis_defendidos_p100',
                        'gols_sofridos_p90',
                        
                        #9. OUTROS
                        
                        'cartoes_amarelos',
                        'cartoes_vermelhos',
                        'impedimentos',
                        'tiros_de_velocidade_p90'
                        ]
    
    list_sorted_columns = [col for col in list_sorted_columns if col in df.columns]

    df = df[list_sorted_columns]
    
    return df"""


def _validate_path(path:str) -> bool:
    
    pattern = r'^.+[_]*[0-9]{4}.{1}[a-zA-Z0-9]+$'
    
    if re.fullmatch(pattern=pattern, string=path):
        return True
    else:
        return False
    
def _get_season(path:str) -> int:
    
    pattern = r'^(?P<nome>.+_*)(?P<season>[0-9]{4})(?P<ext>.{1}[a-zA-Z0-9]+)'
    season = re.search(pattern, path).group('season')
    
    return int(season)

