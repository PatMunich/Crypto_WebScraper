import time
import Tester
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class WebScraper:
    def __init__(self, in_website):
        # Defines
        self.SUCCESS_CODE = 200
        self.TEST_MODE = False
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

    def performanceTimerWebsiteLoading(self):
        if not self.TEST_MODE:
            start_request_time = time.time()
            self.response = requests.get(self.website)
            end_response_time = time.time()
            if self.response.status_code == self.SUCCESS_CODE:
                print(f"[WebScraper status] website successfully loaded within "
                      f"{round(end_response_time - start_request_time, 2)} seconds!")
                return True
            else:
                return False
        else:
            print("[WebScraper test mode] activated!")
            return True

    def getTimestamp(self):
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

        idx_temp = website.find('Subnet breakdown')
        idx_fin = website.find('Subnet breakdown', idx_temp + 1)
        trimmed_content = website[idx_fin:]
        idx_pos = trimmed_content.find('Positions')
        idx_tra = trimmed_content.find('Transactions')
        self.trimmed_content = trimmed_content[idx_pos:idx_tra]

        pre_text_token_value = "runcate text-text-primary'><div class='inline'> <div class='inline'>"  # NOQA
        self.pre_token_value_offset = len(pre_text_token_value)
        post_text_token_value = "'\n                    "
        self.post_token_value_offset = len(post_text_token_value)
        pre_text_token_name = 'a class="truncate text-lg font-bold text-text-primary"'
        self.pre_token_name_offset = len(pre_text_token_name)

    def getValuesBasedOnIndex(self, in_scope):
        section = self.trimmed_content
        if in_scope == 'token_value':
            while section.find('truncate text-text-primary') > 0:
                idx = section.find('truncate text-text-primary')
                section = section[idx + self.pre_token_value_offset:]
                self.values_list.append(section[self.post_token_value_offset - 1:self.post_token_value_offset + 5])
        elif in_scope == 'token_name':
            while section.find('truncate text-lg font-bold text-text-primary') > 0:
                idx = section.find('truncate text-lg font-bold text-text-primary')
                section = section[idx + self.pre_token_name_offset:]
                self.subnets_list.append(section[self.post_token_name_offset - 1:self.post_token_name_offset + 1])
        else:
            pass

    def formatListEntries(self, in_scope):
        if in_scope == 'token_value':
            # print(f"[WebScraper debug] before formatting: {self.values_list}")
            for value in self.values_list:
                if value.find('\n') != -1:
                    idx = value.find('\n')
                    self.values_list[self.values_list.index(value)] = value[:idx]
            # print(f"[WebScraper debug] after formatting: {self.values_list}")
        elif in_scope == 'token_name':
            # print(f"[WebScraper debug] before formatting: {self.subnets_list}")
            for subnet in self.subnets_list:
                if subnet.find('-') != -1:
                    idx = subnet.find('-')
                    self.subnets_list[self.subnets_list.index(subnet)] = subnet[:idx]
            # print(f"[WebScraper debug] after formatting: {self.subnets_list}")
        else:
            pass

    def buildDictionary(self):
        idx = 0
        self.result_dict['0'] = self.timestamp_year
        self.result_dict['1'] = self.timestamp_day_month
        for subnet in self.subnets_list:
            self.result_dict[subnet] = round(float(self.values_list[idx]), 2)
            idx += 1

    def provideResultData(self):
        return self.result_dict
