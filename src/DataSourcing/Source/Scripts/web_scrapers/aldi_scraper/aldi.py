import time
from selenium import webdriver
import os
from Source.Scripts.web_scrapers import scraper_tool as st
from Source.Scripts.web_scrapers.logger import get_logger
import csv

class Aldi():



    def scrape(self):

        logger = get_logger('Aldi')
        categories = []
        total = []
        driver = webdriver.Chrome(executable_path=st.path)
        driver.get('https://www.aldi.co.uk/c/groceries/groceriescategories')
        browse_by = driver.find_elements_by_xpath('/html/body/main/div[2]/div[5]/div[3]/div[1]/ul/li[2]/ul/li/div/a')
        for i in browse_by[:5]:
            name = i.text
            link = i.get_attribute('href')

            categories.append((name,link))

        logger.info(categories)

        for i in categories:
            driver.get(i[1])

            url = i[1].split('/')[-3:]
            update_url = ('/'+ ('/').join(url))
            logger.info(update_url)
            element = driver.find_element_by_css_selector("[title^='{}']".format(i[0]))

            elements = element.find_element_by_xpath("//following-sibling::ul[@class='category-facets__list category-facets__list--facet']")

            for i in elements.find_elements_by_tag_name('a'):

                sublink = i.get_attribute('href')
                subname = sublink.split('/')[-1]
                if '-' in subname:
                    subname = (' ').join(subname.split('-'))
                logger.info((subname,sublink))

            current = driver.find_elements_by_xpath('/html/body/main/div[2]/div[5]/div[3]/div[2]/div/h1/span')
            number_of_produce = current[0].text[2:-1]
            logger.info(number_of_produce)



            while True:

                links = [i.get_attribute('srcset').split(' ')[0][:-1] for i in driver.find_elements_by_xpath('/html/body/main/div[2]/div[5]/div[3]/div[2]/div/div[4]/div/a[2]/picture/source[1]')]

                products = [i.text for i in driver.find_elements_by_xpath('/html/body/main/div[2]/div[5]/div[3]/div[2]/div/div[4]/div/ul[2]/li[1]')]





                if len(products) == int(number_of_produce):

                    produce = products
                    logger.info(produce)
                    linkies = links
                    break


                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            logger.info('length of links list ' + str(len(links)))
            logger.info('length of produce list ' + str(len(produce)))


            total += zip(produce,linkies)

        logger.info('#' * 32 + 'DOWNLOADING' + '#' * 32)
        with open('./aldi_csv/aldi{}.csv'.format(st.DATE), "w+", newline="") as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow(["Product","Image_url","Image_File_Path"])

                for name in total:
                    st.dl_jpg(name[1], './aldi_images/', name[0])
                    full_path = st.dl_jpg(name[1], './aldi_images/', name[0])
                    f.write("%s,%s,%s\n" % (name[0], name[1], full_path))










if __name__ == '__main__':
    Aldi().scrape()