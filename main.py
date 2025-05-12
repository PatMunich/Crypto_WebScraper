import time
import schedule
from WebScraper import WebScraper
from WorkbookEditor import WorkbookEditor
from TelegramManager import TelegramManager

# Defines
TARGET_WEBSITE = 'https://backprop.finance/dtao/profile/5Cd5nSe1PzuGteZ3vSCZs8pcHxqy3wwmYcpHznK5Fbctu27W'
USER = 'Patrick'
ERROR_CODES = {'1': "[WebScraper error] trying to execute web-scraper!"}
DAILY_UPDATE_TIME = '23:55'

def dailyUpdate():  # NOQA
    WebScraper.getTimestamp()
    if WebScraper.performanceTimerWebsiteLoading():
        WebScraper.trimWebsiteContent()
        WebScraper.getValuesBasedOnIndex('token_value')
        WebScraper.getValuesBasedOnIndex('token_name')
        WebScraper.formatListEntries('token_value')
        WebScraper.formatListEntries('token_name')
        WebScraper.buildDictionary()
        print(f"[WebScraper status] {WebScraper.timestamp} result: "
              f"{str(dict(list(WebScraper.result_dict.items())))}")
        data_set = WebScraper.provideResultData()
        WorkbookEditor.sortInSubnetData(data_set)
        if TelegramManager.sendMessage(data_set):
            pass
        else:
            print("[TelegramManager error] while trying to send daily rewards update message!")
    else:
        TelegramManager.sendMessage(ERROR_CODES['1'])
        print(ERROR_CODES['1'])


# Run script in background: nohup python2.7 MyScheduledProgram.py &
if __name__ == '__main__':
    WebScraper = WebScraper(TARGET_WEBSITE)
    WorkbookEditor = WorkbookEditor()
    TelegramManager = TelegramManager(USER)
    schedule.every().day.at(DAILY_UPDATE_TIME).do(dailyUpdate)
    while True:
        schedule.run_pending()
        time.sleep(240)
