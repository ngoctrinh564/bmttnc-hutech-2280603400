import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.playfair import Ui_Dialog

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.encrypt_btn.clicked.connect(self.call_api_encrypt)
        self.ui.decrypt_btn.clicked.connect(self.call_api_decrypt)
        self.ui.key_txt.textChanged.connect(self.update_matrix)

    def update_matrix(self):
        url = "http://127.0.0.1:5000/api/playfair/creatematrix"
        key = self.ui.key_txt.text()
        if not key.strip():
            self.ui.matrix_txt.clear()
            return
        try:
            response = requests.post(url, json={"key": key})
            if response.status_code == 200:
                data = response.json()
                matrix = data.get("playfair_matrix", [])
                formatted_matrix = "\n".join([" ".join(row) for row in matrix])
                self.ui.matrix_txt.setPlainText(formatted_matrix)
            else:
                self.ui.matrix_txt.setPlainText("Lỗi tạo ma trận.")
        except requests.exceptions.RequestException as e:
            self.ui.matrix_txt.setPlainText(f"Lỗi kết nối: {e}")

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        try:
            payload = {
                "plain_text": self.ui.plaintext_txt.toPlainText(),
                "key": self.ui.key_txt.text()
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                encrypted = data.get("encrypted_text", "")
                self.ui.ciphertext_txt.setPlainText(encrypted)
                QMessageBox.information(self, "Success", "Encrypted successfully.")
            else:
                QMessageBox.critical(self, "API Error", f"Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        try:
            payload = {
                "cipher_text": self.ui.ciphertext_txt.toPlainText(),
                "key": self.ui.key_txt.text()
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                decrypted = data.get("decrypted_text", "")
                self.ui.plaintext_txt.setPlainText(decrypted)
                QMessageBox.information(self, "Success", "Decrypted successfully.")
            else:
                QMessageBox.critical(self, "API Error", f"Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
