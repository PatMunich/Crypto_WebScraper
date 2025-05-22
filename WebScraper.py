import Tester
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class WebScraper:
    def __init__(self, in_website, in_test_mode):
        # Defines
        self.SUCCESS_CODE = 200
        self.TOTAL_SUBNETS = 4
        self.TEST_MODE = in_test_mode
        self.LOG_WEBSITE = False
        self.SEARCH_STRING_VALUES = '<span class="max-w-full truncate text-text-secondary">'
        self.SEARCH_STRING_NAMES = '<dt class="max-w-36 truncate font-medium lg:max-w-28 xl:max-w-36">'
        self.ERROR_CODES = {'1': "[WebScraper error] value in dict not correctly formatted!",
                            '2': "[WebScraper error] character in subnets list!"}
        self.STATUS_CODES = {'1': "[WebScraper status] website successfully loaded!",
                             '2': "[WebScraper test mode] activated!"}
        # Variables
        self.website = in_website
        self.response = ''
        self.timestamp = ''
        self.timestamp_year = ''
        self.timestamp_day_month = ''
        self.trimmed_content = ''
        self.pre_token_value_offset = 0
        self.post_token_value_offset = 0
        self.pre_token_name_offset = 0
        self.post_token_name_offset = 13
        self.values_list = []
        self.subnets_list = []
        self.result_dict = {}
        self.Tester = Tester.Tester()
        self.path_to_file = 'Files/website_for_backtest.txt'

    def getTimestamp(self):  # NOQA
        self.timestamp = datetime.now().strftime("%Y-%d/%m,%H:%M:%S")
        date = self.timestamp.split(',')[0]
        self.timestamp_year = date.split('-')[0]
        self.timestamp_day_month = date.split('-')[1]

    def loadWebsiteContent(self):  # NOQA
        if not self.TEST_MODE:
            self.response = requests.get(self.website)
            if self.response.status_code == self.SUCCESS_CODE:
                print(self.STATUS_CODES['1'])
                return True
            else:
                return False
        else:
            print(self.STATUS_CODES['2'])
            return True

    def trimWebsiteContent(self):  # NOQA
        if not self.TEST_MODE:
            soup = BeautifulSoup(self.response.content, 'html.parser')  # NOQA
            if self.LOG_WEBSITE:
                with open(self.path_to_file, "w") as f:
                    f.write(str(soup))
        else:
            soup = BeautifulSoup(self.Tester.readFile(), 'html.parser')
        website = str(soup.prettify())
        # Get Subnet Values
        temp_content = website
        self.values_list = []
        for i in range(self.TOTAL_SUBNETS):  # NOQA
            trim_idx = temp_content.find(self.SEARCH_STRING_VALUES)
            self.values_list.append(temp_content[trim_idx+113:trim_idx+119])
            temp_content = temp_content[trim_idx+1:]
        # Get Subnet Names
        self.subnets_list = []
        temp_content = website
        for i in range(self.TOTAL_SUBNETS):  # NOQA
            trim_idx = temp_content.find(self.SEARCH_STRING_NAMES)
            self.subnets_list.append(temp_content[trim_idx+79:trim_idx+88])
            temp_content = temp_content[trim_idx+1:]

    def formatListEntries(self):  # NOQA
        for value in self.values_list:
            if value.find('\n') != -1:
                idx = value.find('\n')
                self.values_list[self.values_list.index(value)] = value[:idx]
        for subnet in self.subnets_list:
            if subnet.find('\n') != -1:
                idx = subnet.find('\n')
                self.subnets_list[self.subnets_list.index(subnet)] = subnet[:idx]

    def buildDictionary(self):  # NOQA
        idx = 0
        self.result_dict['0'] = self.timestamp_year
        self.result_dict['1'] = self.timestamp_day_month
        for subnet in self.subnets_list:
            self.result_dict[subnet] = round(float(self.values_list[idx]), 2)
            idx += 1

    def provideResultData(self):  # NOQA
        return self.result_dict
