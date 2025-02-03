import pandas as pd

def prepare_df(parsed_items):
    # Creating a DataFrame for maintain compatibility with the rest of the code
    # Convert parsed_items to a list of dictionaries
    data = [{
        'titulo': item.titulo,
        'codigo': item.codigo,
        'tipo': item.tipo,
        'status': item.status,
        'responsavel': item.responsavel,
        'solicitante': item.solicitante,
        'data_criacao': item.data_criacao,
        'data_atualizacao': item.data_atualizacao,
        'data_resolucao': item.data_resolucao,
        'componente': item.componente,
        'descricao': item.descricao,
        'story_points': item.story_points,
        'sprints': ', '.join(item.sprints)
    } for item in parsed_items]

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Fill empty date fields with a placeholder date before conversion
    df['data_criacao'].replace('', '01/01/70 00:00:00', inplace=True)
    df['data_atualizacao'].replace('', '01/01/70 00:00:00', inplace=True)
    df['data_resolucao'].replace('', '01/01/70 00:00:00', inplace=True)

    # Convert date columns to datetime
    df['data_criacao'] = pd.to_datetime(df['data_criacao'], format='%d/%m/%y %H:%M:%S').dt.date
    df['data_atualizacao'] = pd.to_datetime(df['data_atualizacao'], format='%d/%m/%y %H:%M:%S').dt.date
    df['data_resolucao'] = pd.to_datetime(df['data_resolucao'], format='%d/%m/%y %H:%M:%S').dt.date

    return df

