import sqlite3
import csv




class Iceland_sql():

    def run(self):

        conn = sqlite3.connect('../framework/Produce.db')
        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS Iceland')
        cur.execute('''
        CREATE TABLE "Iceland"(
            "Product_id" TEXT,
            "Image_Url" TEXT,
            "Image_Path" TEXT,
            "Image_Data" BLOP
        )
        ''')


        csv_name ='./iceland_csv/iceland.csv'


        with open(csv_name, encoding='utf-8') as csv_file:
            csv_reader = csv.reader((csv_file))
            for row in csv_reader:
                try:

                    product_id = row[0]
                    image_url =  row[1]
                    image_path =  row[2]
                    with open(image_path,'rb') as f:
                        data = f.read()
                    cur.execute('''INSERT INTO iceland(Product_id,Image_URL,Image_Path,Image_Data)
                            VALUES(?,?,?,?)''', (product_id, image_url, image_path, data))
                    conn.commit()


                except(FileNotFoundError):
                    print(image_path)




        conn.close()




