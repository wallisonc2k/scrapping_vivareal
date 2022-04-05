import requests
from bs4 import BeautifulSoup


def scrapping(paginas=10):
    """
        paginas --> int
            Até que pagina deve ser feito o scrapping
    """
    url = "https://www.vivareal.com.br/venda/?pagina={npagina}"

    fichas=[]

    for pagina in range(1,paginas+1):
        print("Estou aqui: " + url.format(npagina=pagina))
        
        # pega a página do site pela internet
        doc = requests.get(url.format(npagina=pagina)) #obtem o html bruto
        
        # analisa o HTML
        analisador = BeautifulSoup(doc.content, 'html.parser') #realiza o parseamento para aplicar a estrutura da arvore DOM ao html
        
        # extrai somente a lista de imóveis (em HTML) usando o seletor descoberto no código da página
        imoveis = analisador.find_all('div', class_="js-card-selector")
        
        for unidade in imoveis:
            uni={}
            # extrai dado por dado segundo seus seletores...
            
            # O ID:
            uni['id']    = unidade.parent.get('id')
            
            # O título/nome:
            uni['nome']  = unidade.find("span",class_="property-card__title").contents[0].strip()
            
            # O endereço:
            uni['end']  = unidade.find("span",class_="property-card__address").contents[0].strip()
            
            # A metragem
            uni['area']=int(unidade.find('ul',class_='property-card__details').find('span',class_='property-card__detail-area').text.strip())
            
            # O preço tem uma pegadinha
            try:
                # Na maioria dos anuncios o preço está na posição 1.
                # Mas em alguns, o preço aparece como "a partir de" e causa um erro aqui.
                uni['preco'] = int(str(unidade.find("div",class_="property-card__price").contents[1]).split('R$ ')[1].split(' ',1)[0].replace('.',''))
            except ValueError:
                # Então o meu tratamento de erro para preços "a partir de" é tentar capturá-lo na posição 2:
                try:
                    uni['preco'] = int(str(unidade.find("div",class_="property-card__price").contents[2]).split('R$ ')[1].split(' ',1)[0].replace('.',''))
                except IndexError:
                    # Mas há um outro tipo de problema, onde o preço aparece "sob consulta", e causa um "IndexError". Trato assim:
                    uni['preco'] = -1

            # Condomínio:
            try:
                uni['condominio'] = imoveis[1].find(class_="js-condo-price").text.strip().split('R$ ')[1].replace('.','')
            except:
                pass

            # A descrição:
            try:
                uni['desc']  = unidade.find('ul',class_='property-card__details').text.strip()
            except:
                pass

            # No final deste loop, o dict uni contém os dados de 1 imóvel, aí adiciono-o a uma lista de imóveis
            fichas.append(uni)

    """Processei todos os imóveis de todas as páginas. Vamos ver o resultado..."""

    return fichas