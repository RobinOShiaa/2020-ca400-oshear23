import time
from selenium import webdriver
import Source.Scripts.web_scrapers.scraper_tool as ST
from Source.Scripts.web_scrapers.logger import get_logger
import csv
from Source.Scripts.web_scrapers.supervalue_scraper.supervalue_to_sql import Supervalue_sql

class Supervalue():




    def __init__(self):
        self.Data = []
        self.driver = webdriver.Chrome(
            executable_path=ST.path)
        self.driver.get('https://shop.supervalu.ie/shopping/')
        self.driver.maximize_window()
        self.urls = []
        self.logger = get_logger("Supervalue")



    def parse_products(self,link_url, save=()):
            attempts = 0
            save = set(save)
            if link_url:

                for i in link_url:
                    self.logger.info(i) #url
                    self.logger.info(i.split('/')[4])
                    self.logger.info(i)
                    if 'recipes'  == i.split('/')[4]:
                        self.logger.info(i.split('/')[4])  #only produce urls
                        continue


                    else:

                        self.driver.get(i)
                        time.sleep(2)
                        cat_urls = [i.get_attribute('href') for i in
                                    self.driver.find_elements_by_xpath('//a[@class="subcat-name "]')if 'recipes' not in i.get_attribute('href')]
                        if cat_urls:
                            try:
                                self.logger.info(cat_urls)
                                self.logger.info('sub_categorys')
                                product = [i.text for i in self.driver.find_elements_by_xpath('//div[@class = "product-list-item-details"]/a/h4[@class="product-list-item-details-title"]') if i.text not in save]
                                save.union(set(product))
                                price = [i.get_attribute('src') for i in self.driver.find_elements_by_xpath('//div[@class = "product-list-item-display"]/img')] #images
                                product_price = list(zip(product, price))
                                self.Data += product_price
                                current_index = link_url.index(i)
                                link_url = link_url[current_index+1:] + cat_urls
                                return self.parse_products(link_url, save)
                            except:
                                self.logger.info('Failed')
                                if attempts == 0:
                                    attempts += 1
                                    return self.parse_products(link_url,save)
                                else:
                                    continue

                        else:

                            product = [i.text for i in self.driver.find_elements_by_xpath('//div[@class = "product-list-item-details"]/a/h4[@class="product-list-item-details-title"]') if i.text not in save]
                            save.union(set(product))
                            price = [i.get_attribute('src') for i in self.driver.find_elements_by_xpath('//div[@class = "product-list-item-display"]/img')]
                            product_price = list(zip(product, price))
                            self.Data += product_price
                            self.logger.info(self.Data)

                return (self.Data)

    def parse_dropdown(self):
            dropdown = self.driver.find_elements_by_xpath('//*[@id="megaMenu"]/div[1]/a')
            for i in dropdown:
                if (i.get_attribute('href')):
                    self.logger.info(i.get_attribute('href'))
                    self.urls.append(i.get_attribute('href'))
                if (i.get_attribute('data-url')):
                    self.logger.info(i.get_attribute('data-url'))
                    self.urls.append(i.get_attribute('data-url'))
            return self.urls

    def parse_products_cat(self):
            self.logger.info(self.urls)
            for i in self.urls:
                self.logger.info(i)
                self.driver.get(i.replace("'", ''))
                time.sleep(2)
                prod = self.driver.find_elements_by_xpath(
                    '//div[@class = "product-list-item-details"]/a/h4[@class="product-list-item-details-title"]')
                if prod:
                    cat_urls = [i.get_attribute('href') for i in
                                self.driver.find_elements_by_xpath('//a[@class="subcat-name "]')if 'recipes' not in i.get_attribute('href')]

                    self.parse_products(cat_urls)
                else:
                    self.logger.info('images')
                    images = self.driver.find_elements_by_xpath("//div[@onclick]")
                    for j in images:
                        url = j.get_attribute('onclick')
                        url = url.split('=')[1]

                        if '{{' not in url:
                            if 'recipes' not in url:
                                url.replace("'", '')
                                self.logger.info('link receved from images' + url )
                                self.urls.append(url)


    def get_images(self): ####download images
        self.logger.info('#' * 32 + 'DOWNLOADING' + '#' * 32)
        with open('./supervalue_csv/supervalue{}.csv'.format(ST.DATE), "w+", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["Product", "Image_url", "Image_File_Path"])

            for name in self.Data:


                ST.dl_jpg(name[1], './supervalue_images/', name[0])
                full_path = ST.dl_jpg(name[1], './supervalue_images/', name[0])
                f.write("%s,%s,%s\n" % (name[0], name[1], full_path[0]))

    def scrape(self):


            self.driver.implicitly_wait(3)
            if (self.driver.find_element_by_id('simpleNotification')):

                self.driver.find_element_by_id('simpleNotificationClose').click()
                time.sleep(1)

                if (self.driver.find_element_by_class_name('modal-content')):
                    self.driver.find_element_by_class_name('takeover-modal-close').click()
                    time.sleep(1)
                    self.driver.find_element_by_xpath('//*[@id="menuToggle"]/span').click()

            self.parse_dropdown()
            self.parse_products_cat()

            self.get_images()







if __name__ == '__main__':
    Supervalue().scrape()
    Supervalue_sql().run()

