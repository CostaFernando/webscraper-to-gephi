from services import convertWebscraperToGephi

webscraperFileFields= {
    'web-scraper-order': 0,
    'web-scraper-start-url': 1,
    'patent_link': 2,
    'patent_link-href': 3,
    'patent_date': 4,
    'patent_abstract': 5,
    'patent_number': 6,
    'patent_assignee': 7,
    'referenced_by_link': 8,
    'referenced_by_link-href': 9,
    'citator_link': 10,
    'citator_link-href': 11,
    'pagination': 12,
    'pagination-href': 13,
    'citator_patent_number': 14,
    'citator_date': 15
}
gephiNodesFileFields= ['Id', 'Label', 'patent_title', 'link', 'data', 'assignee', 'abstract']
gephiEdgesFileFields= ['Source', 'Target', 'Type', 'patent_number_of_citator', 'patent_number_of_cited', 'data']

webscraperFile= open('uspto_patent_citations.csv', 'r')

print('Iniciando a criação dos arquivos para o Gephi...')

convertWebscraperToGephi(webscraperFile, webscraperFileFields, gephiNodesFileFields, gephiEdgesFileFields)

print('Arquivos prontos para o Gephi!')
