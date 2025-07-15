from PIL import Image
import pytesseract
import os
#print(os.getcwd())

#image = Image.open('screenshot.png')
image = Image.open(r"C:\Users\Chandan.Sahoo1\pythonProject\dsf-RN\venv\screenshot.png")
text = pytesseract.image_to_string(image)
print(text)
