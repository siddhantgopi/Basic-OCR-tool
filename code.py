import cv2
import pytesseract
import io
import requests
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
tessdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'

'''
Page segmentation Modes(PSM) :
0  Orientation and script detection
1  Automatic page segmentation with OSD
2  Automatic page segmentation but no OSD or OCR
3  Fully automatic page segmentation but no OSD.(Default)
4  Assume a single column of text of variable sizes
5  Assume a single uniform block of vertically aligned text 
6  Assume a single uniform block of text
7  Treat the image as single text line
8  treat the image as a single word
9  Treat the image as a single word in a circle
10 Treat the image as a single character
11 Sparse text. Find as much text as possible in no particular order
12 Sparse test with OSD
13 Paw line . Treat the image as a single text line
  -----------------------Tesseract specific tricks to get accurate text 
OCR Engine Mode
0  Legacy engine only
1  Neural nets LstM engine only
2  Legacy + LSTm engines
3  Default  
'''


choice=int(input("Enter main choice: "))
if choice==1:
    num1 = input("Enter the first choice: ")
    num2 = input("Enter the second choice: ")
    myconfig = r"--psm num1 --osm num2"
    image = input("Enter the name of the image with extension: ")
    print("-" * 40)
    # get the string and print the output
    if 'http' in image:
        img_resp = requests.get(image)
        image = Image.open(io.BytesIO(img_resp.content))

    text = pytesseract.image_to_string(image, config=tessdata_dir_config)
    print(text)
    print("-" * 40)
elif choice==2:
    import pytesseract
    import cv2
    import matplotlib.pyplot as plt
    from PIL import Image

    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    tessdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'

    b = input("Enter filename: ")
    a=input("Enter target word: ")


    # read the image using OpenCV
    image = cv2.imread(b)
    # make a copy of this image to draw in
    image_copy = image.copy()
    # the target word to search for
    target_word = a
    # get all data from the image
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=tessdata_dir_config)
    # get all occurences of the that word
    word_occurences = [ i for i, word in enumerate(data["text"]) if word == target_word ]

    for occ in word_occurences:
        # extract the width, height, top and left position for that detected word
        w = data["width"][occ]
        h = data["height"][occ]
        l = data["left"][occ]
        t = data["top"][occ]
        # define all the surrounding box points
        p1 = (l, t)
        p2 = (l + w, t)
        p3 = (l + w, t + h)
        p4 = (l, t + h)
        # draw the 4 lines (rectangular)
        image_copy = cv2.line(image_copy, p1, p2, color=(255, 0, 0), thickness=2)
        image_copy = cv2.line(image_copy, p2, p3, color=(255, 0, 0), thickness=2)
        image_copy = cv2.line(image_copy, p3, p4, color=(255, 0, 0), thickness=2)
        image_copy = cv2.line(image_copy, p4, p1, color=(255, 0, 0), thickness=2)

    plt.imsave("all_dog_words.png", image_copy)
    plt.imshow(image_copy)
    plt.show()