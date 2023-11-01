This Python code is a PyQt5-based graphical user interface (GUI) application for Optical Character Recognition (OCR) tasks. It provides two main functions:

1. Extract Text from an Image:
   - The user can select an image file (local or via URL).
   - Adjust OCR parameters (Page Segmentation Mode - `psm` and OCR Segmentation Mode - `osm`).
   - Upon clicking the "Go" button, the application uses Tesseract OCR to extract text from the provided image. The extracted text is displayed in a QTextEdit widget.

2. Find and Highlight Target Word in an Image:
   - The user provides an image file.
   - The user specifies a target word to find and highlight.
   - Upon clicking the "Go" button, the application reads the image and uses Tesseract OCR to find occurrences of the target word.
   - It then highlights these occurrences in the image by drawing rectangles around them using OpenCV.
   - The highlighted image is displayed for the user to view.

Key components of the code:
- PyQt5 is used for the GUI, creating windows, labels, buttons, and text input fields.
- Tesseract OCR is utilized for text extraction from images.
- OpenCV is used for image processing and highlighting the target word.
- The code defines a class `MainWindow` that represents the main application window, and it provides methods for handling user interactions, including file selection and OCR operations.

This OCR tool allows users to interact with image-based text data easily, making it useful for tasks like extracting text from scanned documents or analyzing images containing text. Users can fine-tune OCR settings and visually locate specific words within images.
