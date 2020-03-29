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
df.to_csv('dados_imovirtual.csv', index=False, header=True)


def parseHTML(url):  # Parsing Html
    text_url = url

    text_content = requests.get(
        text_url, headers=headers).text

    text_soup = BeautifulSoup(text_content, 'lxml')

    return text_soup


def imovelFeatures(soup):  # Extração das features da págima dum imóvel

    nome = soup.find('h1', class_="css-1ld8fwi").getText()
    print(nome)

    return


def main():

    i = 1

    while(1):
        # Url das páginas de apartamentos da 'Sapo.pt', aceder num ciclo às páginas existentes
        htmlBraga = f"https://www.imovirtual.com/comprar/braga/?search%5Bregion_id%5D=3&search%5Bsubregion_id%5D=36&page={i}"

        print(htmlBraga)

        # Final das páginas
        if i == 3:
            break

        # Realizar o parsing da página associada ao iterador do ciclo
        soup = parseHTML(htmlBraga)

        # Encontrar o link de cada imóvel presente na página, através do id associado
        container = soup.find_all(
            'article', id=re.compile("offer-item-ad_id.*"))

        # print(container)

        # Para cada link do imóvel presente no imóvel, ir buscar as features associadas a esse através do método imovelFeatures(imovel)
        for tableCode in container:
            # print(tableCode['data-url'])
            imovel = parseHTML(tableCode['data-url'])
            imovelFeatures(imovel)

        # Aumentar o iterador associado às páginas
        i = i+1


main()
