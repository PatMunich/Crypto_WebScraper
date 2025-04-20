class Tester:
    def __init__(self):
        self.path_to_file = '/Users/patricksmacbookpro/Desktop/demo_website.rtf'

    def readFile(self):
        with open(self.path_to_file, 'r') as file:
            test_website = file.read()
        return test_website

# Findings
# [WebScraper status] 16/04 result: {'0': '2025', '1': '16/04', '64': '128.29', '19': '214.17', '56': '109\n  ', '4': '106.09'}
# [WebScraper status] 16/04 result: {'0': '2025', '1': '16/04', '64': '128.3\n', '19': '214.22', '56': '109.01', '4': '106.12'}
# [WebScraper status] 18/04 result: {'0': '2025', '1': '18/04', '64': '128.81', '19': '215.1\n', '56': '109.38', '4': '106.66'}