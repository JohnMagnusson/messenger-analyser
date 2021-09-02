"""
The message class represents a message that a user in the group chat has sent
"""


class Message:

    def __init__(self, timestamp, sender, reactions, content_type, content):
        """
        :param timestamp: When the message was sent in unix epoch time
        :param sender: The sender in the chat
        :param reactions: List of reactions the message received
        :param content_type: What kind of content the message is (TEXT, GIF, IMAGE....)
        :param content: The content the message carries
        """
        self.timestamp = timestamp
        self.sender = sender
        self.reactions = reactions
        self.content_type = content_type
        self.content = content
