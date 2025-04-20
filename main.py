import time

from WebScraper import WebScraper
from WorkbookEditor import WorkbookEditor

# Defines
target_website = 'https://backprop.finance/dtao/profile/5Cd5nSe1PzuGteZ3vSCZs8pcHxqy3wwmYcpHznK5Fbctu27W'

if __name__ == '__main__':
    WebScraper = WebScraper(target_website)
    WorkbookEditor = WorkbookEditor()
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
        else:
            print(f"[WebScraper error] trying to execute web-scraper {str(WebScraper.response.status_code)}")
        time.sleep(10)
