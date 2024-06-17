import sys
import pythoncom
import win32com.client
from PyQt5.QtCore import QTimer, QCoreApplication

class WordApp:
    def __init__(self):
        self.text = ''
        self.index = 0
        self.init_word()

    def init_word(self):
        pythoncom.CoInitialize()  # Initialize the COM library
        self.word_app = win32com.client.Dispatch("Word.Application")
        self.word_app.Visible = True
        
        # Add a new document
        self.document = self.word_app.Documents.Add()

    def add_text(self, text):
        # Add the text to the end of the document
        self.document.Content.Text += text

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)  # Use QCoreApplication instead of QApplication
    word_app = WordApp()
    sys.exit(app.exec_())
