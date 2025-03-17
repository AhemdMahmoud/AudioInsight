from googletrans import Translator
from langdetect import detect

def translate_text(text):
    """
    Automatically detect language and translate between English and Arabic
    """
    try:
        detected_lang = detect(text)
        translator = Translator()
        
        # If text is in Arabic, translate to English
        if detected_lang == 'ar':
            translation = translator.translate(text, dest='en')
            return translation.text
            
        # If text is in English or any other language, translate to Arabic
        else:
            translation = translator.translate(text, dest='ar')
            return translation.text
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
