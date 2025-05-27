from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Caesar cipher routes
@app.route("/caesar")
def caesar():
    return render_template("caesar.html")

@app.route("/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    cipher = CaesarCipher()
    encrypted_text = cipher.encrypt_text(text, key)
    return f"text: {text} <br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    cipher = CaesarCipher()
    decrypted_text = cipher.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key} <br/>decrypted text: {decrypted_text}"

# Vigenere cipher routes
@app.route("/vigenere")
def vigenere():
    return render_template("vigenere.html")

@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    cipher = VigenereCipher()
    encrypted_text = cipher.vigenere_encrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    cipher = VigenereCipher()
    decrypted_text = cipher.vigenere_decrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

# Rail Fence cipher routes
@app.route("/railfence")
def railfence():
    return render_template("railfence.html")

@app.route("/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    cipher = RailFenceCipher()
    encrypted_text = cipher.rail_fence_encrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    cipher = RailFenceCipher()
    decrypted_text = cipher.rail_fence_decrypt(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

# Playfair cipher routes
@app.route("/playfair")
def playfair():
    return render_template("playfair.html")

@app.route("/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    encrypted_text = cipher.playfair_encrypt(text, matrix)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    decrypted_text = cipher.playfair_decrypt(text, matrix)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

from cipher.playfair import PlayFairCipher

playfair_cipher = PlayFairCipher()

@app.route("/playfair/creatematrix", methods=["POST"])
def playfair_create_matrix():
    key = request.form["matrixKey"]
    matrix = playfair_cipher.create_playfair_matrix(key)
    # Hiển thị kết quả trực tiếp, hoặc chuyển sang template nếu bạn muốn render đẹp hơn
    matrix_html = "<br>".join([" ".join(row) for row in matrix])
    return f"<h4>Matrix created with key '{key}':</h4><pre>{matrix_html}</pre><br><a href='/playfair'>Back</a>"


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
