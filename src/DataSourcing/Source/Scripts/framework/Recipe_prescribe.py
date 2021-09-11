import sqlite3
from sqlite3 import OperationalError
import random

class Recipe_P():

    def __init__(self,prodinput):
        self.con = sqlite3.connect('./Produce.db')
        onto = []
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.recipes = []

        for i in prodinput:
            print(i)
            try:
                self.cur.execute("SELECT Ontology from ontologies WHERE Product_id = '{}'".format(i))
            except(OperationalError):
                print(i)
            try:
                onto.append(self.cur.fetchone()[0])

            except(TypeError):
                print(i)
                print("None type")



        stmt = ""
        count = 0
        onto = [i for i in onto if i!= "null"]
        print(onto)
        for o in onto:
            if count == (len(onto)-1):
                stmt += "Select * from Recipes Where Ingredients LIKE '%{}%'".format(o)
            else:
                stmt += "Select * from Recipes Where Ingredients LIKE '%{}%' UNION ".format(o)
            count += 1

        print(count)
        print(stmt)
        print((len(onto) - 1))

        try:
            self.cur.execute(stmt)

        except(OperationalError):
            print(stmt)
            self.cur.execute(stmt)


        rows = self.cur.fetchall()
        for row in rows:
            self.recipes.append(row[1])

        random.shuffle(self.recipes)