import sqlite3
import csv

class Supervalue_sql():

    def run(self):
        print('Writing to database..')
        conn = sqlite3.connect('../framework/Produce.db')
        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS Supervalue')
        cur.execute('''
        CREATE TABLE "Supervalue"(
            "Product_id" TEXT,
            "Image_Url" TEXT,
            "Image_Path" TEXT,
            "Image_Data" BLOP
        )
        ''')

        csv_name ='./supervalue_csv/supervalue.csv'
        with open(csv_name) as csv_file:
            csv_reader = csv.reader((csv_file))
            for row in csv_reader:
                try:

                    product_id = row[0]
                    image_url =  row[1]
                    image_path =  row[2]
                    with open(image_path,'rb') as f: ##obtain image data
                        data = f.read()
                    cur.execute('''INSERT INTO Supervalue(Product_id,Image_URL,Image_Path,Image_Data)
                            VALUES(?,?,?,?)''', (product_id, image_url, image_path, data))
                    conn.commit()

                except(OSError):
                    print(image_path) ##error string in csv
                except(FileNotFoundError):
                    print(image_path) ## image doesnt exist



        conn.close()

if __name__ == '__main__':
    Supervalue_sql().run()

