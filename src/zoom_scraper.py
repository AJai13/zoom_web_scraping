from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from collections import Counter
from selenium.webdriver.support.ui import Select
import csv
import os
import json

# Configuração do navegador
options = Options()
options.add_argument("--start-maximized")

prefs = {
    "profile.default_content_setting_values.notifications": 2
}
options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome(options=options)
driver.get("https://www.zoom.com.br")

# Função para aceitar cookies / fechar popups
def fechar_popups():
    # cookies
    try:
        concordar_btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.PrivacyPolicy_Button__1RxwB"))
        )
        concordar_btn.click()
        print("Botão 'Concordar' clicado!")
    except Exception as e:
        print("Erro ao fechar popup de cookies.")
        print(e)

    # pesquisa de opinião
    try:
        pesquisa_btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//svg[contains(@class,'fb-h-6')]]"))
        )
        pesquisa_btn.click()
        print("Popup de pesquisa fechado!")
    except Exception as e:
        print("Erro ao fechar popup de pesquisa.")
        print(e)
        
    # botão de propaganda (botão X)
    try:
        botao_propaganda = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[./svg/path[@id='icon' and @d='M13.295.705a.997.997 0 0 0-1.41 0L7 5.59 2.115.705a.997.997 0 1 0-1.41 1.41L5.59 7 .705 11.885a.997.997 0 0 0 1.41 1.41L7 8.41l4.885 4.885a.997.997 0 1 0 1.41-1.41L8.41 7l4.885-4.885a.997.997 0 0 0 0-1.41Z']]"))
        )
        botao_propaganda.click()
        print("Popup de propaganda fechado!")
    except Exception as e:
        print("Erro ao fechar popup de propaganda.")
        print(e)


# Função para coletar os produtos de uma página
def coletar_produtos():
    produtos = []
    cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-card']")

    for card in cards:
        try:
            nome = card.find_element(By.CSS_SELECTOR, "h2[data-testid='product-card::name']").text
            preco = card.find_element(By.CSS_SELECTOR, "p[data-testid='product-card::price']").text
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            produtos.append((nome, preco, link))
        except Exception as e:
            print("Erro ao coletar informações do produto.")
            print(e)
            continue
    return produtos

# Função para navegar pelas páginas
def navegar_paginas(num_paginas=3):
    todos_produtos = []
    for i in range(num_paginas):
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        produtos = coletar_produtos()
        todos_produtos.extend(produtos)

        # Ir para próxima (até 3)
        try:
            next_button = driver.find_element(By.XPATH, f"//a[@aria-label='Página {i+2}']")
            driver.execute_script("arguments[0].click();", next_button)
        except Exception as e:
            print("Erro ao navegar para a próxima página.")
            print(e)
            break
    return todos_produtos

# Função de busca
def executar_busca(filtro="Mais relevante"):
    driver.get("https://www.zoom.com.br/")
    fechar_popups()

    # Caixa de busca
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "SearchInput_Input__W2vzU"))
    )
    search_box.clear()
    search_box.send_keys("iphone")
    search_box.send_keys(Keys.ENTER)


    # Aguarda resultados
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='product-card']"))
    )

    fechar_popups()

    select_element = driver.find_element(By.ID, "orderBy")
    select = Select(select_element)
    select.select_by_visible_text(filtro)

    time.sleep(5)

    # Coleta os produtos das 3 páginas
    return navegar_paginas(3)

# Rodando os 3 testes
produtos_relevancia = executar_busca("Mais relevante")
produtos_preco = executar_busca("Menor preço")
produtos_avaliado = executar_busca("Melhor avaliado")

# Contabilizar quais aparecem mais vezes
todos = produtos_relevancia + produtos_preco + produtos_avaliado
nomes = [p[0] for p in todos]
contagem = Counter(nomes)

# Exibir os que mais aparecem
print("Produtos mais frequentes nos 3 filtros:")
produtos_mais_frequentes = []

for nome, qtd in contagem.most_common(5):
    print(f"{nome} - apareceu {qtd} vezes")
    produtos_mais_frequentes.append({"nome": nome, "frequencia": qtd})

if not os.path.exists('../resultados'):
    os.makedirs('../resultados')

# Salvar os resultados em um arquivo CSV (top 5)
csv_path = '../resultados/produtos_mais_frequentes.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['nome', 'frequencia']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for produto in produtos_mais_frequentes:
        writer.writerow(produto)

# Ranking completo em CSV
csv_ranking_completo = '../resultados/ranking_completo.csv'
with open(csv_ranking_completo, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['nome', 'frequencia']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for nome, freq in contagem.most_common():
        writer.writerow({"nome": nome, "frequencia": freq})

# Detalhes completos dos 5 produtos mais frequentes
detalhes_top5 = []
nomes_top5 = [p["nome"] for p in produtos_mais_frequentes]

for produto in todos:
    nome, preco, link = produto
    if nome in nomes_top5 and not any(d["nome"] == nome for d in detalhes_top5):
        detalhes_top5.append({
            "nome": nome,
            "preco": preco,
            "link": link,
            "frequencia": contagem[nome]
        })

# Detalhes em CSV
csv_detalhes_path = '../resultados/top5_produtos_detalhes.csv'
with open(csv_detalhes_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['nome', 'preco', 'link', 'frequencia']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for produto in detalhes_top5:
        writer.writerow(produto)

# Resultados em formato JSON
json_path = '../resultados/ranking_completo.json'
with open(json_path, 'w', encoding='utf-8') as jsonfile:
    # Ranking completo
    ranking_completo = [{"nome": nome, "frequencia": freq} for nome, freq in contagem.most_common()]
    json.dump(ranking_completo, jsonfile, ensure_ascii=False, indent=4)

# Detalhes dos top 5 em JSON
json_detalhes_path = '../resultados/top5_produtos_detalhes.json'
with open(json_detalhes_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(detalhes_top5, jsonfile, ensure_ascii=False, indent=4)

print("\nArquivos salvos na pasta 'resultados':")
print(f"Top 5 produtos: {os.path.basename(csv_path)}")
print(f"Ranking completo: {os.path.basename(csv_ranking_completo)}")
print(f"Detalhes dos top 5 produtos: {os.path.basename(csv_detalhes_path)}")
print(f"Ranking completo (JSON): {os.path.basename(json_path)}")
print(f"Detalhes dos top 5 (JSON): {os.path.basename(json_detalhes_path)}")

driver.quit()
