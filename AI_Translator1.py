from googletrans import Translator, LANGUAGES

def translate_text(text, target_language_code, source_language_code=None):
    translator = Translator()
    try:
        if source_language_code:
            translation = translator.translate(text, dest=target_language_code, src=source_language_code)
        else:
            translation = translator.translate(text, dest=target_language_code) 
        return translation.text
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None

supported_languages = LANGUAGES

while True:
    text_to_translate = input("Enter the text you want to translate (or type 'quit' to exit): ")
    if text_to_translate.lower() == 'quit':
        break

    source_language_input = input("\nTranslate From (leave blank for auto-detection): ")
    target_languages_input = input("Translate To (enter multiple languages separated by commas): ")

    source_language_code = None
    if source_language_input:
        if source_language_input in supported_languages:
            source_language_code = source_language_input
        else:
            for code, lang in supported_languages.items():
                if lang.lower() == source_language_input.lower():
                    source_language_code = code
                    break
        if not source_language_code and source_language_input:
            print(f"\nSorry, the source language '{source_language_input}' you entered is not supported. Attempting with auto-detection.")

    target_languages = [lang.strip() for lang in target_languages_input.split(',')]

    for target_language_input in target_languages:
        target_language_code = None
        if target_language_input:
            if target_language_input in supported_languages:
                target_language_code = target_language_input
            else:
                for code, lang in supported_languages.items():
                    if lang.lower() == target_language_input.lower():
                        target_language_code = code
                        break

        if target_language_code:
            translated_text = translate_text(text_to_translate, target_language_code, source_language_code)
            if translated_text is not None:
                print(f"Translated text ({target_language_input}): {translated_text}")
        else:
            print(f"Sorry, the target language '{target_language_input}' you entered is not supported.")

    print("-" * 20) 