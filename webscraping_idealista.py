from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

# CSV Header
df = pd.DataFrame([], columns=['Nome', 'Nº Quartos', 'Nº Casas de Banho', 'Nº Estacionamentos', 'Área Útil',
                               'Área Terreno', 'Finalidade', 'Tipo de Imóvel', 'Estado',
                               'Preço de Venda', 'Distrito', 'Concelho', 'Freguesia', 'Referência'])
df.to_csv('dados_idealista.csv', index=False, header=True)


def parseHTML(url):  # Parsing Html
    text_url = url

    text_content = requests.get(text_url).text

    text_soup = BeautifulSoup(text_content, 'lxml')

    return text_soup


def imovelFeatures(soup):  # Extração das features da págima dum imóvel

    # ------ Nome ------
    # Método de webscraping: procurar tags 'span' com a classe 'openSansR t18 cinza33 line_height150'
    nome = soup.find('span', {'class': 'openSansR t18 cinza33 line_height150'})
    # Estas 'class's tendem sempre a ser únicas, daí dar para ir direto ao conteúdo que se quer, mas verificar sempre isso

    # ------ Bloco de características principais ------
    # Método de webscraping: procurar tags 'ul' com a classe 'bloco-caracteristicas'
    bloco_caracteristicas = soup.find('ul', {'class': 'bloco-caracteristicas'})

    principais = {}  # Necessitei deste dicionário porque há alguns características principais que não existem sempre

    # Método de webscraping: estas características estavam dentro de uma lista de 'span's, portanto tive que fazer uma abordagem diferente
    # O dicionário 'principais' vai ter as caracteristicas que existem no bloco (a key será o "title" = spans[0]), e o 'value' vai ser o spans[1] associado a cada elemento
    # Por exemplo, cada elemento da lista tem: '<li><span class="icon-imovel-quartos" title="Quartos"> </span><span class="num">3</span></li>'
    # Tenho que ir buscar os spans, neste caso: os "Quartos" e depois o "3", daí ter metido isto numa lista chamada 'spans'
    # O index 0 é o "Quartos" e o index 1 é o "3"
    if bloco_caracteristicas is not None:
        for li in bloco_caracteristicas.find_all('li'):
            spans = li.find_all('span')
            if spans[0]["title"] == "Quartos":
                principais["quartos"] = spans[1].getText()
            elif spans[0]["title"] == "C. Banho":
                principais["casas_de_banho"] = spans[1].getText()
            elif spans[0]["title"] == "Estacionamento":
                principais["estacionamento"] = spans[1].getText()
            elif spans[0]["title"] == "Área Útil":
                principais["area_util"] = spans[1].getText()
            elif spans[0]["title"] == "Área Terreno":
                principais["area_terreno"] = spans[1].getText()

    # ------ Características adicionais ------
    # Método de webscraping: cada característica tinha um id associado, portanto estas características fui diretamente pelo id
    finalidade = soup.find(
        id="ctl00_ContentPlaceHolder1_lbl_imovel_show_finalidade")

    tipoDeImovel = soup.find(
        id="ctl00_ContentPlaceHolder1_lbl_imovel_show_tipo_imovel")

    estado = soup.find(
        id="ctl00_ContentPlaceHolder1_lbl_imovel_show_estado")

    preco_venda = soup.find(
        id="ctl00_ContentPlaceHolder1_lbl_imovel_show_preco_venda")

    distrito = soup.find(
        id="ctl00_ContentPlaceHolder1_lbl_imovel_show_distrito")

    concelho = soup.find(
        id="ctl00_ContentPlaceHolder1_lbl_imovel_show_concelho")

    freguesia = soup.find(
        id="ctl00_ContentPlaceHolder1_lbl_imovel_show_freguesia")

    ref = soup.find(
        id="ctl00_ContentPlaceHolder1_lbl_imovel_show_ref")

    # Adicionar a informação extraída ao csv
    obj = df.append({'Nome': nome.text, 'Nº Quartos': principais.get("quartos", None), 'Nº Casas de Banho': principais.get("casas_de_banho", None),
                     'Nº Estacionamentos': principais.get("estacionamento", None), 'Área Útil': principais.get("area_util", None),
                     'Área Terreno': principais.get("area_terreno", None), 'Finalidade': finalidade.text, 'Tipo de Imóvel': tipoDeImovel.text,
                     'Estado': estado.text, 'Preço de Venda': preco_venda.text, 'Distrito': distrito.text,
                     'Concelho': concelho.text, 'Freguesia': freguesia.text, 'Referência': ref.text}, ignore_index=True)
    obj.to_csv('dados_era.csv', mode='a', header=False, index=False)


def main():

    i = 1

    while(1):
        # Url das páginas da 'Era.pt', aceder num ciclo às páginas existentes
        htmlIdealista = f"https://www.idealista.pt/comprar-casas/braga/pagina-{i}"

        print(htmlIdealista)

        # Final das páginas
        if i == 60:
            break

        # Realizar o parsing da página associada ao iterador do ciclo
        soup = parseHTML(htmlIdealista)

        # Encontrar o link de cada imóvel presente na página, visto que a página esta dividida em 'article' entao é só aceder a cada um e sacar o href
        # 'href=True' faz com que depois seja possível aceder a esse atributo, o que vai acontecer já em baixo

        for data in soup.find_all('div', class_='item-info-container'):
            for a in data.find_all('a'):
                print(a.get('href')) #for getting link
                print(a.text) #for getting text between the link
        

        # Para cada imóvel da página, aceder ao href e adicionar 'https://www.era.pt' no início para o url ficar a funcionar
        for tableCode in data:
            tableCode['href'] = "https://www.idealista.pt" + tableCode['href']
            print(tableCode['href'])

        # Para cada link do imóvel presente no imóvel, ir buscar as features associadas a esse através do método imovelFeatures(imovel)
        for tableCode in data:
            imovel = parseHTML(tableCode['href'])
            imovelFeatures(imovel)

        # Aumentar o iterador associado às páginas
        i = i+1


main()
