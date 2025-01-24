import requests, uuid, json
from dotenv import load_dotenv
import os
import traceback
import time, math
import re
from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential

# Cargar variables de entorno desde el archivo .env
load_dotenv()

        
# Add your key and endpoint

endpoint = "https://api.cognitive.microsofttranslator.com/"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
key = os.getenv('microsoft_key1')
location = os.getenv('microsoft_location')

path = '/translate'

headers = {
    'Ocp-Apim-Subscription-Key': key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

def translate_text(texts, from_lang, to_langs, do_not_translate=[]):
    """
    Traduce una lista de textos desde un idioma origen a uno o más idiomas destino,
    protegiendo palabras específicas para que no sean traducidas.

    Args:
        texts (list): Lista de textos a traducir.
        from_lang (str): Idioma original.
        to_langs (list): Lista de idiomas a los que traducir.
        do_not_translate (list): Lista de palabras/frases que no deben ser traducidas.

    Returns:
        list: Lista de textos traducidos.
    """
    time_sleep = 3
    placeholders = {word: f"__{i}__" for i,word in enumerate(do_not_translate)}  # Crear marcadores

    # Reemplazar palabras protegidas por marcadores en los textos originales
    modified_texts = []
    for text in texts:
        for word, placeholder in placeholders.items():
            text = text.replace(word, placeholder)
        modified_texts.append(text)

    while True:
        constructed_url = endpoint + path
        body = [{'text': text} for text in modified_texts]

        params = {
            'api-version': '3.0',
            'from': from_lang,
            'to': to_langs,
            'textType': 'html'
        }

        try:
            # Solicitud a la API
            response = requests.post(constructed_url, params=params, headers=headers, json=body)
            json_response = response.json()

            if not response.ok:
                if 'error' in json_response and json_response['error']['code'] == 429001:
                    # Manejo de límite de solicitudes
                    print(f"Esperando {time_sleep} segundos para no sobrecargar el servicio")
                    time.sleep(time_sleep)
                    time_sleep = math.ceil(time_sleep * math.log2(time_sleep))
                else:
                    print(f"Error en la solicitud: {json_response}")
                    break
            else:
                break

        except Exception as e:
            traceback.print_exc()
            print(f"Error: {e}")
            return []

    # Revertir los marcadores a las palabras originales en los textos traducidos
    translated_texts = [item['translations'][0]['text'] for item in json_response]
    for i, text in enumerate(translated_texts):
        for word, placeholder in placeholders.items():
            text = text.replace(placeholder, word)
        translated_texts[i] = text

    return translated_texts



def detect_language(texts):
    """
    Detecta el idioma de una lista de textos usando la API de Microsoft Translator.
    """
    path = '/detect'
    constructed_url = f"{endpoint}{path}?api-version=3.0"
    
    body = [{'text': text} for text in texts]
    
    headers = {
        "Ocp-Apim-Subscription-Key": key,  # Asegúrate de que `key` esté definido
        "Ocp-Apim-Subscription-Region": location,  # Asegúrate de que `location` esté definido
        "Content-Type": "application/json"
    }
    time_sleep = 3
    
    while True:
        try:
            # Realiza la solicitud POST
            response = requests.post(constructed_url, headers=headers, json=body)
            json_response = response.json()
            
            if not response.ok:
                if json_response['error']['code'] == 429001:
                    # print(f"Esperar {time_sleep} segundos para no sobrecargar el servicio")
                    time.sleep(time_sleep)
                    time_sleep = math.ceil(time_sleep * math.log2(time_sleep))
                    continue
            return response.json()  # Devuelve la respuesta en formato JSON
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error al detectar el idioma: {e}")


if __name__ == "__main__":
    
    texts = ["O teu gusto", "Como me gusta Xogo de fíos", "Adeus para sempre meu amor","All products","""<p><span><span><span><span>Sentes esa conexión máxica coa música? Pertences a unha banda de gaitas? Vives o baile galego? Séntete parte da esencia de Galicia a través desta obra artesanal!</span></span></span></span></p><p>&nbsp;</p><p><span><span><span><span>Descubre esta exclusiva figura do muiñeiro no que se combina arte e tradición galegas, confeccionada <strong>artesanalmente</strong> por Xogo de Fíos. Trátase dun proceso de creación realmente singular, no que tan só intervén a habilidade manual e o<strong> tacto </strong>que posúe Lorena para dar maxia a cada deseño. Esta técnica <strong>artesanal</strong> de <strong>fiado </strong>basease na creatividade e a diferenciación do produto; sempre con énfase nos valores transversais de igualdade, inclusión das persoas con discapacidade e a sustentabilidade co medio ambiente.</span></span></span></span></p><p>&nbsp;</p><p><span><span><span><span>As danzas e cantigas populares interpretadas ao redor do muiño, na mentres esperaban pola muñaxe, convertéronse en auténticos símbolos da cultura galega. Neste caso representado por este home que viste o traxe rexional do baile galego.. Por iso, en Xogo de fíos dámoslle un enfoque único, no que cada detalle foi fiado a man con agarimo para capturar a esencia das nosas tradicións. Asemade, empregamos a base de madeira natural que aporta autenticidade e resalta as cores que fían este traballo artesanal. </span></span></span></span></p><p>&nbsp;</p><p><span><span><span><span>CARACTERÍSTICAS:</span></span></span></span></p><ul>	<li><strong><span>Materiais</span></strong><span><strong>:</strong> fío de finca (algodón 100%), cinta de dobre cara, prato de madeira natural, cola branca de madeira, verniz mate ecolóxico en aerosol e colgadoiro.</span></li>	<li><strong><span>Deseño</span></strong><span><strong>: </strong>muiñeiro confeccionado con fío sobre base de madeira natural.</span></li>	<li><span>Dimensións</span><span>: 20cm diámetro e 2cm grosor.</span></li>	<li><span><strong>Bases</strong>: polo formato do deseño empregamos madeira, pero no caso que prefiras outras bases (cadro ou tablilla) recoméndase contactar.</span></li>	<li><span><strong>Personalizado</strong>: </span><span>unha opción é porlle o teu nome ou o da banda de gaitas.</span></li></ul><p>&nbsp;</p><p><span><span><span><span>O TEU GUSTO: en Xogo de Fíos creemos na individualidade, na singularidade e na creatividade; por iso tes opción de personalizar (deseño, cor, tamaño, base, nome...) para que se adapte perfectamente o teu estilo. Contáctanos para converter a túa idea en realidade! </span></span></span></span></p><p>&nbsp;</p><p><span><span><span><span>BENEFICIOS:</span></span></span></span></p><ul>	<li><strong><span>Singularidade</span></strong><span><strong>:</strong> peza decorativa que combina arte, tradición e cultura.</span></li>	<li><strong><span>Distinción</span></strong><span>: a elegancia e sentimento que transmite esta obra é innegable, pero o verdadeiro valor engadido do produto radica na confección a través do tacto.</span></li>	<li><strong><span>Proceso</span></strong><span><strong> manual</strong>: trátase dunha obra confeccionada totalmente a man, sen que medie ningún tipo de maquinaria. O tacto é o instrumento de traballo.</span></li>	<li><strong><span>Referente</span></strong><span><strong> artístico</strong>: atendemos minuciosamente cada detalle do proceso, sendo conscientes da dedicación que implica esta técnica e ofrecemos a opción de personalizar sempre que sexa posible.</span></li>	<li><strong><span>Sustentable</span></strong><span> co medio ambiente e de calidade en canto a materiais e servizos.</span></li>	<li><strong><span>Ideal para amantes da música tradicional ou do baile galego. Regala calidade!</span></strong></li></ul><p>&nbsp;</p><p><span><span><span><span>PREZO: 22€ (IVA incluído) + gastos de envío a toda España.</span></span></span></span></p><p>&nbsp;</p><p><span><span><span><span>POLÍTICA DE DEVOLUCIÓN:</span></span></span></span></p><ul>	<li><span>Debido a ruptura do produto ou mala calidade do mesmo, aceptamos devolucións nos 14 días naturais posteriores á súa recepción, asumindo desde Xogo de Fíos o custo de dita devolución.</span></li>	<li><span>Se o cliente rexeita o produto por motivos persoais, aceptamos devolucións nos 14 días naturais posteriores a recepción do mesmo, asumindo o cliente dito custo. </span></li></ul><p>&nbsp;</p><p><span><span><span><span>Valora cada peza como unha obra única de arte inclusiva!</span></span></span></span></p><p>&nbsp;</p>"""]
    
    idiomas = []
    response = detect_language(texts)
    
    for i, idioma in enumerate(response):
        response = translate_text([texts[i]], idioma['language'], 'es',do_not_translate=['Xogo de fíos'])
        print(response)