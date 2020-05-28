from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import time
import json

# Headers for request

# CSV Header
df = pd.DataFrame(
    [],
    columns=[
        "Nome",
        "Id",
        "Tipo de imóvel",
        "Preço",
        "Preço m/2",
        "Distrito",
        "Concelho",
        "Freguesia",
        "Rua",
        "Latitude",
        "Longitude",
        "Tipologia",
        "Nº Casas de Banho",
        "Área útil m/2",
        "Área bruta m/2",
        "Ano construção",
        "Certificado energético",
        "Armário",
        "Cozinha equipada",
        "Garagem box",
        "Gás canalizado",
        "Lareira",
        "Marquise",
        "Suite",
        "Varanda",
        "Vista de cidade",
        "Condição",
        "Despensa",
        "Arrecadação",
        "Porta blindada",
        "Video Porteiro",
        "Empreendimento",
        "Ar condicionado",
        "Elevador",
        "Estores elétricos",
        "Fibra ótica",
        "Pré-instalação de ar condicionado",
        "Terraço",
        "Área de terreno m/2",
        "Churrasco",
        "Árvores de fruto",
        "Sotão",
        "Cave",
        "Jardim",
        "Aquecimento central",
        "Caldeira",
        "Acessibilidade a pessoas com mobilidade condicionada",
        "Box 2 carros",
        "Detetor de gás",
        "Painéis solares",
        "Recuperação de calor",
        "Vista de campo/serra",
        "Box 1 carro",
        "Portaria",
        "Estacionamento",
        "Piso radiante",
        "Som ambiente",
        "Aspiração central",
        "Finalidade",
        "Tipo de terreno",
        "Acesso pavimentado",
        "Asfaltado",
        "Iluminação pública",
        "Zona arborizada",
        "Declive",
        "Ruína",
        "Alarme",
        "Furo de água",
        "Domótica",
        "Casa das máquinas",
        "Condomínio Fechado",
        "Parque infantil",
        "Piscina",
        "Piscina Privada",
        "Termoacumulador",
        "Garagem exterior",
        "Mobilado",
        "Hidromassagem/jacuzzi",
        "Quintal/horta",
        "Ginásio",
        "Kitchenette",
        "Vigilância/segurança",
        "Campo de ténis",
        "Segurança 24 horas",
        "Vedação",
        "Parqueamento (1 carro)",
        "Ligação a rede de água",
        "Ligação a rede de saneamento",
        "Ligação a rede elétrica",
        "Animais permitidos",
        "Parqueamento (2 carros)",
        "Cofre",
        "Vista de rio",
        "Nº divisões",
        "Tipo",
        "Pisos",
        "Com WC",
        "Montra",
        "Anexo habitacional",
        "Detetor de incêndio",
        "Detetor de Inundução",
        "Vista de cidade",
        "Área (m/2)",
        "Vista de mar",
        "Jacuzzi",
        "Património classificado",
        "Adaptada a mobilidade reduzida",
        "Com cozinha",
        "Imóvel de banca",
        "Vista de lago",
        "Fossa séptica",
        "Licensa de construção",
        "Acesso a veículos pesados",
        "Área administrativa",
        "Copa",
        "Recepção",
        "Refeitório",
        "Sala de reuniões",
        "Área florestal",
        "Hidromassagem",
        "Percurso de água",
        "Armazém",
        "Vista de Serra",
        "Adaptado a mobilidade reduzida",
        "Terra batida",
        "Video vigilância",
        "Espaço frigorífico",
        "Espaço para arrumação",
        "Casa de banho partilhada",
        "Poço",
        "Sótão",
        "Paisagem protegida",
    ],
)
df.to_csv("dados_imovirtual.csv", index=False, header=True)


def parseHTML(url):  # Parsing Html
    headers = requests.utils.default_headers()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0",
        # 'User-Agent': 'Windows NT 10.0; Win64; x64',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://google.pt",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "pt-PT,pt;q=0.8,en;q=0.5,en-US;q=0.3",
    }
    # proxies = {
    #    'http': 'http://192.168.1.9:51895',
    #    'https': 'https://192.168.1.9:51895',
    # }
    text_url = url

    text_content = requests.get(text_url, headers=headers).text
    # text_content = requests.get(text_url, headers=headers, proxies=proxies).text

    text_soup = BeautifulSoup(text_content, "lxml")

    return text_soup


def imovelFeatures(soup):  # Extração das features da págima dum imóvel

    nome = soup.find("h1", {"class": "css-1ld8fwi"})
    if nome is not None:
        nome = nome.text

    p = soup.find("div", {"class": "css-1vr19r7"})
    if p is not None:
        preco = re.match("[0123456789 ]+", p.getText())
        if preco is not None:
            preco = preco.group(0)
    else:
        preco = None

    pm2 = soup.find("div", {"class": "css-zdpt2t"})
    if pm2 is not None:
        precom2 = re.match("[0123456789 ]+", pm2.getText())
        if precom2 is not None:
            precom2 = precom2.group(0)
    else:
        precom2 = None

    propriedades = soup.find("div", {"class": "css-2fnk9o"})
    if propriedades is not None:
        prs = propriedades.find("ul")
        if prs is not None:
            pr = prs.find_all("li")

    ident = soup.find("div", {"class": "css-kos6vh"})
    if ident is not None:
        iden = ident.find("br")
        if iden is not None:
            ide = iden.previousSibling.split(": ")[1]
    else:
        ide = None

    jsonstr = soup.find("script", {"type":"application/json", "id": "server-app-state"})
    lat=None
    long=None
    if jsonstr is not None:
        jsonobj=json.loads(jsonstr.getText())
        if "initialProps" in jsonobj:
            if "data" in jsonobj["initialProps"]:
                if "advert" in jsonobj["initialProps"]["data"]:
                    if jsonobj["initialProps"]["data"]["advert"]["location"]["coordinates"]["latitude"] is not None and jsonobj["initialProps"]["data"]["advert"]["location"]["coordinates"]["longitude"] is not None:
                        lat = jsonobj["initialProps"]["data"]["advert"]["location"]["coordinates"]["latitude"]
                        long = jsonobj["initialProps"]["data"]["advert"]["location"]["coordinates"]["longitude"]
    else:
        jsonstrs= soup.find_all("script", {"type": "application/ld+json"})
        if jsonstrs is not None:
            for x in jsonstrs:
                jsonobj=json.loads(jsonstrs[x].getText())
                if jsonobj["@graph"][0]["geo"]["latitude"] is not None and jsonobj["@graph"][0]["geo"]["longitude"]:
                    lat = jsonobj["@graph"][0]["geo"]["latitude"]
                    long = jsonobj["@graph"][0]["geo"]["longitude"]

    features = {}

    if propriedades is not None:
        for li in pr:
            a = li.find("strong").getText()
            key = li.find("strong").previousSibling.lower()
            if " :" in key:
                key = key.replace(" :", "")
            elif ": " in key:
                key = key.replace(": ", "")
            if "área útil" in key:
                key = "área útil (m/2)"
            elif "área bruta" in key:
                key = "área bruta (m/2)"
            elif "área de terreno" in key:
                key = "área de terreno (m/2)"
            elif "área" in key:
                key = "área (m/2)"
            value = a
            if value is not None:
                features[key] = value

    local = soup.find("ul", {"class": "breadcrumb css-1ry41wf"})
    if local is not None:
        locais = local.find_all("li")
        if locais is not None:
            key = "Tipo de imóvel"
            value = locais[1].find("a").getText().split(" ")[0]
            features[key] = value
            key = "Distrito"
            value = locais[2].find("a").getText()
            features[key] = value
            key = "Concelho"
            value = locais[3].find("a").getText()
            features[key] = value
            key = "Freguesia"
            value = locais[4].find("a").getText()
            features[key] = value
            if len(locais) > 5:
                key = "Rua"
                value = locais[5].find("a")
                if value is not None:
                    features[key] = value.getText()

    caracteristicas = soup.find("div", {"class": "css-1bpegon"})
    if caracteristicas is not None:
        ul = caracteristicas.find("ul")
        for li in ul:
            key = li.getText().lower()
            if " :" in key:
                key = key.replace(" :", "")
            elif ": " in key:
                key = key.replace(": ", "")
            value = "True"
            features[key] = value

    obj = df.append(
        {
            "Nome": nome,
            "Id": ide,
            "Tipo de imóvel": features.get("Tipo de imóvel", None),
            "Preço": preco,
            "Preço m/2": precom2,
            "Distrito": features.get("Distrito", None),
            "Concelho": features.get("Concelho", None),
            "Freguesia": features.get("Freguesia", None),
            "Rua": features.get("Rua", None),
            "Latitude": lat,
            "Longitude": long,
            "Tipologia": features.get("tipologia", None),
            "Nº Casas de Banho": features.get("casas de banho", None),
            "Área útil m/2": features.get("área útil (m/2)", None),
            "Área bruta m/2": features.get("área bruta (m/2)", None),
            "Ano construção": features.get("ano de construção", None),
            "Certificado energético": features.get("certificado energético", None),
            "Armário": features.get("armário", None),
            "Cozinha equipada": features.get("cozinha equipada", None),
            "Garagem box": features.get("garagem (box)", None),
            "Gás canalizado": features.get("gás canalizado", None),
            "Lareira": features.get("lareira", None),
            "Marquise": features.get("marquise", None),
            "Suite": features.get("suite", None),
            "Varanda": features.get("varanda", None),
            "Vista de cidade": features.get("vista de cidade", None),
            "Condição": features.get("condição", None),
            "Despensa": features.get("despensa", None),
            "Arrecadação": features.get("arrecadação", None),
            "Porta blindada": features.get("porta blindada", None),
            "Video Porteiro": features.get("video porteiro", None),
            "Empreendimento": features.get("empreendimento", None),
            "Ar condicionado": features.get("ar condicionado", None),
            "Elevador": features.get("elevador", None),
            "Estores elétricos": features.get("estores elétricos", None),
            "Fibra ótica": features.get("fibra óptica", None),
            "Pré-instalação de ar condicionado": features.get(
                "pré-instalação de ar condicionado", None
            ),
            "Terraço": features.get("terraço", None),
            "Área de terreno m/2": features.get("área de terreno", None),
            "Churrasco": features.get("churrasco", None),
            "Árvores de fruto": features.get("árvores de fruto", None),
            "Sotão": features.get("sotão", None),
            "Cave": features.get("cave", None),
            "Jardim": features.get("jardim", None),
            "Aquecimento central": features.get("aquecimento central", None),
            "Caldeira": features.get("caldeira", None),
            "Acessibilidade a pessoas com mobilidade condicionada": features.get(
                "acessibilidade a pessoas com mobilidade condicionada", None
            ),
            "Box 2 carros": features.get("box 2 carros", None),
            "Detetor de gás": features.get("detector de gás", None),
            "Painéis solares": features.get("painéis solares", None),
            "Recuperação de calor": features.get("recuperação de calor", None),
            "Vista de campo/serra": features.get("vista de campo/serra", None),
            "Box 1 carro": features.get("box 1 carro", None),
            "Portaria": features.get("portaria", None),
            "Estacionamento": features.get("estacionamento", None),
            "Piso radiante": features.get("piso radiante", None),
            "Som ambiente": features.get("som ambiente", None),
            "Aspiração central": features.get("aspiração central", None),
            "Finalidade": features.get("finalidade", None),
            "Tipo de terreno": features.get("tipo de terreno", None),
            "Acesso pavimentado": features.get("acesso pavimentado", None),
            "Asfaltado": features.get("asfaltado", None),
            "Iluminação pública": features.get("iluminação pública", None),
            "Zona arborizada": features.get("zona arborizada", None),
            "Declive": features.get("declive", None),
            "Ruína": features.get("ruína", None),
            "Alarme": features.get("alarme", None),
            "Furo de água": features.get("furo de água", None),
            "Domótica": features.get("domótica", None),
            "Casa das máquinas": features.get("casa das máquinas", None),
            "Condomínio Fechado": features.get("condomínio fechado", None),
            "Parque infantil": features.get("parque infantil", None),
            "Piscina": features.get("piscina", None),
            "Piscina Privada": features.get("piscina privada", None),
            "Termoacumulador": features.get("termoacumulador", None),
            "Garagem exterior": features.get("garagem exterior", None),
            "Mobilado": features.get("mobilado", None),
            "Hidromassagem/jacuzzi": features.get("hidromassagem/jacuzzi", None),
            "Quintal/horta": features.get("quintal/horta", None),
            "Ginásio": features.get("ginásio", None),
            "Kitchenette": features.get("kitchenette", None),
            "Vigilância/segurança": features.get("vigilância/segurança", None),
            "Campo de ténis": features.get("campo de ténis", None),
            "Segurança 24 horas": features.get("segurança 24 horas", None),
            "Vedação": features.get("vedação", None),
            "Parqueamento (1 carro)": features.get("parqueamento (1 carro)", None),
            "Ligação a rede de água": features.get("ligação a rede de água", None),
            "Ligação a rede de saneamento": features.get(
                "Ligação a rede de saneamento", None
            ),
            "Ligação a rede elétrica": features.get("ligação a rede eléctrica", None),
            "Animais permitidos": features.get("animais permitidos", None),
            "Parqueamento (2 carros)": features.get("parqueamento (2 carros)", None),
            "Cofre": features.get("cofre", None),
            "Vista de rio": features.get("vista de rio", None),
            "Nº divisões": features.get("nº divisões", None),
            "Tipo": features.get("tipo", None),
            "Pisos": features.get("pisos", None),
            "Com WC": features.get("com wc", None),
            "Montra": features.get("montra", None),
            "Anexo habitacional": features.get("anexo habitacional", None),
            "Detetor de incêndio": features.get("detector de incêncio", None),
            "Detetor de Inundução": features.get("detector de inundução", None),
            "Vista de cidade": features.get("vista de cidade", None),
            "Área (m/2)": features.get("área (m/2)", None),
            "Vista de mar": features.get("vista de mar", None),
            "Jacuzzi": features.get("jacuzzi", None),
            "Património classificado": features.get("património classificado", None),
            "Adaptada a mobilidade reduzida": features.get(
                "adaptada a mobilidade reduzida", None
            ),
            "Com cozinha": features.get("com cozinha", None),
            "Imóvel de banca": features.get("imóvel de banca", None),
            "Vista de lago": features.get("vista de lago", None),
            "Fossa séptica": features.get("fossa séptica", None),
            "Licensa de construção": features.get("licensa de construção", None),
            "Acesso a veículos pesados": features.get(
                "acesso a veículos pesados", None
            ),
            "Área administrativa": features.get("área administrativa", None),
            "Copa": features.get("copa", None),
            "Recepção": features.get("recepção", None),
            "Refeitório": features.get("refeitório", None),
            "Sala de reuniões": features.get("sala de reuniões", None),
            "Área florestal": features.get("área florestal", None),
            "Hidromassagem": features.get("hidromassagem", None),
            "Percurso de água": features.get("percurso de água", None),
            "Armazém": features.get("armazém", None),
            "Vista de Serra": features.get("vista de serra", None),
            "Adaptado a mobilidade reduzida": features.get(
                "adaptado a mobilidade reduzida", None
            ),
            "Terra batida": features.get("terra batida", None),
            "Video vigilância": features.get("video vigilância", None),
            "Espaço frigorífico": features.get("espaço frigorífico", None),
            "Espaço para arrumação": features.get("espaço para arrumação", None),
            "Casa de banho partilhada": features.get("casa de banho partilhada", None),
            "Poço": features.get("poço", None),
            "Sótão": features.get("sótão", None),
            "Paisagem protegida": features.get("paisagem protegida", None),
        },
        ignore_index=True,
    )

    obj.to_csv("dados_imovirtual.csv", mode="a", header=False, index=False)


def main():

    i = 1
    dictio = {}
    while 1:

        # Final das páginas
        if i == 215:
            break

        # Url das páginas de apartamentos da 'Sapo.pt', aceder num ciclo às páginas existentes
        htmlBraga = f"https://www.imovirtual.com/comprar/braga/?search%5Bregion_id%5D=3&search%5Bsubregion_id%5D=36&page={i}"

        print(htmlBraga)

        # Realizar o parsing da página associada ao iterador do ciclo
        soup = parseHTML(htmlBraga)

        # Encontrar o link de cada imóvel presente na página, através do id associado
        container = soup.find_all(
            "article", id=re.compile("offer-item-ad_id[0-9a-zA-Z]*")
        )

        # print(container)

        # Para cada link do imóvel presente no imóvel, ir buscar as features associadas a esse através do método imovelFeatures(imovel)
        for tableCode in container:
            # print(tableCode['data-url'])
            imovel = parseHTML(tableCode["data-url"])
            imovelFeatures(imovel)
            # dictio.update(features)

        # Aumentar o iterador associado às páginas
        i = i + 1
    # print(dictio.keys())


main()
