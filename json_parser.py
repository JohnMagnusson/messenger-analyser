import numpy as np

from model.content_types import ContentType
from model.group_chat import GroupChat
from model.message import Message
from model.reaction import Reaction


class JsonParser:
    """
    Parses the facebook data files to a GroupChat object
    """

    def json_to_group_chat(self, data_files):
        users = set()
        messages = []
        for data in data_files:
            users.update(self.__get_participants_from_json(data["participants"]))
            messages.extend(self.__get_messages_from_json(data["messages"]))
        return GroupChat(users, np.array(messages))

    def __get_participants_from_json(self, json_participants):
        return [name["name"].encode("latin_1").decode("utf_8") for name in json_participants]

    def __get_messages_from_json(self, json_messages):
        messages = []
        for dict_message in json_messages:
            timestamp = dict_message["timestamp_ms"]
            sender = dict_message["sender_name"].encode("latin_1").decode("utf_8")  # Ensure name is correct
            reactions = self.__parse_reactions_from_json(dict_message)
            content_type = self.__parse_type_from_json(dict_message["type"], dict_message)
            content = self.__parse_content_from_json(content_type, dict_message)
            new_message = Message(timestamp, sender, reactions, content_type, content)
            messages.append(new_message)
        return messages

    def __parse_reactions_from_json(self, dict_message):
        if "reactions" in dict_message:
            reactions = []
            for reaction in dict_message["reactions"]:
                reactions.append(Reaction(reaction["actor"], reaction["reaction"]))
            return reactions
        return None  # The case where no one reacted to the message

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
            elif "audio_files" in dict_message:
                return ContentType.AUDIO
            elif len(dict_message) == 3:  # The case where empty message, we verify by controlling nr fields
                return ContentType.EMPTY
            else:  # Todo fortsätt med att fixa all olika möjlig data
                raise ValueError("The generic type had unknown payload, " + str(dict_message))
        elif json_type == "Share":
            return ContentType.SHARE
        elif json_type == "Call":
            return ContentType.CALL
        elif json_type == "Subscribe":
            return ContentType.SUBSCRIBE
        else:
            raise ValueError("Unsupported json type, " + str(json_type))

    def __parse_content_from_json(self, content_type, dict_message):
        """
        Parses the JSON to get information from the message depending on its type.
        :param content_type: The type of content
        :param dict_message: The json
        :return: The content of the message
        """

        if content_type == ContentType.TEXT:
            return dict_message["content"].encode("latin_1").decode("utf_8").lower()  # Fixing encoding of the data
        elif content_type == ContentType.SHARE:
            if "share" in dict_message:
                if "link" in dict_message["share"]:  # For sharing links
                    return dict_message["share"]["link"]
                elif "share_text" in dict_message["share"]:  # For sharing location
                    return dict_message["share"]["share_text"]
                else:
                    raise ValueError("The message had an unknown share content " + str(dict_message["share"]))
            else:
                if "content" in dict_message:
                    return dict_message["content"]
                else:
                    raise ValueError("The message was share classified but no content " + str(dict_message["share"]))
        elif content_type == ContentType.GIF:
            return self.__get_nested_uri(dict_message["gifs"])
        elif content_type == ContentType.IMAGE:
            return self.__get_nested_uri(dict_message["photos"])
        elif content_type == ContentType.VIDEO:
            return self.__get_nested_uri(dict_message["videos"])  # Only takes the uri, ignore ts of video and thumbnail
        elif content_type == ContentType.STICKER:
            return dict_message["sticker"]["uri"]
        elif content_type == ContentType.EMPTY:
            return "Empty"
        elif content_type == ContentType.CALL:
            return dict_message["call_duration"]  # Returns how long the call was
        elif content_type == ContentType.SUBSCRIBE:
            new_users = []
            for user in dict_message["users"]:
                new_users.append(user["name"])
            return new_users
        elif content_type == ContentType.AUDIO:
            return self.__get_nested_uri(dict_message["audio_files"])
        else:
            raise ValueError("content_type is not known" + str(content_type))

    def __get_nested_uri(self, data):
        entities = []
        for entity in data:
            entities.append(entity["uri"])  # Only takes the uri, ignore possibly other attribues
        return entities
