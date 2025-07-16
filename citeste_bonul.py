import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # typical path on Ubuntu

image_path = "/home/ubuntu/Downloads/bon2.jpeg"
image = cv2.imread(image_path)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray_image_output.jpg", gray)


data = pytesseract.image_to_data(image, lang='ron', output_type=pytesseract.Output.DICT)


start_y, end_y = None, None

for i, word in enumerate(data['text']):
    word = word.strip().lower()

    if 'cod' in word and 'fiscal' in data['text'][i + 1].lower():
        start_y = data['top'][i]

    if 'total' in word:
        end_y = data['top'][i] + data['height'][i]


if start_y and end_y:
    height, width, _ = image.shape
    cropped = image[start_y:end_y, 0:width]
    cv2.imwrite("bon_decupat.jpg", cropped)
    custom_config = r'--psm 11'  # Treat the image as a single uniform block of text
    text = pytesseract.image_to_string(cropped, lang='ron')
    print(text)
else:
    print("Not found 'Cod fiscal' or 'TOTAL' in the image.")