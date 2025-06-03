from flask import Flask, render_template, request
from util import encrypt, decrypt
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    error = ""
    key_raw = ""

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
            print(f"Mode: {mode}, Text: {text}, Key: {key}")
        except Exception as e:
            error = f"密钥格式错误：{str(e)}"
            print(f"Error: {error}")

    return render_template("index.html", result=result, error=error, key_raw=key_raw)


if __name__ == "__main__":
    app.run(debug=True)
