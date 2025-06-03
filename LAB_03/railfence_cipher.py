import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_Dialog
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.encrypt_btn.clicked.connect(self.call_api_encrypt)
        self.ui.decrypt_btn.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        try:
            payload = {
                "plain_text": self.ui.plaintext_txt.toPlainText(),
                "key": int(self.ui.key_txt.text())
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if "encrypted_text" in data:
                    self.ui.ciphertext_txt.setPlainText(data["encrypted_text"])
                    QMessageBox.information(self, "Success", "Encrypted successfully.")
                else:
                    QMessageBox.warning(self, "Warning", "No 'encrypted_text' in response.")
            else:
                QMessageBox.critical(self, "Error", f"API error: {response.status_code}")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Key must be an integer.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        try:
            payload = {
                "cipher_text": self.ui.ciphertext_txt.toPlainText(),
                "key": int(self.ui.key_txt.text())
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if "decrypt_text" in data:
                    self.ui.plaintext_txt.setPlainText(data["decrypt_text"])
                    QMessageBox.information(self, "Success", "Decrypted successfully.")
                else:
                    QMessageBox.warning(self, "Warning", "No 'decrypt_text' in response.")
            else:
                QMessageBox.critical(self, "Error", f"API error: {response.status_code}")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Key must be an integer.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
