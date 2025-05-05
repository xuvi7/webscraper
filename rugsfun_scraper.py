import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without GUI
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.265 Safari/537.36"
)

load_dotenv()
file_path = os.getenv("DRIVER_PATH")

# Path to Chromedriver
service = Service(file_path)

try:
    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = "https://rugs.fun"

    history = []
    with open("game_history.txt", "r") as f:
        history = f.read().splitlines()
    
    # print(history)

    while (True):
        driver.get(url)
        
        # Wait for the required section to load (with the correct class name)
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.game-history-item"))
        )

        # Get the page source
        html = driver.page_source
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        
        # Locate the game history divs
        game_history = soup.select('.game-history-item')
        
        # Extract game history
        current_history = []
        for i, item in enumerate(game_history):  # Limit to top 10
            child = item.findChild("div")
            text_div = child.findChild("div")
            current_history.append(text_div.text.strip())

        if history == []:
            history = current_history
            print("set history to current_history")
        else:
            extended = False
            for i in range(len(current_history), 0, -1):
                match = True
                for j in range(i):
                    if current_history[j] != history[-i+j]:
                        match = False
                        break
                if match:
                    history.extend(current_history[i:])
                    extended = True
            if not extended:
                print("added entire current_history to history")
                history.extend(current_history)

        with open("game_history.txt", "w") as file:
            for item in history:
                file.write(item + "\n")

        time.sleep(60)
    
finally:
    # Close the WebDriver
    driver.quit()