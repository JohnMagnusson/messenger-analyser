

class GroupChat:

    def __init__(self, users, messages):
        """
        Class representing the group chat in a format way.
        :param users: Set of users in the chat
        :param messages: List of messages sorted by time, newest first and oldest last
        """
        self.users = users
        self.messages = messages
        # addd dict with each user as key and there corresponidn gmessages