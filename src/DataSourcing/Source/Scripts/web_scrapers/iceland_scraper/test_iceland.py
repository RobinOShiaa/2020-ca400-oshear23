import unittest
from Source.Scripts.web_scrapers import logger as l
from Source.Scripts.web_scrapers.iceland_scraper.iceland import iceland
import os

class Iceland_tests(unittest.TestCase):
    test = iceland()

    def test_scrape(self):
        logr = l.get_logger('Tesco Produce')
        self.test.scrape()
        assert os.path.exists('./iceland_csv/iceland.csv')
        logr.info('Iceland products CSV File created')


if __name__ == '__main__':
    unittest.main()