from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

# CSV Header
df = pd.DataFrame(
    [],
    columns=[
        "Nome",
        "Nº Quartos",
        "Nº Casas de Banho",
        "Nº Estacionamentos",
        "Área Útil",
        "Área Terreno",
        "Certificado Energia",
        "Finalidade",
        "Tipo de Imóvel",
        "Estado",
        "Preço de Venda",
        "Distrito",
        "Concelho",
        "Freguesia",
        "Coordenadas",
        "Referência",
        "Infraestruturas",
        "Tipo de modalidade",
        "Zona",
        "Constituição",
        "Sistema de abastecimento de água",
        "Caixilharia das Janelas",
        "Climatização",
        "Domótica",
        "Edifício",
        "Garagem",
        "Vistas",
        "Exposição Solar",
        "Segurança",
    ],
)
df.to_csv("dados_era.csv", index=False, header=True)


def parseHTML(url):  # Parsing Html
    text_url = url

    text_content = requests.get(text_url).text

    text_soup = BeautifulSoup(text_content, "lxml")

    return text_soup


def imovelFeatures(soup):  # Extração das features da págima dum imóvel

    # ------ Nome ------
    # Método de webscraping: procurar tags 'span' com a classe 'openSansR t18 cinza33 line_height150'
    nome = soup.find("span", {"class": "openSansR t18 cinza33 line_height150"})
    # Estas 'class's tendem sempre a ser únicas, daí dar para ir direto ao conteúdo que se quer, mas verificar sempre isso

    # ------ Bloco de características principais ------
    # Método de webscraping: procurar tags 'ul' com a classe 'bloco-caracteristicas'
    bloco_caracteristicas = soup.find("ul", {"class": "bloco-caracteristicas"})

    features = {}

    # Método de webscraping: estas características estavam dentro de uma lista de 'span's, portanto tive que fazer uma abordagem diferente
    # O dicionário 'features' vai ter as caracteristicas que existem no bloco (a key será o "title" = spans[0]), e o 'value' vai ser o spans[1] associado a cada elemento
    if bloco_caracteristicas is not None:
        for li in bloco_caracteristicas.find_all("li"):
            key = li.find("span")["title"]
            value = li.find("span", {"class": "num"})
            if value is not None:
                features[key] = value.getText()

    icon_certificado = soup.find("span", class_="icon-imovel-certificado")
    if icon_certificado is not None:
        cert_energia = icon_certificado["title"]
    else:
        cert_energia = None

    # ------ Características adicionais ------
    # Método de webscraping: cada característica tinha um id associado, portanto estas características fui diretamente pelo id
    finalidade = soup.find(id="ctl00_ContentPlaceHolder1_lbl_imovel_show_finalidade")

    tipoDeImovel = soup.find(id="ctl00_ContentPlaceHolder1_lbl_imovel_show_tipo_imovel")

    estado = soup.find(id="ctl00_ContentPlaceHolder1_lbl_imovel_show_estado")

    preco_venda = soup.find(id="ctl00_ContentPlaceHolder1_lbl_imovel_show_preco_venda")

    distrito = soup.find(id="ctl00_ContentPlaceHolder1_lbl_imovel_show_distrito")

    concelho = soup.find(id="ctl00_ContentPlaceHolder1_lbl_imovel_show_concelho")

    freguesia = soup.find(id="ctl00_ContentPlaceHolder1_lbl_imovel_show_freguesia")

    ref = soup.find(id="ctl00_ContentPlaceHolder1_lbl_imovel_show_ref")

    # ------ Bloco de características extra ------
    # Método de webscraping: procurar tags 'div' com a classe 'imovel_show_list_caracteristicas box'
    box_caract = soup.find_all("div", {"class": "imovel_show_list_caracteristicas box"})

    # Método de webscraping: (semelhante ao método das características principais)
    for item in box_caract:
        key = item.find("span", {"class": "caracteristicas_titulo_nome"})
        value = item.find("span", {"class": "caracteristicas_descricao"})
        features[key.getText()] = value.getText()

    # ------ Coordenadas geográficas ------
    mapa_holder = soup.find("div", class_="mapa-holder")

    mapa_img = mapa_holder.find("img", class_="img_mapa", onclick=True)

    coordinates = re.sub(r".*query=(.*?)\'.*", r"\1", mapa_img["onclick"])

    # ------ Adicionar a informação extraída ao csv ------
    obj = df.append(
        {
            "Nome": nome.text,
            "Nº Quartos": features.get("Quartos", None),
            "Nº Casas de Banho": features.get("C. Banho", None),
            "Nº Estacionamentos": features.get("Estacionamento", None),
            "Área Útil": features.get("Área Útil", None),
            "Área Terreno": features.get("Área Terreno", None),
            "Certificado Energia": cert_energia,
            "Finalidade": finalidade.text,
            "Tipo de Imóvel": tipoDeImovel.text,
            "Estado": estado.text,
            "Preço de Venda": preco_venda.text,
            "Distrito": distrito.text,
            "Concelho": concelho.text,
            "Freguesia": freguesia.text,
            "Coordenadas": coordinates,
            "Referência": ref.text,
            "Infraestruturas": features.get("Infraestruturas", None),
            "Tipo de modalidade": features.get("Tipo", None),
            "Zona": features.get("Zona", None),
            "Constituição": features.get("Geral", None),
            "Sistema de abastecimento de água": features.get("Água", None),
            "Caixilharia das Janelas": features.get("Caixilharia", None),
            "Climatização": features.get("Climatização", None),
            "Domótica": features.get("Domótica", None),
            "Edifício": features.get("Edifício", None),
            "Garagem": features.get("Garagem", None),
            "Vistas": features.get("Vistas", None),
            "Exposição Solar": features.get("Exposição Solar", None),
            "Segurança": features.get("Segurança", None),
        },
        ignore_index=True,
    )

    obj.to_csv("dados_era.csv", mode="a", header=False, index=False)


def main():

    i = 1

    while 1:

        # Final das páginas
        if i == 43:
            break

        # Url das páginas da 'Era.pt', aceder num ciclo às páginas existentes
        htmlBraga = f"https://www.era.pt/imoveis/comprar/-/braga/braga?pg={i}"

        print(htmlBraga)

        # Realizar o parsing da página associada ao iterador do ciclo
        soup = parseHTML(htmlBraga)

        # Encontrar o link de cada imóvel presente na página, através do id associado
        # 're.compile' para utilizar regex, precisei porque o que diferenciava os ids eram os números presentes no id, tipo:
        # "ctl00_ContentPlaceHolder1_DataList_imoveis_ctl00_hpl_img_imovel"
        # "ctl00_ContentPlaceHolder1_DataList_imoveis_ctl01_hpl_img_imovel"
        # então '[0123456789]*' trata disso
        # 'href=True' faz com que depois seja possível aceder a esse atributo, o que vai acontecer já em baixo
        table = soup.find_all(
            id=re.compile(
                "ctl00_ContentPlaceHolder1_DataList_imoveis_ctl[0123456789]*_hpl_img_imovel"
            ),
            href=True,
        )

        # Para cada imóvel da página, aceder ao href e adicionar 'https://www.era.pt' no início para o url ficar a funcionar
        for tableCode in table:
            tableCode["href"] = "https://www.era.pt" + tableCode["href"]

        # Para cada link do imóvel presente no imóvel, ir buscar as features associadas a esse através do método imovelFeatures(imovel)
        for tableCode in table:
            imovel = parseHTML(tableCode["href"])
            imovelFeatures(imovel)

        # Aumentar o iterador associado às páginas
        i = i + 1


main()
