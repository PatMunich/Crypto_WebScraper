class Tester:
    def __init__(self):
        self.path_to_file = '/Users/patrick/PycharmProjects/Crypto_WebScraper/Files/website_for_backtest.txt'

    def readFile(self):  # NOQA
        with open(self.path_to_file, 'r') as file:
            test_website = file.read()
        return test_website
