import sqlite3


def create_db():
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    qry ='CREATE TABLE IF NOT EXISTS vegetables ( id INTEGER PRIMARY KEY AUTOINCREMENT,Name TEXT,Qunatity INT,Price INT,Image_source VARCHAR(500))'
    cursor.execute(qry)
    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    for row in data:
        cursor.execute("SELECT Name FROM vegetables WHERE Name = ?", (row['Name'],))
        exist = cursor.fetchone()
        if exist:
            print(f"user with email {row['email']} already esixts.")
        else:
            qry = 'INSERT INTO vegetables (Name, Qunatity, Price, Image_source) VALUES (?,?,?,?)'
            index = (row['Name'], row['Quantity'], row['Price'], row['Image_source'])
            cursor.execute(qry,index)
            print("Data inserted sucessfuly")
    conn.commit()
    conn.close()
