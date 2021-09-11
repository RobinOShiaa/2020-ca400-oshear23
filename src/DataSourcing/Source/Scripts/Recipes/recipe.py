from os import listdir
from os.path import isfile, join
from Source.Scripts.web_scrapers.logger import get_logger
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import Source.Scripts.web_scrapers.scraper_tool as ST
from selenium.common.exceptions import InvalidArgumentException
import time


class Recipes():


    def scrape(self):


        logger = get_logger('Recipes')

        csv_files = [join('./Recipe_csv/', f) for f in listdir('./Recipe_csv/')]
        print(csv_files)
        driver = webdriver.Chrome(executable_path= ST.path)
        driver.maximize_window()
        with open('./Recipe{}.csv'.format(ST.DATE), "a",newline="",encoding='utf-8') as f:
            logger.info("Creating csv file")
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            #writer.writerow(["Category","Recipe_name","Ingredients","Instructions","Image_url","Image_Path"])
            for csv_file in csv_files[7:]:
                print(csv_file)
                with open(csv_file, "r", newline="", encoding="utf-8") as f:
                    logger.info("Reading csv file {}".format(csv_file))
                    csv_reader = csv.reader(f)
                    for line in csv_reader:
                        ingredient = []
                        instruction = []
                        try:
                            print(line[1],line[2],[line[3]])
                            driver.get(line[2])
                            time.sleep(2)
                            try:
                                driver.find_element_by_xpath('//*[@id="onetrust-close-btn-container"]/button').click()
                                time.sleep(4)

                            except:
                                print('nopopup')


                            soup = BeautifulSoup(driver.page_source, "lxml")
                            try:
                                ingredient = [i.text.strip() for i in soup.find("section", {"class": "recipeIngredients gridResponsive__module"}).find_all("li") if i != None]
                                print(ingredient)
                            except(AttributeError):
                                ingredient = [i.text for i in driver.find_elements_by_xpath('//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[2]/ul[1]/li/span')]
                                print(ingredient)

                            try:

                                instruction = ['(+) '+ i.text for  i in soup.find("section", {"class": "recipeDirections gridResponsive__module"}).find_all("li")if i!= None]
                                print(instruction)
                            except(AttributeError):
                                instruction = [i.text for i in driver.find_elements_by_xpath('//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[3]/ol/li/span')]
                                print(ingredient)

                            logger.info(instruction)
                            logger.info(ingredient)
                            time.sleep(1)
                            file_path = ST.dl_jpg(line[3],'./Recipe_images/',line[1])
                            print(file_path)


                            print('writing')
                            writer.writerow([line[0]] + [line[1]] + [str(ingredient)] + [str(instruction)] + [line[3]]+ [file_path[0]])
                            time.sleep(3)



                            print('finished succesfully')

                        except(InvalidArgumentException):
                            print('Title' + line[1],line[2],[line[3]])



if __name__ == '__main__':
    Recipes().scrape()



