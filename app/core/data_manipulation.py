from typing import List, Union, Sequence

import pandas as pd
import re
import numpy as np
from pandas.api.typing import NAType
# from .files_utils import get_selected_files_names, get_file_extension, get_selected_files_paths

from data_preprocessing import (
                                    _initialize_dataframe,
                                    _drop_fm_dataframe_columns,
                                    _normalize_values,
                                    _str_to_numeric_values,
                                    _fillna_with_default,
                                    _replace_hyphen_with_zero,
                                    _create_new_position_column,
                                    _add_custom_metrics_columns,
                                    _validate_path,
                                    _get_season,
                                    _set_reputation
                                    
                                    # _rename_columns_names,
                                    # _reorganize_columns_df,
                                    )

pd.set_option('future.no_silent_downcasting', True)


def fm_create_dataframe(path:str) -> pd.DataFrame: 
    
    #1. Carregar arquivo para criação do dataframe e criar id da temp dos dados
    
    #1.1 Validar nome do arquivo
    if _validate_path(path):
        df = _initialize_dataframe(path)
    else:
        raise Exception('Arquivo inválido. Seguir padrão: xxxx_20xx.ext')


    #1.2 Pegar temporada do dado
    ID_SEASON = _get_season(path)
    
    #1.3 Criar coluna com id da temporada
    
    df['id_temporada'] = ID_SEASON # type: ignore
    
    # 2. Limpeza estutural e renomeaçao das colunas importadas    
    
    COLUMNS_FOR_DROP = [
        'Preço Exigido',
        'Inf',
        '% Remates',
        '% Cr T',
        'Conv %',
        'Crz T/90',
        'Fls',
        'FL/90',
        'Fj',
        'Gls/90',
        'Golos fora da área',
        'Op C/90',
        'PC',
        'Peso',
        'Remates fora da área/90',
        'Rems Bloq/90',
        'Sprints/90',
        'xG AcE',
        'xG/90',
        'xG/remate',
        'Amr',
        'Vermelhos',
        '% Dfp',
        'Valor',
        'PC/90',
        'Base',
        ]
    COLUMNS_FOR_RENAME = {
    '% Passe':'passe_c_p100',
    '% de Pen. Def.':'gk_pen_def_p100',
    'Altura':'altura',
    'Alí/90':'alivios_p90',
    'Assis/90':'ass_p90',
    'Ast':'ass',
    'Blq/90':'bloqueios_p90',
    'CC-JA %':'cruz_c_p100',
    'CC-JA/90':'cruz_c_p90',
    'CT-JA/90':'cruz_t_p90',
    'Cab %':'cab_g_p100',
    'Cab Dec/90':'cab_dec_p90',
    'Cab G/90':'cab_g_p90',
    'Cab P/90':'cab_p_p90',
    'Cl Med':'nota_med',
    'Clube':'clube',
    'Defesas/90':'gk_def_p90',
    'Des Dec/90':'des_dec_p90',
    'Des/90':'des_g_p90',
    'Dfa':'gk_def_desv',
    'Dft':'gk_def_dif',
    'Divisão':'divisao',
    'Ds':'gk_def_segu',
    'Expira':'final_contrato',
    'Fls':'faltas_sof',
    'Fnt/90':'fintas_p90',
    'Gl Err':'erro_chave',
    'Gls':'gols',
    'HdJ':'motm',
    'IDU':'id',
    'Idade':'idade',
    'Int/90':'int_p90',
    'JAr T/90':'jg_ar_t_p90',
    'Jogos':'partidas',
    'M Des':'des_c_p100',
    'Mins':'minutos',
    'Nac':'nac',
    'Nome':'nome',
    'OCG':'grandes_chances',
    'PD-JC/90':'passe_dec_p90',
    'Passes Pr/90':'passe_prog_p90',
    'Pens':'penaltis_batidos',
    'Pens M':'penaltis_conv',
    'Personalidade':'person',
    'Posição':'posicao',
    'Poss Con/90':'poss_g_p90',
    'Poss Perd/90':'poss_p_p90',
    'Pr C/90':'press_c_p90',
    'Pr T/90':'press_t_p90',
    'Preço Exigido':'preco',
    'Ps A/90':'passe_t_p90',
    'Ps C/90':'passe_c_p90',
    'Pé Preferido': 'melhor_pe',
    'Rem %':'chutes_gol',
    'Remt/90.1':'chutes_gol_p90',
    'Remates':'chutes',
    'Remt/90':'chutes_p90',
    'Salário':'salario',
    'Sem golos sofridos':'gk_sg',
    'Sof/90':'gk_gsof_p90',
    'T Desa':'des_t',
    'Valor Estimado':'valor_estimado',
    'xA':'xA',
    'xA/90':'xA_p90',
    'xG':'xG',
    'xG SP':'npxG',
    'xG SP/90':'npxG_p90',
    'xGD':'gk_xG_def',
    'xGP/90':'gk_xG_def_p90',    
    }
    
    #2.1 Deletar colunas sem usos
    df = _drop_fm_dataframe_columns(df, COLUMNS_FOR_DROP) # type: ignore
    
    #2.2 Renomear colunas para padrão da DB (snake_case)
    df.rename(columns=COLUMNS_FOR_RENAME, inplace=True)
        
    # 3. Normalização de valores (salarios, minutos, valor estimado e %)
    df = _normalize_values(df)
    df = _str_to_numeric_values(df)
    
    # 4. Tratamento de valores nulos e símbolos
    df = _fillna_with_default(df,'person','-')
    df = _replace_hyphen_with_zero(df)
    
    # 5. Criação de novas colunas e métricas
    df = _set_reputation(df)
    df = _create_new_position_column(df)
    df = _add_custom_metrics_columns(df)
    
    # 6. Preenchimentos de valores inf, -inf e NaN
    # df = df.replace([np.inf,-np.inf, np.nan], 0.00)

    # 7. Renomear algumas colunas 
    # df = _rename_columns_names(df)
       
    #8. Reorganizar ordem das colunas, agrupando por contexto de estastística
    # df = _reorganize_columns_df(df)
    
    return df
   
def fm_convert_str_to_numeric(df:pd.DataFrame) -> pd.DataFrame:
    
    list_of_columns = list(df.columns)
    list_of_columns.remove('partidas')
    list_of_columns.remove('preco_min')
    list_of_columns.remove('preco_max')

    
    for col in list_of_columns:
        if df[col].astype(str).str.match(r'^[+-]?(\d+\.?\d+?)$').any():
            try:
                df[col] = df[col].replace('-',0)
                df[col] = pd.to_numeric(df[col])
                
            except:
                pass
        
    return df
  
def fm_initialize_dataframe(filePath:str) -> pd.DataFrame|None:
    
    """ 
    Importa um arquivo do tipo HTML, CSV ou Excel e retorna um DataFrame do Pandas.

    Args:
        filePath (str): Caminho do arquivo a ser importado.
        

    Returns:
        pd.DataFrame: DataFrame do Pandas

    """
    
    name_file = get_selected_files_names(filePath)
    extension = get_file_extension(name_file)

    try:
        if extension == 'html':
            df_dados = pd.read_html(filePath, encoding = "utf-8", decimal = ".")  

            if df_dados:
                df_dados = df_dados[0]   
                
            else:
                df_dados =  None

        elif extension == 'csv':
            df_dados = pd.read_csv(filePath, sep = ";", decimal = ".")
            df_dados = df_dados.fillna(0)
 
        elif extension == 'excel':
            df_dados = pd.read_excel(filePath)
            
        else:
            df_dados =  None


    except FileNotFoundError:
        print(f'Erro: Caminho não encontrado')
        df_dados =  None
    
    except pd.errors.ParserError as e:
        print(f'Erro ao importar os dados: {e}')
        df_dados =  None

    except Exception as e:
        print(f'Erro: {e}')
        df_dados =  None

    # df_dados = df_dados.dropna(subset=['IDU'])
    # df_dados = df_dados.dropna(how='all')

    return df_dados

def fm_normalize_minutes_values(value:str|int) -> int:

    """
    Função para remover espaços em branco dos valores de minutos jogados no FM.

    Args:
        value: O valor dos minutos jogados, que pode ser uma string ou um inteiro.

    Returns:
        Os minutos sem espaços em branco e em formato de um número inteiro.

    Raises:
        TypeError: Se o valor de entrada não for uma string ou um inteiro.
        ValueError: Se o valor de entrada não puder ser convertido para um inteiro.

    Examples:
        FMnormalizeMinutes("90")
        90
        FMnormalizeMinutes("90'\xa0'")
        90
        FMnormalizeMinutes(45)
        45
        >FMnormalizeMinutes("abc")
        ValueError: Não foi possivel converter 'abc' para um inteiro.
    """


    if not isinstance(value, (str, int)):
        raise TypeError("O valor de entrada deve ser uma String ou Inteiro.")
    
    try:

        if isinstance(value, str):

            value = value.replace('\xa0', '').replace(' ', '').replace('-','0')
            value = int(value)
    
        if value < 0:

            raise ValueError ("O valor dos minutos jogados tem que ser maior que zero")
        
        return value

    except ValueError as e:
        raise ValueError (f"Não foi possivel converter '{value}' para um inteiro.") from e

def fm_normalize_wage_values(value: Union[str, int, float]) -> int:
    """Remove espaços em branco do campo Salario. altém de transformalo  em int
    retirando os sufixos e convertendo de str.

    Args:
        value (any): Valor do campo salario, podendo ser str ou int.

    Raises:
        TypeError: Se o valor de entrada nao for uma str ou um int.
        ValueError: Se os valores da str nao puderem ser normalizados e transformados
        em int.
        

    Returns:
        int: Retorna o valor do salário em formato int.
    """
  
    if not isinstance(value, (str, int)):
        raise TypeError("O valor de entrada deve ser uma String ou Inteiro.")  
    
    if isinstance(value, str):

        try:
            if value == 'N/D':
                return int(0)
            else:
                value = re.sub(r'(€ p/s|\xa0| )', '', value)
                return int(value)

        except ValueError as e:
            raise ValueError (f'Não foi possivel normarlizar o valor.') from e

    elif isinstance(value, int):
        return value

def fm_remove_percent_symbol_from_values(value:str|NAType|int) -> Union[int, float,str]:
    
    """_summary_

    Args:
        value (str): _description_

    Returns:
        int: _description_
    """
    if isinstance(value, NAType) or '-' in str(value):
        return 0
        
    else: 
        if isinstance(value, str) and value.find('%'):
            value = value.replace('%', '')
            return float(value) if bool(re.match(r'[0-9]+\.?[0-9]*', value)) else value
        
        else:
            return value
      
def fm_remove_percent_symbol_from_dataframe(df:pd.DataFrame) -> pd.DataFrame:
    
    """_summary_

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    
    df_nomesColunas = df.columns
    colunas_com_valores_percent = []

    for coluna in df_nomesColunas:
        if df[coluna].astype(str).str.contains('%').any():
            colunas_com_valores_percent.append(coluna)
    
    for coluna in colunas_com_valores_percent:
        df[coluna] = df[coluna].apply(fm_remove_percent_symbol_from_values)
    
        
    return df
    
def fm_create_extracted_position_column(df:pd.DataFrame) -> pd.DataFrame:
    
    df['posicao_analise'] = df['posicao'].apply(fm_extract_positions_from_values)
    return df 
    
def fm_extract_positions_from_values(value: str) -> list:
    
    """_summary_

    Returns:
        _type_: _description_
    """
    
    
    import re

    position_replacement = {'GR':'Goleiro',
        'D:C':'Zagueiro',
        'D:D':'Lateral-Direito',
        'D:E':'Lateral-Esquerdo',
        'DA:D':'Ala-Direito',
        'DA:E':'Ala-Esquerdo',
        'MD:C':'Volante',
        'M:C':'Meia-Central',
        'M:D':'Meia-Direito',
        'M:E':'Meia-Esquerdo',
        'MO:C':'Meia-Armador',
        'MO:D':'Ponta-Direito',
        'MO:E':'Ponta-Esquerdo',
        'PL:C':'Centroavante'}

    list_position_return = []
    shorten_position_list = []

    if value == 'GR':
        list_position_return = ['Goleiro']
        
    if value in (None, np.nan, '-', 0):
        list_position_return = []
        
    else:
        exported_position = re.sub(r"\s", '', value).split(',')

        for positions in exported_position:
            list_sides = re.findall(r'\((.*?)\)', positions)
        
            if not list_sides:
                list_sides = ['C']
    
        
            if '/' in positions:
                list_sides = list(list_sides[0])
                list_positions = re.sub(r'\((.*?)\)', "", positions).split('/')
            
                for position in list_positions:
                    for side in list_sides:
                        shorten_position_list.append(f'{position}:{side}')   
        
            else:
                list_sides = list(list_sides[0])
                position = re.sub(r'\((.*?)\)', "", positions)
                
                for side in list_sides:
                    shorten_position_list.append(f'{position}:{side}')
                
        for position in shorten_position_list:
            if position in position_replacement.keys():
                list_position_return.append(position_replacement[position])
            
            
        
    return list_position_return

def fm_unabbreviate_numeric_values(abbreviateValue:str) -> Sequence[Union[int,str]]:
    
    """_summary_

    Returns:
        _type_: _description_
    """
    
    import re


    unabbreviate_numeric_values: List[int] = []

    pattern = r'([0-9]+\.?[0-9]?)([mM]+)*'
    matches = re.findall(pattern, abbreviateValue)


    if matches:
        for match in matches:
            numeric_part = match[0]
            abbreviation = match[1]
        
            if numeric_part or numeric_part != '0':
                value = float(numeric_part)
            
                if abbreviation == 'm':
                    value = int(value*1_000)
                    unabbreviate_numeric_values.append(value)
                elif abbreviation == 'M':
                    value = int(value*1_000_000)
                    unabbreviate_numeric_values.append(value)
                elif not abbreviation:
                    unabbreviate_numeric_values.append(int(value))
        return unabbreviate_numeric_values
    
    else:
        return unabbreviate_numeric_values         
                     
def fm_normalize_estimated_values(value:str|int) -> Sequence[Union[int, str]]:
    """
    _summary_

    Returns:
        _type_: _description_

    """
    
    value = str(value)

    if 'Não' in value: 
            return 'NotSell'

    elif "Des" in value:
            return '-'
    else:
        return fm_unabbreviate_numeric_values(value)

def fm_split_max_min_estimated_values(value:Sequence[Union[int, str]]) -> pd.Series:
   
    if 'NotSell' in value or '-' in value:
        return pd.Series([value, value])

    else:
        min_price = (min(value))
        max_price = (max(value))
        
        return pd.Series([min_price, max_price])
 
def fm_create_max_min_estimated_column(df:pd.DataFrame) -> pd.DataFrame:
    
    df[['preco_min','preco_max']] = df['valor_estimado'].apply(fm_split_max_min_estimated_values)
    
    return df

def fm_create_new_parameters(df:pd.DataFrame) -> pd.DataFrame:

    #Criação do valor per90
    df['per90'] = (df['minutos']/90).round(2)
    
    #Tranformação de colulas de str para numericas
    df['penaltis_batidos'] = pd.to_numeric(df['penaltis_batidos'], errors='coerce')
    df['penaltis_conv'] = pd.to_numeric(df['penaltis_conv'], errors='coerce')
    
    #Substituição de colunas existentes
    
    df['ass_p90'] = (df['ass']/df['per90']).round(2)
    df['cruz_c_p100'] = ((df['cruz_c_p90']/(df['cruz_t_p90']))*100).round(0)

    #Criação de parâmetros iniciais
    df['salario_anual'] = (df['salario']*52.17).round(2)
    df['grandes_chances_p90'] = (df['grandes_chances']/df['per90']).round(2)
   
   
#================ Criação do parâmetro de analise das qualidades de criação de jogadas =================================
    
    df['aval_cria'] = (
        df['xA_p90']*0.70 + 
        ((df['passe_dec_p90']*0.30 + 
          df['grandes_chances_p90']*0.70))*0.30)*df['coef']
    
  
    df['aval_cria'] = df['aval_cria'].round(2)
   
    df = df.copy()
    
#================================= Taratamento de dados de finalização e gols =======================================================

    df['np_chutes'] = (df['chutes'] - df['penaltis_batidos'])
    df['np_chutes_p90'] = (df['np_chutes']/df['per90']).round(2)
    df['np_chutes_gol'] = (df['chutes_gol'] - df['penaltis_batidos'])
    df['np_chutes_gol_p90'] = (df['np_chutes_gol']/df['per90']).round(2)
    df['np_chutes_gol_p100'] = ((df['np_chutes_gol']/df['np_chutes'].where(df['np_chutes_p90'] >= 0.50, np.nan))*100).round(2)
    df = df.copy()
    
    df['xG'] = (df['npxG'] + df['penaltis_conv']*0.79).round(2) #xG
    df['xG_p90'] = (df['xG']/df['per90']).round(2) #xG/90
    df['npG'] = (df['gols'] - df['penaltis_conv']) #xG SP
    df['npG_p90'] = (df['npG']/df['per90']).round(2) #xG SP/90
    df['conv_p100'] = (df['npG']/df['np_chutes'].where(df['np_chutes'] != 0, np.nan)).round(2)
    df['npG_ae'] = (df['npG'] - df['npxG']).round(2)
    df['conv_penal_p100'] = ((df['penaltis_conv']/df['penaltis_batidos'].where(df['penaltis_batidos'] !=0, np.nan))*100).round(2)
    df['npxG_per_np_chute'] = (df['npxG']/df['np_chutes'].where(df['np_chutes'] != 0, np.nan)).round(2)
    df = df.copy()
    
    df['xPnpG_p90'] = (df['npxG_p90'] + df['xA_p90']).round(2)
    
    df['pnpG_p90'] = (df['npG_p90'] + df['ass_p90']).round(2)
    

    
    #====================== Criação dos dados de Analise das Finalizações ===========================================================
 
    p1 = 0.5
    p2 = 0.1
    p3 = 0.2
    p4 = 0.2
    
    df.loc[df['np_chutes_p90'] >= 0.50, 'aval_fin'] = (
        ((df['npxG_p90']/df['np_chutes_p90'])*p1 + 
        (df['np_chutes_gol_p90']/df['np_chutes_p90'])*p2 +
        df['conv_p100']*p3 + 
        (df['npG_p90']/df['np_chutes_p90'])*p4)*df['np_chutes_p90']).round(2)
    
    df['aval_fin'] = df['aval_fin'].replace([np.inf,-np.inf ], np.nan)
    df['aval_fin'] *= df['coef']
    
    df = df.copy()
    
#========================== Avaliações das ações ofensicas/criação ==========================================    
    
    df['aof_p90'] = (
        df['passe_prog_p90'] + 
        df['passe_dec_p90'] + 
        df['np_chutes_p90'] + 
        df['fintas_p90']).round(2)

#====================== Exclusão de colunas desnecessárias ===========================================    
    
    df = df.drop(columns='penaltis_batidos', errors='ignore')
    df = df.drop(columns='penaltis_conv', errors='ignore')
    df = df.drop(columns='chutes', errors='ignore')
    df = df.drop(columns='Remt/90', errors='ignore')
    df = df.drop(columns='chutes_gol', errors='ignore')
    df = df.drop(columns='Remt/90.1', errors='ignore')
    
    
    df = df.copy()
    
#======================== Criação de alguns parâmentrros per90 ===============================================


    df['faltas_sofridas_p90'] = (df['FC']/df['per90']).round(2)
    df = df.drop(columns='FC', errors='ignore')
    
    df['erros_decisivos_p90'] = (df['erro_chave'].astype(int)/df['per90']).round(3)
    df = df.drop(columns='erro_chave', errors='ignore')
    df = df.copy()


    df['gk_def_dif_p90'] = (df['gk_def_dif'].astype(int)/df['per90']).round(2)
    df = df.drop(columns='gk_def_dif', errors='ignore')
    
    df['gk_def_segu_p90'] = (df['gk_def_segu'].astype(int)/df['per90']).round(2)
    df = df.drop(columns='gk_def_segu', errors='ignore')

    df['gk_def_desv_p90'] = (df['gk_def_desv'].astype(int)/df['per90']).round(2)
    df = df.drop(columns='gk_def_desv', errors='ignore')
    
#================================ Criação e ajustes de parâmetros de ações defensivas ====================================================

    df['des_t_p90'] = (df['des_t']/df['per90']).round(2)
    
    df['duel_t_p90'] = (df['des_t_p90'] + df['press_t_p90']).round(2)
    
    df['duel_g_p90'] = (df['des_g_p90'] + df['press_c_p90']).round(2)
    
    df['rtg_duel'] = (df['duel_g_p90']/df['duel_t_p90'])*0.70 + np.tanh(df['duel_t_p90']/13)*0.30
    
    df = df.copy()

    df['adef_t_p90'] = (
        df['alivios_p90'] + 
        df['int_p90'] + 
        df['bloqueios_p90'] + 
        df['des_t_p90'] + 
        df['jg_ar_t_p90'] + 
        df['press_t_p90']).round(2) 
    
    df['adef_c_p90'] = (
        df['alivios_p90'] + 
        df['int_p90'] + 
        df['bloqueios_p90'] + 
        df['des_g_p90'] + 
        df['cab_g_p90'] + 
        df['press_c_p90']).round(2) 
    
    
    df['rtg_adef'] = (
        ((df['adef_c_p90']/df['adef_t_p90'])*0.75) + 
        (df['poss_g_p90']/df['adef_t_p90'])*0.15 + 
        np.tanh(df['adef_t_p90']/21)*0.10)
    
    
    df = df.copy()
    
#=========================================== Criação do parâmetro de avaliação defensivo ===========================================    
    
    df['rtg_jg_ar'] = (((df['cab_g_p100'])/100)*0.70
    + (df['cab_dec_p90']/df['cab_g_p90'])*0.20
    + np.tanh(df['jg_ar_t_p90']/7)*0.10).round(2)
    
    df['rtg_des'] = (((df['des_c_p100'])/100)*0.70 + 
                     (df['des_dec_p90']/df['des_g_p90'])*0.20 + 
                     np.tanh(df['des_t_p90']/3)*0.10).round(2)
    
    df['rtg_rec_bola'] = (
        (df['poss_g_p90']/df['adef_t_p90'])*0.70 + 
        (np.tanh(df['adef_t_p90'])/21)*0.30)
 
    
#=============================================== Criação do parâmetro de avaliação defensivo Global =====================================    
    
    df['aval_def'] = np.nan
    
    #Aplicação do coeficiente de ajustamento das ligas
    df['rtg_jg_ar'] = (df['rtg_jg_ar']*df['coef']).round(2)
    df['rtg_duel'] = (df['rtg_duel']*df['coef']).round(2)
    df['rtg_des'] = (df['rtg_des']*df['coef']).round(2)
    df['rtg_rec_bola'] = (df['rtg_rec_bola']*df['coef']).round(2)
    df['rtg_adef'] = (df['rtg_adef']*df['coef']).round(2)
    
    p1 = 0.25
    p2 = 0.10
    p3 = 0.10
    p4 = 0.25
    p5 = 0.30
    
    df['aval_def'] = (
        (((df['rtg_jg_ar']*p1) + 
          df['rtg_duel']*p2 + 
          (df['rtg_des'])*p3 + 
          (df['rtg_rec_bola'])*p4 + 
          df['rtg_adef']*p5))).round(2)
    
    df['aval_def'] = df['aval_def'].replace([np.inf,-np.inf ], np.nan)
    
#======================================  Exclusão de colunas desnecessárias==========================================================
   
    df = df.drop(columns='des_t', errors='ignore')
    df = df.drop(columns='per90', errors='ignore')

    
    
    df = df.copy()
    df.round(2)

    return df

def load_database():
    df = ""
    
    pass

def concat_positions(x:list | str) -> str:
    
    if isinstance(x, list):
        list_positions = x
        string_positions = ".".join(list_positions)
        return string_positions
    else:
        return x

