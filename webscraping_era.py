from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

# CSV Header
df = pd.DataFrame([], columns=['Nome', 'Finalidade', 'Tipo de Imóvel', 'Estado',
                               'Preço de venda', 'Distrito', 'Concelho', 'Freguesia', 'Referência'])
df.to_csv('Era.csv', index=False, header=True)


def parseHTML(url):
    text_url = url
    # Fazer pedido GET para obter o objecto HTML em formato texto
    text_content = requests.get(text_url).text
    # Criar objeto BS, usando o lxml
    text_soup = BeautifulSoup(text_content, 'lxml')
    # Obter apenas o texto da pagina HTML, sem as tags deste
    return text_soup


def imovelFeatures(soup):

    nome = soup.find('span', {'class': 'openSansR t18 cinza33 line_height150'})

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

    obj = df.append({'Nome': nome.text, 'Finalidade': finalidade.text, 'Tipo de Imóvel': tipoDeImovel.text,
                     'Estado': estado.text, 'Preço de venda': preco_venda.text, 'Distrito': distrito.text,
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


# correr o script
main()
