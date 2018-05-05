# Webscraper to Gephi
Cria arquivos nodes.csv e edges.csv para o Gephi a partir de um arquivo csv gerado pelo Webscraper.

Este projeto nasceu a partir de outro projeto na UFRJ. Onde parcerias entre empresas da indústria de Bioplásticos foram mapeadas a partir de citações em patentes do USPTO e analisadas no software de mapeamento de redes Gephi[https://gephi.org/]. Essa é uma tarefa que envolve Big Data e, portanto, seria inviável realizar manualmente. 

Para a aquisição dos dados de citações entre as patentes, foi usada a extensão Web Scraper (http://webscraper.io/[http://webscraper.io/]) para fazer um scrape no site do USPTO. No entanto, os dados tinham que ser manipulados de forma que o Gephi pudesse lidar (criando arquivos nodes.csv para representar os atores e um arquivo edges.csv para representar a ligação entre eles) e para isso este projeto foi criado.

O script em Python recebe um arquivo csv de entrada gerado pelo Web Scraper e extrai as informações adequadas para arquivos nodes.csv e edges.csv, que podem ser importados diretamente no Gephi para desenhar a rede.


