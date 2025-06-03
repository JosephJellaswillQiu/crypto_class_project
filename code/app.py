from flask import Flask, render_template, request
from util import *
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    error = ""
    key_raw = ""
    mode = "encrypt"  # Default mode

    if request.method == "POST":
        mode = request.form.get("mode")
        text = request.form.get("text", "")
        key_raw = request.form.get("key", "")

        try:
            key = json.loads(key_raw.lower())  
            if not isinstance(key, dict):
                raise ValueError("密钥必须是字典格式。")
        
            
            if mode == "encrypt":
                result = encrypt(text, key)
            elif mode == "decrypt":
                result = decrypt(text, key)
            elif mode == "freq":
                freq_type = request.form.get("freq_type")
                if freq_type == "letter":
                    result = json.dumps(letter_frequency(text), indent=2)
                elif freq_type == "bigram":
                    result = json.dumps(bigram_frequency(text), indent=2)
                elif freq_type == "trigram":
                    result = json.dumps(trigram_frequency(text), indent=2)
                elif freq_type == "word":
                    result = json.dumps(word_frequency(text), indent=2)
            elif mode == "assist":
                assist_type = request.form.get("assist_type")

                
                if assist_type == "vowel":
                    result = suggest_vowels(text,key)
                elif assist_type == "word_level":
                    result = json.dumps(suggest_by_word_frequency(text),indent=2)
                elif assist_type == "compare":
                    result = contrast_decrypt(text, key)
            print(f"Mode: {mode}, Text: {text}, Key: {key},result: {result}")
        except Exception as e:
            error = f"密钥格式错误：{str(e)}"
            print(f"Error: {error}")
            
    return render_template("index.html",mode=mode, result=result, error=error, key_raw=key_raw)


if __name__ == "__main__":
    app.run(debug=True)
