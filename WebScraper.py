import time
from time import sleep

import Tester
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class WebScraper:
    def __init__(self, in_website):
        # Defines
        self.SUCCESS_CODE = 200
        self.TEST_MODE = False
        self.TOTAL_SUBNETS = 4
        self.SEARCH_STRING_VALUES = '<span class="max-w-full truncate text-text-secondary">'
        self.SEARCH_STRING_NAMES = '<dt class="max-w-36 truncate font-medium lg:max-w-28 xl:max-w-36">'
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
        self.errorCodes_dict = {'1': "[WebScraper error] value in dict not correctly formatted!",
                                '2': "[WebScraper error] character in subnets list!"}
        self.Tester = Tester.Tester()

    def performanceTimerWebsiteLoading(self):  # NOQA
        if not self.TEST_MODE:
            start_request_time = time.time()
            self.response = requests.get(self.website)
            end_response_time = time.time()
            if self.response.status_code == self.SUCCESS_CODE:
                print("[WebScraper status] website successfully loaded within!")
                return True
            else:
                return False
        else:
            print("[WebScraper test mode] activated!")
            return True

    def getTimestamp(self):  # NOQA
        self.timestamp = datetime.now().strftime("%Y-%d/%m,%H:%M:%S")
        date = self.timestamp.split(',')[0]
        self.timestamp_year = date.split('-')[0]
        self.timestamp_day_month = date.split('-')[1]

    def trimWebsiteContent(self):
        if not self.TEST_MODE:
            soup = BeautifulSoup(self.response.content, 'html.parser')  # NOQA
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
        print(f"formatted values_list: {self.values_list}")
        for subnet in self.subnets_list:
            if subnet.find('\n') != -1:
                idx = subnet.find('\n')
                self.subnets_list[self.subnets_list.index(subnet)] = subnet[:idx]
        print(f"formatted subnets_list: {self.subnets_list}")

    def buildDictionary(self):  # NOQA
        idx = 0
        self.result_dict['0'] = self.timestamp_year
        self.result_dict['1'] = self.timestamp_day_month
        for subnet in self.subnets_list:
            self.result_dict[subnet] = round(float(self.values_list[idx]), 2)
            idx += 1

    def provideResultData(self):
        return self.result_dict
