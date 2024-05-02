import time
import speech_recognition as sr
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

url = "https://services.ecourts.gov.in/ecourtindia_v4_bilingual/cases/case_no.php?state=D&state_cd=13&dist_cd=20"
driver.get(url)

play_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#captcha_container_2 .captcha_play_button"))
)
# Create a Recognizer object
recognizer = sr.Recognizer()

# Use the microphone as the source
with sr.Microphone() as source:
    print("Adjusting for ambient noise, please wait...")
    recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce noise by calibrating to the environment
    print("Please speak into the microphone...")
    play_button.click()
    audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=20)

print("Recording complete. Processing...")

try:
    text = recognizer.recognize_sphinx(audio_data)
    print("Audio converted into text :", text)
except sr.UnknownValueError:
    print("Could not understand the audio")
except sr.RequestError as e:
    print(f"Request error from Google Speech Recognition service; {e}")

driver.quit()
