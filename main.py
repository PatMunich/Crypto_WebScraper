import time
from WebScraper import WebScraper
from WorkbookEditor import WorkbookEditor
from TelegramManager import TelegramManager

# Defines
USER = 'Patrick'
TEST_MODE = False
DAY_IN_SECONDS = 10 #86400
ERROR_CODES = {'1': "[WebScraper error] trying to execute web-scraper!",
               '2': "[TelegramManager error] while trying to send daily rewards update message!"}
STATUS_CODES = {'1': f"[WebScraper status] result: "}
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
        if TelegramManager.sendMessage(data_set):
            pass
        else:
            print(ERROR_CODES['2'])
    else:
        TelegramManager.sendMessage(ERROR_CODES['1'], 'error')
        print(ERROR_CODES['1'])


if __name__ == '__main__':
    WebScraper = WebScraper(TARGET_WEBSITE, TEST_MODE)
    WorkbookEditor = WorkbookEditor()
    TelegramManager = TelegramManager(USER)
    while True:
        dailyUpdate()
        print('\n')
        time.sleep(DAY_IN_SECONDS)
