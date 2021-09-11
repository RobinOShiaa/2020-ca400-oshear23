import sqlite3
import csv

class aldi_sql():

    def run(self):

        conn = sqlite3.connect('../framework/Produce.db')
        cur = conn.cursor()
        sql = 'SELECT * FROM Aldi'
        cur.execute(sql)
        rows = cur.fetchall()

        conn2 = sqlite3.connect('../Produce.db')
        cur2 = conn2.cursor()

        cur2.execute('DROP TABLE IF EXISTS Aldi')
        cur2.execute('''
        CREATE TABLE "Aldi"(
            "Product_id" TEXT,
            "Image_Url" TEXT,
            "Image_Path" TEXT,
            "Image_Data" BLOP
        )
        ''')

        for row in rows:
            product_id = row[0]
            image_url = row[1]
            image_path = row[2]
            data = row[3]
            cur2.execute('''INSERT INTO Aldi(Product_id,Image_URL,Image_Path,Image_Data)
                            VALUES(?,?,?,?)''', (product_id, image_url, image_path, data))
            conn2.commit()
        conn.close()
        conn2.close()




