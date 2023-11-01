import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit
from PyQt5.QtGui import QFont
import cv2
import pytesseract
import io
import requests
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
tessdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'


# create a class for the main window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OCR Tool")

        self.setStyleSheet("""
            QWidget {
                background-color: "lightcyan";
            
            }
            
            QLabel, QLineEdit, QComboBox, QPushButton {
                font-size: 25pt;
            }
        """)
        # create the UI elements
        self.window_label = QLabel("OCR Tool")
        self.window_label.setAlignment(Qt.AlignCenter)
        self.text_edit = QTextEdit()

        self.choice_label = QLabel("Enter main choice:")
        self.choice_combobox = QComboBox()
        self.choice_combobox.addItems(["Extract text from image", "Find and highlight target word in image"])
        self.num1_label = QLabel("Enter the first choice:")
        self.num1_lineedit = QLineEdit()
        self.num2_label = QLabel("Enter the second choice:")
        self.num2_lineedit = QLineEdit()
        self.image_label = QLabel("Enter the name of the image with extension:")
        self.image_lineedit = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_clicked)
        self.target_word_label = QLabel("Enter target word:")
        self.target_word_lineedit = QLineEdit()
        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.go_clicked)
        # create the layouts
        self.input_layout = QVBoxLayout()
        self.input_layout.addWidget(self.window_label)
        self.input_layout.addWidget(self.choice_label)
        self.input_layout.addWidget(self.choice_combobox)
        self.input_layout.addWidget(self.num1_label)
        self.input_layout.addWidget(self.num1_lineedit)
        self.input_layout.addWidget(self.num2_label)
        self.input_layout.addWidget(self.num2_lineedit)
        self.input_layout.addWidget(self.image_label)
        self.input_layout.addWidget(self.image_lineedit)
        self.input_layout.addWidget(self.browse_button)
        self.input_layout.addWidget(self.target_word_label)
        self.input_layout.addWidget(self.target_word_lineedit)
        self.input_layout.addWidget(self.go_button)
        self.input_layout.addWidget(self.text_edit)

        self.text_edit.setStyleSheet("""
            QTextEdit {
                font-size: 26pt;
            }
        """)

        # create the main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.input_layout)
        # set the layout for the main window
        self.setLayout(self.main_layout)
        # set the main window properties
        self.setWindowTitle("OCR GUI")
        self.setGeometry(100, 100, 400, 400)
        # show the main window
        self.show()

    def browse_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                   "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
        if file_name:
            self.image_lineedit.setText(file_name)

    def go_clicked(self):
        choice = self.choice_combobox.currentIndex()
        if choice == 0:
            num1 = self.num1_lineedit.text()
            num2 = self.num2_lineedit.text()
            myconfig = f"--psm {num1} --osm {num2}"
            image = self.image_lineedit.text()
            if 'http' in image:
                img_resp = requests.get(image)
                image = Image.open(io.BytesIO(img_resp.content))
            text = pytesseract.image_to_string(image, config=tessdata_dir_config)
            self.text_edit.setText(text)
        elif choice == 1:
            b = self.image_lineedit.text()
            a = self.target_word_lineedit.text()
            image = cv2.imread(b)
            image_copy = image.copy()
            target_word = a
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=tessdata_dir_config)
            word_occurences = [i for i, word in enumerate(data["text"]) if word == target_word]
            for occ in word_occurences:
                w = data["width"][occ]
                h = data["height"][occ]
                l = data["left"][occ]
                t = data["top"][occ]
                p1 = (l, t)
                p2 = (l + w, t)
                p3 = (l + w, t + h)
                p4 = (l, t + h)
                image_copy = cv2.line(image_copy, p1, p2, color=(255, 0, 0), thickness=2)
                image_copy = cv2.line(image_copy, p2, p3, color=(255, 0, 0), thickness=2)
                image_copy = cv2.line(image_copy, p3, p4, color=(255, 0, 0), thickness=2)
                image_copy = cv2.line(image_copy, p4, p1, color=(255, 0, 0), thickness=2)
                image_copy = cv2.line(image_copy, p1, p4, color=(255, 0, 0), thickness=2)
            cv2.imshow("Output", image_copy)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


# create the main function
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


# run the main function
if __name__ == "__main__":
    main()
