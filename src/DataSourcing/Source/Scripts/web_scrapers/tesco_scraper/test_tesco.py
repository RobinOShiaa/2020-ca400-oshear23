import unittest
from Source.Scripts.web_scrapers import logger as l
from Source.Scripts.web_scrapers.tesco_scraper.tesco2 import Tesco
import os

class Tesco_tests(unittest.TestCase):
    test = Tesco()

    def test_scrape(self):
        logr = l.get_logger('Tesco Produce')
        self.test.scrape()
        assert os.path.exists('./tesco_csv/tesco.csv')
        logr.info('Tesco products CSV File created')


if __name__ == '__main__':
    unittest.main()