from difflib import SequenceMatcher
from pyjarowinkler import distance


stores = ['Supervalu','Tesco','Aldi','Iceland']
final_Store = ''

class Storesim():

    def __init__(self,store):
        self.store = store
        self.storelist = []
        self.actual = ''
        self.check()


    def check(self):
        if self.store in stores:
           self.actual = self.store
        else:
            self.storelist += stores
            self.similar()

    def similar(self):
        value = -100
        index = 0
        for i in stores:
            value1 = distance.get_jaro_distance(self.store, i, winkler=True)
            print(value1)
            print(type(value1))
            if value1 > value:
                value = value1
                self.actual = stores[index]

            index += 1
        print(self.actual)

