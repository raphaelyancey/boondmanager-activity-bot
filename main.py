from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os
import time
import tempfile

if os.getenv("BOOND_LOGIN") == None or os.getenv("BOOND_PASSWORD") == None:
    raise Exception("Env vars BOOND_LOGIN and BOOND_PASSWORD must be set")

temp_profile = tempfile.mkdtemp()

# Initialiser le navigateur
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument(f"--user-data-dir={temp_profile}")  # Unique profile
driver = webdriver.Chrome(service=Service("/snap/bin/chromium.chromedriver"), options=options)
driver.set_window_size(1024, 768)
driver.maximize_window()

try:
    # Aller sur la page de connexion
    driver.get("https://ui.boondmanager.com/login")

    # Se connecter
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login"))).send_keys(os.getenv("BOOND_LOGIN"))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(os.getenv("BOOND_PASSWORD"), Keys.RETURN)

    # Attendre que la page charge et cliquer sur "Mes temps"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="nav-item-title" and text()="Mes temps"]'))).click()

    # Exécuter les actions équivalentes aux scripts JavaScript demandés
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "td:has(.bmi-ellipsis-h)"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Ajouter une ligne"]'))).click()
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.bmc-field div[aria-haspopup="listbox"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.bmc-field-select_dropdown_options-list-item[data-id="2"]'))).click()
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.bmc-calendar_sub-select div[aria-haspopup="listbox"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.bmc-field-select_dropdown_options-list-item[data-id="1"]'))).click()
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Remplir"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Valider"]'))).click()

    while True:
        time.sleep(1)
finally:
    driver.quit()
