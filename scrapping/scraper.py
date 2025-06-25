from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests
import os
import re






options = Options()

options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)



driver.get("https://blinkit.com/s/?q=vegetables")


# last_height = driver.execute_script("return document.body.scrollHeight")

# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)
#     new_height = driver.execute_script("return document.body.scrollHeight")
    
#     if new_height == last_height:
#         break
#     last_height = new_height

print("Scrolling to load more products...")
for _ in range(3):  
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
   
time.sleep(3)

try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="button" and .//img]'))
    )
except Exception as e:
    print("Products did not load:", e)


products = driver.find_elements(By.XPATH, '//div[@role="button" and .//img]')

                                
print(f"Found {len(products)} product card(s).\n")
product_data = []

for product in products:
    
    try:
        
        name = product.find_element(By.CLASS_NAME, "tw-line-clamp-2").text
        
        quantity = product.find_element(By.CLASS_NAME, "tw-line-clamp-1").text
        
        price = product.find_element(By.XPATH, ".//div[contains(@class, 'tw-text-200') and contains(@class, 'tw-font-semibold') and not(ancestor::div[contains(@class, 'tw-line-through')])]").text

        img = product.find_element(By.TAG_NAME,"img") 
        img_source = img.get_attribute('src')

        product_id = product.get_attribute('id')

        detail_page_url = None 
        if product_id:
            detail_page_url = f"https://blinkit.com/prn/a/prid/{product_id}"
        else:
            print("not product id")

        product_data.append({
            'Name':name,
            'Quantity':quantity,
            'Price':price,
            'Image_source':img_source,
            'Detail_Page_URL': detail_page_url
        })
    except Exception as e:
        print(f"An unexpected error occurred for Product Card : {e}. Skipping.")
        
print(f"collected info of {len(product_data)} products")
        

final_data = []

if not os.path.exists('datasets/Images'):
    os.makedirs('datasets/Images')

def clean_name(name):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

for i in  product_data:
    detail_url = i['Detail_Page_URL']
    driver.get(detail_url)

    full_image_source = 'N/A'
    detailed_description = 'N/A'

    try:
        main_image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ProductCarousel__ImageContainer")]/div/img'))
        )
        full_image_source = main_image_element.get_attribute('src')

        if full_image_source:
            response = requests.get(full_image_source, stream=True)
            if response.status_code == 200:
                Img_name = clean_name(i['Name'])
                Img_path = f"datasets/Images/{Img_name}.jpg"
                with open (Img_path, 'wb') as out_file:
                    out_file.write(response.content)

            else:
                print(f"  Failed to download image for {i['Name']}")

        
    except TimeoutException:
        print("  Error: Main product image did not load on detail page within 10 seconds.")
    except Exception as e:
        print(f"  An unexpected error occurred getting full image: {e}")


    try:
        view_details = WebDriverWait(driver,5).until(
            EC.element_to_be_clickable((By.XPATH , '//button[.//div[text()="View more details"]]'))
        )
        view_details.click()
        time.sleep(1)  
    except TimeoutException:
        print("  Warning: 'View more details' button not found or clickable.")
    except Exception as e:
        print(f"  Unexpected error clicking 'View more details': {e}")
    try:
        description_heading_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "tw-text-300") and contains(@class, "tw-font-medium") and text()="Description"]'))
        )
        actual_description_element = description_heading_element.find_element(
            By.XPATH, './following-sibling::div[contains(@class, "tw-text-200") and contains(@class, "tw-font-regular") and contains(@class, "tw-whitespace-pre-wrap")]'
        )
        detailed_description = actual_description_element.text 
        
    except TimeoutException:
        print("  Error: 'Description' heading did not load on detail page within 10 seconds.")
    except NoSuchElementException:
        print("  Error: Actual description text element not found following the heading on detail page.")
    except Exception as e:
        print(f"  An unexpected error occurred extracting description: {e}")

    product_full_data = {
        'Name': i['Name'],
        'Quantity': i['Quantity'],
        'Price': i['Price'],
        'Thumbnail_Image': i['Image_source'],
        
        'Full_Product_Image': full_image_source,
        'Detailed_Description': detailed_description,
        'Image_File_Name': Img_name + ".jpg"
    }
    final_data.append(product_full_data)
    
driver.quit()
print(final_data)


