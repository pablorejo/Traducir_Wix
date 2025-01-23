import requests, uuid, json
from dotenv import load_dotenv
import os
import traceback
import time, math
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



def translate_text(texts, from_lang, to_langs):
    time_sleep = 3
    while True:
        constructed_url = endpoint + path
        
        body = [{'text': text} for text in texts]
        
        params = {
            'api-version': '3.0',
            'from': from_lang,
            'to': to_langs,
            'textType': 'html'
        }
        try:
            response = requests.post(constructed_url, params=params, headers=headers, json=body)
            
            json_response = response.json()
            
            if not response.ok:
                if json_response['error']['code'] == 429001:
                    # print(f"Esperar {time_sleep} segundos para no sobrecargar el servicio")
                    time.sleep(time_sleep)
                    time_sleep = math.ceil(time_sleep * math.log2(time_sleep))
                else:
                    break
            else:
                break
            
        except Exception as e:
            traceback.print_exc()
            print(f"Error: {e}")
            return response.json()
        
    return response.json()


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
    texto = """Tablilla zodiacal Acuario🐠
    """
    response = translate_text([texto,'ola'], 'gl', ['es'])

    print(response)