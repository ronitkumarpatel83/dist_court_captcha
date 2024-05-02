import re
import time
import cv2
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://services.ecourts.gov.in/ecourtindia_v4_bilingual/cases/case_no.php?state=D&state_cd=13&dist_cd=20")
driver.maximize_window()

time.sleep(2)
element = driver.find_element(By.ID, 'captcha_image')
element.screenshot("image/image.png")

img = Image.open("image/image.png")
threshold = 115  # Adjust as needed
black_and_white_img = img.point(lambda x: 0 if x < threshold else 190)
# Save the black-and-white image
black_and_white_img.save("image/black.png")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

text = pytesseract.image_to_string(black_and_white_img, config='--psm 6')
pattern = r"[^a-zA-Z0-9]+"
cap = re.sub(pattern, "", text)
print("Text : ", cap)
