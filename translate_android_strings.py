import os
import sys
import requests
from xml.etree import ElementTree as ET

API_KEY = "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"
URL = "https://api.openai.com/v1/engines/text-davinci-002/completions"


def translate_text(text, source_lang, target_lang):
    prompt = f"Translate the following text from {source_lang} to {target_lang}: {text}"

    data = {
        "prompt": prompt,
        "max_tokens": 200,
        "n": 1,
        "stop": None,
        "temperature": 1
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(URL, json=data, headers=headers)
    result = response.json()
    
    # 新增：输出 API 返回的完整响应
    print("API response:", result)

    translated_text = result['choices'][0]['text'].strip()
    return translated_text


def translate_android_strings(input_file, output_file, source_lang, target_lang):
    tree = ET.parse(input_file)
    root = tree.getroot()

    for child in root:
        if child.tag == "string":
            original_text = child.text
            if original_text and not original_text.startswith("@"):
                translated_text = translate_text(original_text, source_lang, target_lang)
                child.text = translated_text

    tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python translate_android_strings.py input_file output_file source_lang target_lang")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    source_lang = sys.argv[3]
    target_lang = sys.argv[4]

    translate_android_strings(input_file, output_file, source_lang, target_lang)
    print("Translation completed.")
