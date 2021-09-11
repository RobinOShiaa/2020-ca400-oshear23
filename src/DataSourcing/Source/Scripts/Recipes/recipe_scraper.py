import time
from selenium import webdriver
import Source.Scripts.web_scrapers.scraper_tool as ST
from Source.Scripts.web_scrapers.logger import get_logger
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import csv

logger = get_logger('AllRecipes')

class Recipe_Scraper():
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=ST.path)
        self.driver.get('http://allrecipes.co.uk/recipes/')
        self.driver.maximize_window()
        self.data = {}
        self.recipes = []
        self.current_topic = 'Curry'



    def scrape(self):
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
            menus = [(i.get_attribute('href'),i.text) for i in self.driver.find_elements_by_xpath('//*[@id="hubsSimilar"]/div/div/h5/a')]
            logger.info('scraping')

            for index in menus:
                print(index[1])
                self.current_topic = index[1]
                with open('./Recipe_csv/{}.csv'.format(self.current_topic+ST.DATE), "w+", newline="", encoding="utf-8") as f:
                    logger.info("Creating new csv file")
                    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                    writer.writerow(["Category", "Recipe", "Recipe_url", "Image_url"])
                    self.driver.get(index[0])
                    time.sleep(3)
                    try:
                        self.driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                    except(NoSuchElementException):
                        print('no button')

                    self.driver.get(self.driver.current_url[0:self.driver.current_url.index('?')+1]+'Page=2')
                    final_count = self.driver.find_element_by_xpath('//*[@id="pageContent"]/div[1]/div[1]/div[3]/div').text
                    final_count = final_count.split('/')[-1].strip()
                    print(final_count)
                    self.scrape_products(final_count)

                    for row in self.recipes:
                        for data in row:
                            writer.writerow([self.current_topic] + [data,row[data][0],row[data][1]])

                    self.recipes = []






    def scrape_products(self,fc):

        time.sleep(3)
        try:

            self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/div[1]/div[1]/div[3]/a[1]').click()

            time.sleep(2)
            page_count = self.driver.find_element_by_xpath('//*[@id="pageContent"]/div[1]/div[1]/div[3]/div/span').text
            print(page_count)
            checkpoint_page = self.driver.current_url

            recipe = [i.get_attribute('href') for i in self.driver.find_elements_by_xpath('//*[@id="sectionTopRecipes"]/div/div[2]/h3/a')]
            print(recipe)
            recipe_name = [ST.clean(i.text) for i in self.driver.find_elements_by_xpath('//*[@id="sectionTopRecipes"]/div/div[2]/h3/a')]
            print(recipe_name)
            recipe_image = [i.get_attribute('src') for i in self.driver.find_elements_by_xpath('//*[@id="sectionTopRecipes"]/div/div[1]/a/img')]
            print(recipe_image)
            self.recipes.append( dict((z[0], list(z[1:])) for z in zip(recipe_name, recipe, recipe_image)))


            print(self.recipes)


            if page_count == fc:
                print('finished')
            else:
                self.scrape_products(fc)

        except(ConnectionResetError):
            self.driver.close()
            self.driver = webdriver.Chrome(executable_path=ST.path)
            self.driver.get(checkpoint_page)
            self.scrape_products(fc)

        except(NoSuchElementException):
            print('Finished')

        except(ElementClickInterceptedException):
            self.driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
            self.scrape_products(fc)









class Recipe():
    def __init__(self,link,image):

        self.link = link
        self.image = image
        self.driver = webdriver.Chrome(executable_path=ST.path)
        self.get_attributes()
        self.ingredients = self.get_ingredients()
        self.recipe_name = self.get_name
        self.filepath = self.get_image(self)


    def get_attributes(self):
        self.driver.get(self.link)
        time.sleep(3)

    def get_name(self):
        print(self.driver.find_element_by_xpath('//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[1]/div/div[2]/h1/span').text)
        return self.driver.find_element_by_xpath('//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[1]/div/div[2]/h1/span').text

    def get_ingredients(self):
        ingredients = [i.text for i in self.driver.find_elements_by_xpath('//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[2]/ul/li[1]')]
        print(ingredients)
        return ingredients

    def get_instructions(self):
        instructions = [i.text for i in self.driver.find_elements_by_xpath('//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[3]/ol/li/span')]
        print(instructions)
        return instructions

    def get_image(self):
        return ST.dl_jpg(self.image,'./Recipe_images/',self.recipe_name)






if __name__ == '__main__':
    Recipe_Scraper().scrape()



