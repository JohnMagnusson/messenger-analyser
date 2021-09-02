class Reaction:

    def __init__(self, user, reaction):
        """
        :param user: The user who reacted
        :param reaction: What kind of reaction it is (smiley, heart etc.)
        """
        self.user = user
        self.reaction = reaction
