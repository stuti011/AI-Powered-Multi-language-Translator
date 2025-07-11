from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from googletrans import Translator
from gtts import gTTS
import googletrans
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/languages")
def get_languages():
    return jsonify(googletrans.LANGUAGES)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get('text_to_translate')
    source_language_code = data.get('source_language_input')
    target_languages = data.get('target_language_input')

    # Safety check: ensure source_language_code is a string
    if not isinstance(source_language_code, str) or source_language_code.strip() == "":
        source_language_code = 'auto'

    # Ensure target_languages is a list
    if not isinstance(target_languages, list):
        target_languages = [target_languages]

    translator = Translator()
    translations = {}

    for lang_code in target_languages:
        try:
            translation = translator.translate(text, dest=lang_code, src=source_language_code)
            translated_text = translation.text

            audio_path = f"static/translated_audio_{lang_code}.mp3"
            tts = gTTS(text=translated_text, lang=lang_code)
            tts.save(audio_path)

            translations[lang_code] = {
                "text": translated_text,
                "audioUrl": '/' + audio_path
            }

        except Exception as e:
            translations[lang_code] = {"error": str(e)}

    return jsonify({"translations": translations})

if __name__ == "__main__":
    os.makedirs('static', exist_ok=True)
    app.run(debug=True)
