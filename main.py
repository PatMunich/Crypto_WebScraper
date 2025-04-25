import time
from WebScraper import WebScraper
from WorkbookEditor import WorkbookEditor
from TelegramManager import TelegramManager

# Defines
TARGET_WEBSITE = 'https://backprop.finance/dtao/profile/5Cd5nSe1PzuGteZ3vSCZs8pcHxqy3wwmYcpHznK5Fbctu27W'
USER = 'Patrick'

if __name__ == '__main__':
    WebScraper = WebScraper(TARGET_WEBSITE)
    WorkbookEditor = WorkbookEditor()
    TelegramManager = TelegramManager(USER)
    while True:
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
            WorkbookEditor.sortInSubnetData(WebScraper.provideResultData())
            if TelegramManager.sendMessage(WebScraper.provideResultData()):
                pass
            else:
                print("[TelegramManager error] while trying to send daily rewards update message!")
        else:
            print(f"[WebScraper error] trying to execute web-scraper {str(WebScraper.response.status_code)}!")
        time.sleep(86400)
