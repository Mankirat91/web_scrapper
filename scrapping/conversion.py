from .scraper import product_data
import csv

if product_data:
    file_name = "blinkit_vegetables.csv"
    
    fields = ['Name', 'Quantity','Price','Image_source']

    try:
        csvfile = open(file_name, 'w', newline='', encoding='utf-8')

        writer = csv.DictWriter(csvfile,fieldnames=fields)

        writer.writeheader()
        writer.writerows(product_data)

        print(csvfile)


    except Exception as e:
        print(e) 