from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

# Headers for request
headers = requests.utils.default_headers()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://google.pt',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-PT,pt;q=0.8,en;q=0.5,en-US;q=0.3'
}

# CSV Header
df = pd.DataFrame([], columns=['Nome', ...])
df.to_csv('dados_idealista.csv', index=False, header=True)


def parseHTML(url):  # Parsing Html
    text_url = url

    text_content = requests.get(
        text_url, headers=headers).text

    text_soup = BeautifulSoup(text_content, 'lxml')

    return text_soup


def imovelFeatures(soup):  # Extração das features da págima dum imóvel

    return


def main():

    i = 1

    while(1):
        # Url das páginas da 'Era.pt', aceder num ciclo às páginas existentes
        htmlIdealista = f"https://www.idealista.pt/comprar-casas/braga/pagina-{i}"

        print(htmlIdealista)

        # Final das páginas
        if i == 3:
            break

        # Realizar o parsing da página associada ao iterador do ciclo
        soup = parseHTML(htmlIdealista)

        # Encontrar o link de cada imóvel presente na página, visto que a página esta dividida em 'article' entao é só aceder a cada um e sacar o href
        # 'href=True' faz com que depois seja possível aceder a esse atributo, o que vai acontecer já em baixo

        container = soup.find_all('div', class_='item-info-container')

        table = []

        for item in container:
            table.append(
                item.find('a', class_='item-link', href=True))

        # print(table)

        # Para cada imóvel da página, aceder ao href e adicionar 'https://www.idealista.pt' no início para o url ficar a funcionar
        for tableCode in table:
            tableCode['href'] = "https://www.idealista.pt" + tableCode['href']
            # print(tableCode['href'])

        # Para cada link do imóvel presente no imóvel, ir buscar as features associadas a esse através do método imovelFeatures(imovel)
        # for tableCode in data:
        #    imovel = parseHTML(tableCode['href'])
        #    imovelFeatures(imovel)

        # Aumentar o iterador associado às páginas
        i = i+1


main()
