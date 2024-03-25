from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import logging
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException,ElementNotInteractableException,InvalidElementStateException,StaleElementReferenceException

def find_username_field(chromedriver_path):
    # Initialize Chrome WebDriver with the specified path
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)

    # Load the webpage containing the username field
    driver.get("URL_of_the_webpage_containing_the_field")

    try:
        # Find the username field by its ID
        username_field = driver.find_element(By.ID, "usernameField")
        print("Username field found:", username_field)
    except Exception as e:
        print("An error occurred while finding the username field:", e)
    finally:
        driver.quit()


def naukri_login(username, password, chromedriver_path):
    print("Initializing ChromeDriver service...")
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)
    print("ChromeDriver service initialized.")

    login_url = "https://www.naukri.com/nlogin/login"
    print(f"Loading login page: {login_url}")
    driver.get(login_url)
    print("Login page loaded successfully.")

    try:
        print("Waiting for the username field to be present...")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "usernameField"))
        )
        print("Username field found.")

        print("Filling username field...")
        username_field.send_keys(username)

        # Find and fill the password field
        print("Finding and filling password field...")
        password_field = driver.find_element(By.ID, "passwordField")
        password_field.send_keys(password)

        print("Clicking the login button...")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        print("Waiting for the page to load after login...")
        WebDriverWait(driver, 10).until(
            EC.title_contains("Jobseeker's Login")
        )

        print("Checking if login was successful...")
        if "Jobs" in driver.page_source:
            print("Login Successful")
            return driver
        else:
            print("Login Failed: Unable to find 'My Naukri' on the page.")
            return None
    except Exception as e:
        print("An error occurred during login:", e)
        return None

def print_sections(driver):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "widgetHead")))
        edit_section_elements = driver.find_elements(By.XPATH, "//div[@class='widgetHead']")

        if not edit_section_elements:
            print("No sections found.")
            return

        for element in edit_section_elements:
            section_name = element.text.strip()
            print("Section:", section_name)

            section_content = element.find_element(By.XPATH, "./following-sibling::div[1]").text.strip()
            print("Content:", section_content)
    except Exception as e:
        print("An error occurred while printing sections:", e)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def update_profile(driver, new_information):
    try:
        # Navigate to the profile edit page
        print("Navigating to the profile edit page...")
        profile_edit_url = "https://www.naukri.com/mnjuser/profile?id=&altresid"
        driver.get(profile_edit_url)

        # Wait for the profile edit page to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "widgetHead")))
        print("Profile edit page loaded successfully.")

        # Locate the section element
        section_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='lazyResumeHead']/div/div/div[1]/span[1]"))
        )
        print("Section element found.")

        # Locate the content element directly using XPath from the root
        content_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='lazyResumeHead']/div/div/div[1]/span[1]/../../following-sibling::div"))
        )
        print("Content element found.")

        # Clear the current content and enter the new one
        content_element.clear()
        content_element.send_keys("New resume headline")

        # Click the save button
        save_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "saveButton"))
        )
        save_button.click()

        print("Resume headline updated successfully.")

    except TimeoutException as e:
        print("Timeout occurred while waiting for an element:", e)
    except Exception as e:
        print("An error occurred while updating the profile:", e)

# Example usage

# Example usage
if __name__ == "__main__":
    username = "nandan10154@gmail.com"
    password = "7090811763"
    chromedriver_path = r"C:\Users\nanda\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    driver = naukri_login(username, password, chromedriver_path)
    update_profile(driver, {"resume_headline": "New resume headline"})
    driver.quit()


