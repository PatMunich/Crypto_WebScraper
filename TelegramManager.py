import requests

# Defines
BASE_URL = "https://api.telegram.org/bot"
UPDATE_ENDPOINT = "/getUpdates"
SEND_MESSAGE_ENDPOINT = "/sendMessage"
SUBNET_NAMES = {'4': "Targon", '19': "Nineteen", '56': "Gradients", '64': "Chutes"}


class TelegramManager:
    def __init__(self, in_user):
        self.token = "init"
        self.chatId = 0
        self.selectChatId(in_user)
        self.url = f"{BASE_URL}{self.token}"
        self.offset = 0
        self.firstRun = True

    def selectChatId(self, in_user):  # NOQA
        if in_user == "Patrick":
            self.chatId = "5494562569"
            self.token = "7577329762:AAGyWZHHKt12YeuziPbhzf8cRhuT8qYq5_U"
        else:
            pass

    def sendMessage(self, in_messageToSend):  # NOQA
        formatted_message = self.formatMessage(in_messageToSend)
        params = {"chat_id": f"{self.chatId}", "text": f"{formatted_message}"}
        message = requests.post(f"{self.url}{SEND_MESSAGE_ENDPOINT}", params=params)  # NOQA
        return message.status_code

    def formatMessage(self, in_message):  # NOQA
        keys = list(in_message.keys())
        formatted_message = f"> daily subnet rewards < \n" \
                            f"▪ {SUBNET_NAMES[keys[0]]} : {in_message[keys[0]]} \n" \
                            f"▪ {SUBNET_NAMES[keys[1]]} : {in_message[keys[1]]} \n" \
                            f"▪ {SUBNET_NAMES[keys[2]]} : {in_message[keys[2]]} \n" \
                            f"▪ {SUBNET_NAMES[keys[3]]} : {in_message[keys[3]]} \n"
        return formatted_message

    def getLastUpdateId(self, updates):  # NOQA
        updateIds = []
        for update in updates["result"]:
            updateIds.append(int(update["update_id"]))
        return max(updateIds)

    def updateBotNews(self):  # NOQA
        try:
            if self.offset > 0:
                message = requests.get(f"{self.url}{UPDATE_ENDPOINT}?offset={self.offset}")
            else:
                message = requests.get(f"{self.url}{UPDATE_ENDPOINT}")
        except Exception as e:  # NOQA
            return "no connection to server"

        updates = message.json()
        if len(updates["result"]) > 0:
            if self.firstRun:
                self.offset = self.getLastUpdateId(updates) + 1
                self.firstRun = False
                return "first run"
            else:
                self.offset = self.getLastUpdateId(updates) + 1
                return updates
        else:
            self.offset = 0
            return "empty message"

    def extractLastReceivedMessage(self):  # NOQA
        full_dict_text = self.updateBotNews()
        if full_dict_text != "no connection to server" and full_dict_text != "empty message":
            try:
                number_of_message_entries = len(full_dict_text['result'])
            except Exception as e:  # NOQA
                number_of_message_entries = 0

            if number_of_message_entries >= 1:
                if full_dict_text['result'][number_of_message_entries - 1]['message']['text'] == "send status" and \
                        full_dict_text['result'][number_of_message_entries - 1]['message']['chat']['id'] == int(self.chatId):
                    return "status"
                else:
                    pass  # NOQA
            else:
                return "nothing found"
        else:
            pass  # NOQA

    def sendRequestedStatusInformation(self, in_data):  # NOQA
        message_to_send = f"> {in_data} < \n" \
                        f"▪ : {in_data} \n" \
                        f"▪ : {in_data} \n"
        self.sendMessage(message_to_send)
