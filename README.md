# Zoom.com.br Web Scraper

Este projeto é uma aplicação que automatiza a busca e análise de produtos no site Zoom.com.br. O script realiza pesquisas com diferentes filtros de ordenação, coleta informações sobre os produtos e gera rankings para ajudar na decisão de compra.

## Funcionalidades

- Realiza buscas no site http://www.zoom.com.br
- Coleta dados de produtos com três filtros diferentes:
  - Mais relevante
  - Menor preço
  - Melhor avaliado
- Analisa as primeiras 3 páginas de resultados para cada filtro
- Identifica os produtos que aparecem com maior frequência nos resultados
- Cria um ranking dos produtos mais recorrentes
- Extrai detalhes dos 5 melhores produtos do ranking
- Salva os resultados em arquivos JSON e CSV para fácil análise

## Requisitos

- Python 3.6+
- Selenium 4.15.2
- Chrome/Chromium (navegador)

## Instalação

1. Crie e ative um ambiente virtual:
```
python3 -m venv .venv
source .venv/bin/activate  # No Linux/Mac
# ou
.venv\Scripts\activate  # No Windows
```

2. Instale as dependências:
```
pip install -r requirements.txt
```

## Uso

1. Ative o ambiente virtual (se ainda não estiver ativo)
2. Execute o script principal:
```
python src/zoom_scraper.py
```
3. O script irá buscar por "iphone" automaticamente
4. Aguarde o processo de coleta e análise
5. Os resultados serão salvos no diretório `resultados/`

## Arquivos de Saída

O script gera os seguintes arquivos na pasta `resultados/`:

- `produtos_mais_frequentes.csv`: Os 5 produtos mais frequentes em formato CSV
- `ranking_completo.csv`: Ranking completo de todos os produtos encontrados em formato CSV
- `top5_produtos_detalhes.csv`: Detalhes dos 5 melhores produtos em formato CSV
- `ranking_completo.json`: Ranking completo de todos os produtos em formato JSON
- `top5_produtos_detalhes.json`: Detalhes dos 5 melhores produtos em formato JSON

## Estrutura do código

O código está organizado em funções principais:

- `fechar_popups()`: Lida com popups de cookies e notificações no site
- `coletar_produtos()`: Extrai informações dos produtos na página atual
- `navegar_paginas()`: Navega entre páginas e coleta os produtos
- `executar_busca()`: Realiza a busca com um filtro específico

## Fluxo de Execução

1. Configuração do navegador Chrome
2. Busca por "iphone" com três filtros diferentes (Mais relevante, Menor preço, Melhor avaliado)
3. Coleta os dados dos produtos em cada filtro
4. Contabiliza os produtos que aparecem com maior frequência
5. Salva os rankings e detalhes em formatos CSV e JSON

## Observações

- O script lida automaticamente com popups de cookies e notificações no site
- Por padrão, o navegador Chrome é exibido durante a execução (modo não-headless)
- Os arquivos de resultados incluem o nome do produto, frequência, preço e link

## Limitações

- O site pode mudar sua estrutura, o que pode exigir atualizações no script
- O script pode ser afetado por alterações na interface do site ou novas camadas de proteção contra automação
- Alguns produtos podem não ter informações completas devido à estrutura da página
