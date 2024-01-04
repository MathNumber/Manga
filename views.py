from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from unidecode import unidecode

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='myapp.log', filemode='w')
logger = logging.getLogger()

# Initialize Chrome browser
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

try:
    #so luong trang muon tim
    for page in range(1, 4):
        
        # Khi nao muon chuyen link tim truyen thi thay o day
        main_url = f"https://www.nettruyenbing.com/tim-truyen/manhwa-11400"
        
        url = f"{main_url}?page={page}"
        driver.get(url)
        truyen_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'item')]")))
        story_urls = [element.find_element(By.TAG_NAME, "a").get_attribute('href') for element in truyen_elements]

        for story_url in story_urls:
            driver.get(story_url)
            try:
                # Tim ten truyen
                title_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.title-detail")))
                title = unidecode(title_element.text)

                # Tim so sao
                rating_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@itemprop='ratingValue']")))
                rating = float(rating_element.text)

                # Tim luot theo doi
                view_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span > b")))
                view = int(view_element.text.replace(".",""))

                #Tim theo chapter
                chapter_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.col-xs-5 > a")))
                chapter = int(chapter_element.text.replace("Chapter",""))

                # Dieu kien de tim truyen
                if (rating >= 3.5) and (chapter>=30) and (view>10000):
                    print("Name:", title)
                    print("---")
            except Exception as e:
                logger.exception("Error processing story at {}: {}".format(story_url, str(e)))

except Exception as e:
    logger.exception("An error occurred: {}".format(str(e)))
    driver.quit()
