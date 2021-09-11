import unittest
from Source.Scripts.web_scrapers import logger as l
from Source.Scripts.web_scrapers.supervalue_scraper.supervalue import Supervalue
import os


class Supervalue_tests(unittest.TestCase):
    test = Supervalue()

    def test_scrape(self):
        logr = l.get_logger('Supervalue Produce')
        self.test.scrape()
        assert os.path.exists('./supervalue_csv/supervalue.csv')
        logr.info('Supervalue products CSV File created')


if __name__ == '__main__':
    unittest.main()