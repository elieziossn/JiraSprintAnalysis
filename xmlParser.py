import xml.etree.ElementTree as ET
import pandas as pds

class Item:
    def __init__(self, titulo, codigo, tipo, status, responsavel, solicitante, data_criacao, data_atualizacao, data_resolucao, componente, descricao, story_points, sprints):
        self.titulo = titulo
        self.codigo = codigo
        self.tipo = tipo
        self.status = status
        self.responsavel = responsavel
        self.solicitante = solicitante
        self.data_criacao = data_criacao
        self.data_atualizacao = data_atualizacao
        self.data_resolucao = data_resolucao
        self.componente = componente
        self.descricao = descricao
        self.story_points = story_points
        self.sprints = sprints

def parse_item(item):
    titulo = item.find('title').text if item.find('title') is not None else ''
    codigo = item.find('key').text if item.find('key') is not None else ''
    tipo = item.find('type').text if item.find('type') is not None else ''
    status = item.find('status').text if item.find('status') is not None else ''
    responsavel = item.find('assignee').text if item.find('assignee') is not None else ''
    solicitante = item.find('reporter').text if item.find('reporter') is not None else ''
    componentes = [comp.text for comp in item.findall('component')]
    componente = ', '.join(componentes) if componentes else ''
    descricao = item.find('description').text if item.find('description') is not None else ''
    sprints = [sprint.text for sprint in item.findall('.//customfield[@key="com.pyxis.greenhopper.jira:gh-sprint"]/customfieldvalues/customfieldvalue')]

    data_criacao = item.find('created').text if item.find('created') is not None else ''
    data_atualizacao = item.find('updated').text if item.find('updated') is not None else ''
    data_resolucao = item.find('resolved').text if item.find('resolved') is not None else ''
    
    data_criacao = pds.to_datetime(data_criacao, format='%a, %d %b %Y %H:%M:%S %z').date() if data_criacao else None
    data_atualizacao = pds.to_datetime(data_atualizacao, format='%a, %d %b %Y %H:%M:%S %z').date() if data_atualizacao else None
    data_resolucao = pds.to_datetime(data_resolucao, format='%a, %d %b %Y %H:%M:%S %z').date() if data_resolucao else None

    # Find story points in customfields
    story_points = '0'
    for customfield in item.findall('customfields/customfield'):
        if customfield.find('customfieldname').text == 'Pontos da História':
            story_points = customfield.find('customfieldvalues/customfieldvalue').text
            break

    return Item(titulo, codigo, tipo, status, responsavel, solicitante, data_criacao, data_atualizacao, data_resolucao, componente, descricao, story_points, sprints)

def loadXml(file_path):
    # Carregar o arquivo XML
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Filtrar apenas as tags de nome "item"
    items = root.findall('.//item')

    # Parse all items into a list of Item objects
    parsed_items = [parse_item(item) for item in items]

    return parsed_items
