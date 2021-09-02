import glob
import json
import numpy as np
from model.message import Message
from model.reaction import Reaction
from model.group_chat import GroupChat
from model.content_types import ContentType


# The files are read in reverse order. That newer the file is the higher number the file has
# Furthermore, The newest is in the top of the file and oldest at the bottom.


class DataManager():

    def load_raw_message_files(self, folder_name):
        test = glob.glob("datasets/"+ folder_name + "/message_*")
        print(glob.glob("datasets"))
        users = set()

        messages = []
        for path in test:
            f = open (path, "r")
            data = json.loads(f.read())
            users.update(self.__get_participants_from_json(data["participants"]))
            messages.extend(self.__get_messages_from_json(data["messages"]))
        return GroupChat(users, messages)

    def __get_participants_from_json(self, json_participants):
        return [name["name"] for name in json_participants]

    def __get_messages_from_json(self, json_messages):
        messages = []
        for dict_message in json_messages:
            timestamp = dict_message["timestamp_ms"]
            sender = dict_message["sender_name"]
            reactions = self.__parse_reactions_from_json(dict_message)
            content_type = self.__parse_type_from_json(dict_message["type"], dict_message)
            content = self.__parse_content_from_json(content_type, dict_message)
            new_message = Message(timestamp, sender, reactions, content_type, content)
            messages.append(new_message)
        messages_array = np.array(messages)
        return messages_array

    def __parse_reactions_from_json(self, dict_message):
        if "reactions" in dict_message:
            reactions = []
            for reaction in dict_message["reactions"]:
                reactions.append(Reaction(reaction["actor"], reaction["reaction"]))
            return reactions
        return Reaction("", "")    # The case where no one reacted to the message

    def __parse_type_from_json(self, json_type, dict_message):
        """
        Converts facebook type to internal
        :param json_type: The type specified in the file
        :param dict_message: The whole dict used to find internal differences
        :return: An enum specifying the content type
        """
        if json_type == "Generic":  # Generic has multiple payloads we need to check
            if "sticker" in dict_message:
                return ContentType.STICKER
            elif "gifs" in dict_message:
                return ContentType.GIF
            elif "videos" in dict_message:
                return ContentType.VIDEO
            elif "photos" in dict_message:
                return ContentType.IMAGE
            elif "content" in dict_message:
                return ContentType.TEXT
            elif len(dict_message) == 3:        # The case where empty message, we verify by controlling nr fields
                return ContentType.EMPTY
            else:
                raise ValueError("The generic type had unknown payload, " + str(dict_message))
        elif json_type == "Share":
            return ContentType.SHARE
        elif json_type == "Call":
            return ContentType.CALL
        else:
            raise ValueError("Unsupported json type, " + str(json_type))

    def __parse_content_from_json(self, content_type, dict_message):
        return 0


    def format_raw_message_to_group_chat(self):
        return 0

    def load_group_chat(self):
        return 0

    def save_group_chat(self):
        return 0

    def save_new_group_chat(self, folder_name):
        # todo Find files from location given (files do need to be in project files dataset)
        self.load_raw_message_files(folder_name)
        # create a new groupchat object
        # save groupchat object
