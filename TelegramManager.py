import requests

# Defines
BASE_URL = "https://api.telegram.org/bot"
UPDATE_ENDPOINT = "/getUpdates"
SEND_MESSAGE_ENDPOINT = "/sendMessage"


class TelegramManager:
    def __init__(self, in_user, in_test_mode):
        self.token = "init"
        self.chatId = 0
        self.selectChatId(in_user)
        self.url = f"{BASE_URL}{self.token}"
        self.offset = 0
        self.first_run = True
        self.last_message = {}
        self.TEST_MODE = in_test_mode

    def selectChatId(self, in_user):  # NOQA
        if in_user == "Patrick":
            self.chatId = "5494562569"
            self.token = "7577329762:AAGyWZHHKt12YeuziPbhzf8cRhuT8qYq5_U"
        else:
            pass

    def sendMessage(self, in_message, type='normal'):  # NOQA
        if not self.TEST_MODE:
            if type == 'normal':
                formatted_message = self.formatMessage(in_message)
                params = {"chat_id": f"{self.chatId}", "text": f"{formatted_message}"}
            else:
                params = {"chat_id": f"{self.chatId}", "text": f"{in_message}"}
            message = requests.post(f"{self.url}{SEND_MESSAGE_ENDPOINT}", params=params)  # NOQA
            return message.status_code
        else:
            return 0

    def formatMessage(self, in_message):  # NOQA
        keys = list(in_message.keys())
        if self.first_run:
            formatted_message = f"> daily subnet rewards < \n" \
                                f"▪ {keys[0]} : {in_message[keys[0]]} \n" \
                                f"▪ {keys[1]} : {in_message[keys[1]]} \n" \
                                f"▪ {keys[2]} : {in_message[keys[2]]} \n" \
                                f"▪ {keys[3]} : {in_message[keys[3]]} \n"
            self.first_run = False
        else:
            formatted_message = f"> daily subnet rewards < \n" \
                                f"▪ {keys[0]} : {in_message[keys[0]]} [+{in_message[keys[0]] - self.last_message[keys[0]]}]\n" \
                                f"▪ {keys[1]} : {in_message[keys[1]]} [+{in_message[keys[1]] - self.last_message[keys[1]]}]\n" \
                                f"▪ {keys[2]} : {in_message[keys[2]]} [+{in_message[keys[2]] - self.last_message[keys[2]]}]\n" \
                                f"▪ {keys[3]} : {in_message[keys[3]]} [+{in_message[keys[3]] - self.last_message[keys[3]]}]\n"
        self.last_message = in_message
        return formatted_message
