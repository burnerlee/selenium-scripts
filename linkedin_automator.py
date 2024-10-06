from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from connection_profiles import PROFILE_LINKS
import time
import string

def remove_non_ascii(text):
    # Filter out non-ASCII characters
    return ''.join(char for char in text if char in string.printable)
profile_path = "/Users/burnerlee/Library/Application Support/Google/Chrome"
profile_directory = "Default"


options = webdriver.ChromeOptions()

selenium_service = Service('./chromedriver')
driver = webdriver.Chrome(service=selenium_service, options=options)
driver.get("https://www.linkedin.com/login")

username_field = driver.find_element(By.CSS_SELECTOR, "#username")
password_field = driver.find_element(By.CSS_SELECTOR, "#password")

username_field.send_keys("your-id")
password_field.send_keys("your-password")

sign_in_button = driver.find_element(By.CSS_SELECTOR, "#organic-div > form > div.login__form_action_container > button")
sign_in_button.click()


time.sleep(10)

for profile_link in PROFILE_LINKS:
    driver.get(profile_link)
    time.sleep(2)
    name_heading = driver.find_element(By.XPATH, "//*[contains(@id, 'ember')]/h1")
    full_name = remove_non_ascii(name_heading.text)
    first_name = full_name.split()[0]
    last_name = full_name.split()[1]
    print(first_name, last_name)
    more_button = driver.find_elements(By.XPATH, "//button[span[text()='More']]")
    for button in more_button:
        if button.is_displayed():
            button.click()
    time.sleep(1)
    connect_button = driver.find_elements(By.XPATH, f"//*[contains(@aria-label,\"Invite\") and contains(@aria-label,\"{first_name}\")]")
    for button in connect_button:
        print(button)
        if button.is_displayed():
            button.click()
    if len(connect_button) == 0:
        print("connect button not found, please check manually")
        print(profile_link)
        continue
    time.sleep(1)
    add_a_note_button = driver.find_element(By.XPATH, "//button[span[text()='Add a note']]")
    if add_a_note_button.is_displayed():
        add_a_note_button.click()
    time.sleep(1)
    note_text_area = driver.find_element(By.XPATH, "//*[@id='custom-message']")
    if note_text_area.is_displayed():
        note_text_area.send_keys(f"Hi {first_name}, I am expanding my network connecting with industry leaders and experts. Looking forward to stay in touch.")
    send_button = driver.find_element(By.XPATH, "//button[span[text()='Send']]")
    if send_button.is_displayed():
        print("send button is displayed")
        send_button.click()
    time.sleep(2)

time.sleep(1000)
driver.quit()
