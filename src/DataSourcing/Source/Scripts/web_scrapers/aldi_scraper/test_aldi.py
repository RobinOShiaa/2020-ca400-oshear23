import unittest
from Source.Scripts.web_scrapers import logger as l
from Source.Scripts.web_scrapers.aldi_scraper.aldi import Aldi
import os

class Aldi_tests(unittest.TestCase):
    test = Aldi()

    def test_scrape(self):
        logr = l.get_logger('Aldi Produce')
        self.test.scrape()
        assert os.path.exists('./aldi_csv/aldi.csv')
        logr.info('Aldi products CSV File created')


if __name__ == '__main__':
    unittest.main()