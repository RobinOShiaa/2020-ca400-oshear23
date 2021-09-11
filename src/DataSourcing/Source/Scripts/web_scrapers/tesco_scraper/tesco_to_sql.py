import sqlite3
import csv


class Tesco_sql():

    def run(self):

        conn = sqlite3.connect('../Produce.db')
        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS Tesco')
        cur.execute('''
        CREATE TABLE "Tesco"(
            "Product_id" TEXT,
            "Image_Url" TEXT,
            "Image_Path" TEXT,
            "Image_Data" BLOP
        )
        ''')


        csv_name ='./tesco_csv/tesco.csv'


        with open(csv_name) as csv_file:
            csv_reader = csv.reader((csv_file))
            for row in csv_reader:
                try:

                    product_id = row[2]
                    image_url =  row[3]
                    image_path =  row[4]
                    with open(image_path+'.'
                                         'jpg','r',encoding='ISO-8859-1') as f:
                        data = f.read()
                    cur.execute('''INSERT INTO Tesco(Product_id,Image_URL,Image_Path,Image_Data)
                            VALUES(?,?,?,?)''', (product_id, image_url, image_path, data))
                    conn.commit()


                except(FileNotFoundError):
                    print(image_path)



        conn.close()

if __name__ == '__main__':
    Tesco_sql().run()
