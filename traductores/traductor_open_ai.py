from dotenv import load_dotenv
import os
import traceback
import time, math

from openai import OpenAI
import asyncio
client = OpenAI()
# Cargar variables de entorno desde el archivo .env
load_dotenv()

model = 'gpt-4o'

async def translate_text(texts, from_lang, to_lang, ten_en_cuenta=''):
    """Traduce un texto de un idioma a otro usando OpenAI.

    Args:
        texts (str): lista de textos para traducir.
        from_lang (str): idioma original, mejor si está el nombre completo del idioma. ejm: 'spanish'
        to_langs (str): idioma a traducir, mejor si está el nombre completo del idioma. ejm: 'english'

    Returns:
        list(str): una lista de str con los textos traducidos.
    """

    translations = []
    for text in texts:
        
        messages = [
            {"role": "system", "content": f"You are a highly skilled translator proficient in translating from {from_lang} to {to_lang}. You only return the text translate without more explanation."},
            {"role": "user", "content": f"Please translate the following text from {from_lang} to {to_lang}. If the text is already in {to_lang}, return original text. Preserve the HTML format, emoticons, and special characters. The text is in UTF-8 encoding. {ten_en_cuenta}:\n\n{text}"}
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            # max_tokens=5000,
            # temperature=0.3,
        )
        translation = response.choices[0].message.content
        
        translations.append({
                "translations": 
                [
                    {"text": translation}
                ]
            })
    return translations

def detect_language(texts):
    pass

if __name__ == "__main__":
    texts = ["O teu gusto", "Como me gusta Xogo de fíos", "Adeus para sempre meu amor"]
    ten_en_cuenta = f'IMPORTANT: This word should not be translated: {", ".join(texts)}'
    
    loop = asyncio.get_event_loop()
    model= 'gpt-4o-mini'
    response = loop.run_until_complete(translate_text(texts, 'Galician', 'español', ten_en_cuenta=ten_en_cuenta))

    print(response)
