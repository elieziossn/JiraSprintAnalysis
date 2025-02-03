import pandas as pd

#retorna apenas os itens da sprint ativa
def filter_sprint_ativa(df, sprint_ativa):
    return df[df['sprints'].apply(lambda x: sprint_ativa in x)]

def prepare_sprints_df(sprint_dates):
    # Convert to DataFrame for easier manipulation
    sprint_df = pd.DataFrame.from_dict(sprint_dates, orient='index')
    sprint_df.index.name = 'sprint'
    sprint_df['start'] = pd.to_datetime(sprint_df['start'], format='%d/%m/%y').dt.date
    sprint_df['end'] = pd.to_datetime(sprint_df['end'], format='%d/%m/%y').dt.date
    return sprint_df

def prepare_feriados_df(feriados):
    feriados_df = pd.DataFrame.from_dict(feriados, orient='index')
    feriados_df.index.name = 'Feriado'
    feriados_df[0] = pd.to_datetime(feriados_df[0], format='%d/%m/%y').dt.date
    return feriados_df

def filter_items(df):
    # Filter for specific item types
    filtered_types = ['Tarefa', 'História', 'Spike', 'Problema']
    return df[df['tipo'].isin(filtered_types)]

def filter_subitems(df):
    filtered_types = ['Sub-tarefa-bug','Sub-tarefa-padrão']
    return df[df['tipo'].isin(filtered_types)]

def get_status_summary(df):
    # Filter items using the existing filter_items function
    items_df = filter_items(df)
    # Group by status and count
    status_summary = items_df['status'].value_counts().reset_index()
    status_summary.columns = ['Status', 'Quantidade']
    
    return status_summary

def simplify_status(status):
    #print(status)
    if status == 'Concluída':
        return 'Concluído'
    elif status == 'Backlog':
        return 'Backlog'
    elif status == 'In Test':
        return 'Testando'
    else:
        return 'Em Progresso'