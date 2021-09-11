import sqlite3
from pyjarowinkler import distance
from pyjarowinkler.distance import JaroDistanceException

class Similarity():
    def __init__(self,table,word):
        self.prod_name = ''
        self.con = sqlite3.connect('./Produce.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        s_table = []

        score = 0
        word = word.replace('&', " ")
        keyword = word.split()

        for i in keyword:
            try:
                self.cur.execute("SELECT DISTINCT Product_id from {} WHERE Product_id LIKE '%{}%'".format(table,keyword[0]))

            except(IndexError):
                continue
            rows = self.cur.fetchall()
            if len(rows) > score:
                score = len(rows)
                s_table = rows


        if len(s_table) is 0:
            try:
                self.cur.execute("SELECT DISTINCT Product_id from {} WHERE Product_id LIKE '{}%{}%'".format(table, keyword[0][0],keyword[0][1]))
                s_table = self.cur.fetchall()
            except(IndexError):
                self.cur.execute("SELECT DISTINCT Product_id from {} WHERE Product_id LIKE '{}%{}%'".format(table, keyword[0][0]))
                s_table = self.cur.fetchall()


        self.product_ids = []
        for row in s_table:
            self.product_ids.append(row[0])
        self.check_valid(word)

    def check_valid(self,word):
        if word in self.product_ids:
            self.compare_string = word

        else:
            self.disect(word)

    def disect(self,word):
        value = 0
        index = 0
        for i in self.product_ids:
            try:
                value1 = distance.get_jaro_distance(word,i,winkler=True)
            except(JaroDistanceException):
                break

            if value1 > value:
                value = value1
                self.prod_name = self.product_ids[index]

            index += 1

        self.con.close()

    def __str__(self):
        return self.prod_name






