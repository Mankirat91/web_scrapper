from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time






options = Options()

options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)



driver.get("https://blinkit.com/s/?q=vegetables")



print("Scrolling to load more products...")
for _ in range(3):  # Try scrolling 5 times
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
   # Give time for new content to load after each scroll

# After scrolling, wait a bit more for final rendering
time.sleep(3)

try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="button" and .//img]'))
    )
except Exception as e:
    print("Products did not load:", e)

# Grab product cards
products = driver.find_elements(By.XPATH, '//div[@role="button" and .//img]')

                                
print(f"Found {len(products)} product card(s).\n")
product_data = []

for product in products:
    
    try:
        wait = WebDriverWait(product, 5)
        name = product.find_element(By.CLASS_NAME, "tw-line-clamp-2").text
        
        quantity = product.find_element(By.CLASS_NAME, "tw-line-clamp-1").text
        
        price = product.find_element(By.XPATH, ".//div[contains(@class, 'tw-text-200') and contains(@class, 'tw-font-semibold') and not(ancestor::div[contains(@class, 'tw-line-through')])]").text

        img = product.find_element(By.TAG_NAME,"img") 
        img_source = img.get_attribute('src')

        product_data.append({
            'Name':name,
            'Quantity':quantity,
            'Price':price,
            'Image_source':img_source
        })

   
         
    
    
    except Exception as e:
        print(f"An unexpected error occurred for Product Card : {e}. Skipping.")
        
   
        
driver.quit()
print(product_data)


