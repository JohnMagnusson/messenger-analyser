from model.content_types import ContentType

class Analyser:

    def __init__(self, group_chat):
        self.group_chat = group_chat

    def get_number_messages_per_user(self):
        user_nr_messages = dict.fromkeys(self.group_chat.users, 0)
        for message in self.group_chat.messages:
            user_nr_messages[message.sender] += 1
        return user_nr_messages

    def get_word_sent_dict(self):
        word_time = dict()
        for message in self.group_chat.messages:
            if message.content_type == ContentType.TEXT:
                words = message.content.split(" ")
                for word in words:
                    if word in word_time:
                        word_time[word].append(message.timestamp)
                    else:
                        word_time[word] = [message.timestamp]
        return word_time
