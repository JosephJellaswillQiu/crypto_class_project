from flask import Flask, render_template, request
from util import *
import json

app = Flask(__name__)

tiered_frequencies = {
    "tier1": [("e", 0.12702)],
    "tier2": [
        ("a", 0.08167), ("h", 0.06094), ("i", 0.06996), ("n", 0.06749),
        ("o", 0.07507), ("r", 0.05987), ("s", 0.06327), ("t", 0.09056)
    ],
    "tier3": [
        ("b", 0.01492), ("c", 0.02782), ("d", 0.04253), ("f", 0.02228),
        ("g", 0.02015), ("l", 0.04025), ("m", 0.02406), ("p", 0.01929),
        ("u", 0.02758), ("w", 0.02360), ("y", 0.01974)
    ],
    "tier4": [
        ("j", 0.00153), ("k", 0.00772), ("q", 0.00095), ("v", 0.00978),
        ("x", 0.00150), ("z", 0.00074)
    ]
}


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    error = ""
    key_raw = ""
    hint = ""
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
                    hint = f"根据英语的统计，单词频率分级为{tiered_frequencies}，可以参考这些频率来进行单词的猜测。"
                elif assist_type == "compare":
                    result = contrast_decrypt(text, key)
                elif assist_type == "word_check":
                    resultdict,total,count=check_short_words_validity(text, key)
                    result = f"总单词数：{total}\n有效单词数：{count}\n无效单词数：{total-count}\n检查结果：{resultdict}"
                elif assist_type == "intelligent_assist":
                    result = generate_assist_suggestions(text, key)
            print(f"Mode: {mode}, Text: {text}, Key: {key},result: {result}")
        except Exception as e:
            error = f"密钥格式错误：{str(e)}"
            print(f"Error: {error}")
            
    return render_template("index.html",hint=hint,mode=mode, result=result, error=error, key_raw=key_raw)


if __name__ == "__main__":
    app.run(debug=True)


