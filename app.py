from flask import Flask, request, send_file, render_template, json
from translate_android_strings import translate_android_strings
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    # 源语言
    with open('data/source_lang.json', 'r', encoding='utf-8') as file:
        source_languages = json.load(file)
    # 目标语言
    with open('data/target_lang.json', 'r', encoding='utf-8') as file:
        target_languages = json.load(file)
    return render_template("index.html", source_languages=source_languages, target_languages=target_languages)

@app.route('/translate', methods=['POST'])
def translate():
    input_file = request.files['input_file']
    source_lang = request.form['source_lang']
    target_lang = request.form['target_lang']
    print(source_lang)
    # Create temporary input and output files
    input_temp = tempfile.NamedTemporaryFile(delete=False)
    output_temp = tempfile.NamedTemporaryFile(delete=False)
    
    input_temp.write(input_file.read())
    input_temp.close()
    
    translate_android_strings(input_temp.name, output_temp.name, source_lang, target_lang)
    
    # Send the translated file
    return send_file(output_temp.name, as_attachment=True, download_name='strings_translated.xml')


if __name__ == '__main__':
    app.run(debug=True)
