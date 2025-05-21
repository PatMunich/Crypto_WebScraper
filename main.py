import time
from WebScraper import WebScraper
from WorkbookEditor import WorkbookEditor
from TelegramManager import TelegramManager

# Defines
USER = 'Patrick'
# TEST_MODE = True
TEST_MODE = False
DAY_IN_SECONDS = 86400
TEST_CYCLE_TIME = 10
ERROR_CODES = {'1': "[WebScraper error] trying to execute web-scraper!",
               '2': "[TelegramManager error] while trying to send daily rewards update message!"}
STATUS_CODES = {'1': "[WebScraper status] result: ",
                '2': "[TelegramManager status] sending status message supressed due to test mode!]"}
TARGET_WEBSITE = 'https://backprop.finance/dtao/profile/5Cd5nSe1PzuGteZ3vSCZs8pcHxqy3wwmYcpHznK5Fbctu27W'

def dailyUpdate():  # NOQA
    WebScraper.getTimestamp()
    if WebScraper.loadWebsiteContent():
        WebScraper.trimWebsiteContent()
        WebScraper.formatListEntries()
        WebScraper.buildDictionary()
        print(STATUS_CODES['1'], dict(list(WebScraper.result_dict.items())))
        data_set = WebScraper.provideResultData()
        WorkbookEditor.sortInSubnetData(data_set)
        send_status = TelegramManager.sendMessage(data_set)
        if send_status:
            pass
        elif send_status == '0':
            print(STATUS_CODES['2'])
        else:
            print(ERROR_CODES['2'])
    else:
        TelegramManager.sendMessage(ERROR_CODES['1'], 'error')
        print(ERROR_CODES['1'])


if __name__ == '__main__':
    WebScraper = WebScraper(TARGET_WEBSITE, TEST_MODE)
    WorkbookEditor = WorkbookEditor()
    TelegramManager = TelegramManager(USER, TEST_MODE)
    while True:
        dailyUpdate()
        print('\n')
        if not TEST_MODE:
            time.sleep(DAY_IN_SECONDS)
        else:
            time.sleep(TEST_CYCLE_TIME)
