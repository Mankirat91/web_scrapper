from db import create_db,insert_data
from dataextraction import read_csv
import os

if __name__ == "__main__":
    create_db()

    
    folder = "scrapping"
for name in os.listdir(folder): 
    if name.endswith('.csv'):
        path = os.path.join(folder,name)
        data = read_csv(path)
        insert_data(data)
        print(data)

    
