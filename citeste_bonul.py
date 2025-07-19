import easyocr
import cv2

# Read the image
image_path = r"D:\imagini\bonuri\bon2.jpeg"
img = cv2.imread(image_path)

# Save the image using cv2 
save_path = r"D:\PycharmProjects\Imagine_Original.jpeg"
cv2.imwrite(save_path, img)

#output path for the cropped receipt
output_path = r"D:\PycharmProjects\bon1_cropped.jpeg"

reader = easyocr.Reader(['en','ro']) #languages
results = reader.readtext(image_path)

# cropped image boundaries
start_keywords = ['lei', 'preț', 'produse', 'pret', 'ron']
end_keywords = ['tva', 'total tva']

start_y = None
end_y = None


for bbox, text, _ in results:
    text_lower = text.lower()
    if start_y is None and any(k in text_lower for k in start_keywords):
        start_y = min([point[1] for point in bbox])  # y minim din box
    if end_y is None and any(k in text_lower for k in end_keywords):
        end_y = max([point[1] for point in bbox])  # y maxim din box


if start_y is None:
    start_y = 0


if end_y is None:
    end_y = img.shape[0]


cropped_img = img[int(start_y):int(end_y), :]


cv2.imwrite(output_path, cropped_img)
final_results = reader.readtext(output_path)

# write the text the cropped image contains
for bbox, text, confidence in final_results:
    print(text)
