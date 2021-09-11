import time
from selenium import webdriver
from Source.Scripts.web_scrapers import scraper_tool as ST
from Source.Scripts.web_scrapers.logger import get_logger
import csv
from Source.Scripts.web_scrapers.iceland_scraper.iceland_to_sql import Iceland_sql

class iceland():



    def __init__(self):
        self.driver = webdriver.Chrome(
            executable_path=ST.path)
        self.groceries_url = 'https://www.iceland.co.uk/'
        self.driver.get(self.groceries_url)
        self.driver.maximize_window()
        time.sleep(1)
        bakery = 'BAK_nav_link'
        frozen = 'FRZ_nav_link'
        fresh = 'CHL_nav_link'
        food_cupboard = 'FDC_nav_link'
        self.categories = [fresh, frozen, food_cupboard, bakery]


    def scrape(self):
        logger = get_logger('Iceland')
        self.driver.find_element_by_xpath('//*[@id="navigation"]/div/div/div/ul/li/a').click()

        index = 0

        with open('./iceland_csv/iceland{}.csv'.format(ST.DATE), "w+", newline="", encoding="utf-8") as f:
            logger.info("Creating new csv file")
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["Category", "Product", "Image_url", "Image_File_Path"])

            for index in self.categories:


                lable = self.driver.find_element_by_id(index)
                logger.info(index)
                lable.click()
                self.driver.find_element_by_link_text('View all').click()


                while True:
                    time.sleep(5)
                    products_names = [i.find_element_by_tag_name('span').text for i in
                                      self.driver.find_elements_by_class_name('name-link')]
                    product_images = [i.get_attribute('srcset').split()[0] for i in
                                      self.driver.find_elements_by_class_name('thumb-link') if
                                      not (i.get_attribute('srcset') is None)]
                    logger.info(product_images)
                    logger.info(products_names)

                    product_image = dict(zip(products_names,product_images))
                    try:
                        file_paths = [ST.dl_jpg(product_image[i],'./iceland_images/', i) for i in product_image]
                    except:
                        print('error')

                    data = dict((z[0], list(z[1:])) for z in zip(products_names, product_images, file_paths))
                    print(data)
                    for row in data:
                        writer.writerow([row] + [data[row][0]] + [data[row][1][0]])

                    time.sleep(2)
                    try:
                        self.driver.find_element_by_xpath('//*[@id="primary"]/div[2]/div/div/nav/ul/li[3]/a').click()

                    except:
                        self.driver.get(self.groceries_url)
                        time.sleep(2)
                        self.driver.find_element_by_xpath('//*[@id="navigation"]/div/div/div/ul/li/a').click()
                        break


if __name__ == '__main__':
    iceland().scrape()
    Iceland_sql().run()