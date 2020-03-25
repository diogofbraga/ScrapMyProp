from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

# CSV Header
df = pd.DataFrame([], columns=['Nome', 'Nº Quartos', 'Nº Casas de Banho', 'Nº Estacionamentos', 'Área Útil',
                               'Área Terreno', 'Finalidade', 'Tipo de Imóvel', 'Estado',
                               'Preço de Venda', 'Distrito', 'Concelho', 'Freguesia', 'Referência'])
df.to_csv('Era.csv', index=False, header=True)


def parseHTML(url):
    text_url = url

    text_content = requests.get(text_url).text

    text_soup = BeautifulSoup(text_content, 'lxml')

    return text_soup


def imovelFeatures(soup):

    # Nome
    nome = soup.find('span', {'class': 'openSansR t18 cinza33 line_height150'})

    # Bloco de características principais
    bloco_caracteristicas = soup.find('ul', {'class': 'bloco-caracteristicas'})

    principais = {}  # necessitei deste dicionário porque há alguns características principais que não existem sempre

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

    # Características adicionais
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

    obj = df.append({'Nome': nome.text, 'Nº Quartos': principais.get("quartos", None), 'Nº Casas de Banho': principais.get("casas_de_banho", None),
                     'Nº Estacionamentos': principais.get("estacionamento", None), 'Área Útil': principais.get("area_util", None),
                     'Área Terreno': principais.get("area_terreno", None), 'Finalidade': finalidade.text, 'Tipo de Imóvel': tipoDeImovel.text,
                     'Estado': estado.text, 'Preço de Venda': preco_venda.text, 'Distrito': distrito.text,
                     'Concelho': concelho.text, 'Freguesia': freguesia.text, 'Referência': ref.text}, ignore_index=True)
    obj.to_csv('Era.csv', mode='a', header=False, index=False)


def main():

    i = 1

    while(1):

        htmlBraga = "https://www.era.pt/imoveis/comprar/-/braga/braga?pg={0}".format(
            i)

        print(htmlBraga)

        if i == 48:
            break

        soup = parseHTML(htmlBraga)

        table = soup.find_all(id=re.compile(
            "ctl00_ContentPlaceHolder1_DataList_imoveis_ctl[0123456789]*_hpl_img_imovel"), href=True)

        for tableCode in table:
            tableCode['href'] = "https://www.era.pt" + tableCode['href']

        for tableCode in table:
            imovel = parseHTML(tableCode['href'])
            imovelFeatures(imovel)

        i = i+1


main()
