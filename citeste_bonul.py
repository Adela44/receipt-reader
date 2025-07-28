import easyocr
import cv2
import re

# Read the image
image_path = r"D:\imagini\bonuri\bon1.jpeg"
img = cv2.imread(image_path)
if img is None:
    raise ValueError("Failed to load image. Check file path or format.")

# Save the image using cv2
save_path = r"D:\PycharmProjects\Imagine_Original.jpeg"
cv2.imwrite(save_path, img)

#output path for the cropped receipt
output_path = r"D:\PycharmProjects\bon1_cropped.jpeg"

reader = easyocr.Reader(['en','ro']) #languages
results = reader.readtext(image_path)

# cropped image bounds
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
if cropped_img.size == 0:
    raise ValueError("Cropped image is empty. Check your crop dimensions.")

cv2.imwrite(output_path, cropped_img)
final_results = reader.readtext(output_path)

# write the text the cropped image contains
for bbox, text, confidence in final_results:
    print(text)

products = []
product_buffer = []

# Match prices like 7,98, optionally surrounded by spaces
price_pattern = re.compile(r"^\s*\d{1,3}\s*,\s*\d{2}\s*$")

for _, text, _ in final_results:
    clean_text = text.strip()

    # If it looks like a price, flush the buffer
    if price_pattern.match(clean_text):
        product_name = " ".join(product_buffer).strip()
        if product_name:
            name_lower = product_name.lower()
            if (
                    name_lower == "total"
                    or (
                    name_lower != "lei"
                    and "sub" not in name_lower
                    and "tva" not in name_lower
                    and "kg" not in name_lower
            )
            ):
              products.append((product_name, clean_text.replace(" ", "")))
        product_buffer = []  # reset for next product
    else:
        # Filter out lines that are quantities or units (e.g. 2.000, BUC, X 3 , 99)
        if not re.search(r"^\s*(x|\d|buc)", clean_text.lower()):
            product_buffer.append(clean_text)

# Print results
print("\n--- Products and Prices ---")
for name, price in products:
    print(f"{name} -> {price}")
