from scraper import final_data
# from detail import detail_data
import csv

product = final_data
if product:
    file_name = "blinkit_vegetables.csv"
    
    fields = ['Name', 'Quantity','Price','Thumbnail_Image','Full_Product_Image','Detailed_Description','Image_File_Name']

    try:
        csvfile = open(file_name, 'w', newline='', encoding='utf-8')

        writer = csv.DictWriter(csvfile,fieldnames=fields)

        writer.writeheader()
        writer.writerows(product)

        print(csvfile)


    except Exception as e:
        print(e) 