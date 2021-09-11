import sqlite3
import csv
import os
from Source.Scripts.web_scrapers import scraper_tool as ST
from pathlib import Path


class Recipe_sql():

    def run(self):

        conn = sqlite3.connect('../framework/Produce.db')
        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS Recipes')
        cur.execute('''
        CREATE TABLE "Recipes"(
            "Category" TEXT,
            "Recipe_id" TEXT,
            "Ingredients",TEXT,
            "Instructions" TEXT,
            "Image_Url" TEXT,
            "Image_Path" TEXT,
            "Image_Data" BLOP
        )
        ''')


        csv_name ='./Recipe_4_11_2020.csv'

        print(os.listdir('./Recipe_images'))
        with open(csv_name,encoding='utf-8') as csv_file:
            csv_reader = csv.reader((csv_file))
            for row in csv_reader:
                        index = 0


                        category = row[0]
                        #print(category)
                        recipe_id = row[1]
                        #print(recipe_id)
                        ingredients = row[2]
                        #print(ingredients)
                        instructions = row[3]
                        #print(instructions)
                        image_url =  row[4]

                        image_path =  row[5]
                        config = Path(image_path)
                        if config.is_file():

                                with open(image_path,'rb') as f:
                                    data = f.read()
                                    cur.execute('''INSERT INTO Recipes(Category,Recipe_id,Ingredients,Instructions,Image_Url,Image_Path,Image_Data)
                                    VALUES(?,?,?,?,?,?,?)''', (category,recipe_id,ingredients,instructions,image_url, image_path, data))
                                    conn.commit()

                        else:
                            print('not Found ' +image_path)



            conn.close()

if __name__ == '__main__':
    Recipe_sql().run()

