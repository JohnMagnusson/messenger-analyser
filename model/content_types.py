from enum import Enum


class ContentType(Enum):
    """
    The different types of content a message can carry
    """
    TEXT = 1
    SHARE = 2
    GIF = 3
    IMAGE = 4
    VIDEO = 5
    STICKER = 6
    EMPTY = 7
    CALL = 8
    SUBSCRIBE = 9
    AUDIO = 10
