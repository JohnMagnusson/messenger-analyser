from datetime import datetime, timedelta

from model.content_types import ContentType


class Analyser:

    def __init__(self, group_chat):
        self.group_chat = group_chat

    def get_number_messages_per_user(self):
        user_nr_messages = dict.fromkeys(self.group_chat.users, 0)
        for message in self.group_chat.messages:
            user_nr_messages[message.sender] += 1
        return user_nr_messages

    def get_message_length_per_user(self):
        """
        Gets the length of all messages user in the group has sent
        :return: dict(user, list(message_length))
        """

        user_message_lengths = {key: [] for key in self.group_chat.users}
        for message in self.group_chat.messages:
            if message.content_type == ContentType.TEXT:
                user_message_lengths[message.sender].append(len(message.content))
        return user_message_lengths

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

    def get_users_activity_over_time(self):
        """
        Gets the user activity of the chat since its creation
        :return: dict(datetime, dict(user_name, nr_messages_sent))
        """

        time_user_message = dict()
        for message in self.group_chat.messages:
            time = self.ts_to_datetime_day(message.timestamp)
            if time in time_user_message:
                time_user_message[time][message.sender] += 1
            else:
                time_user_message[time] = dict.fromkeys(self.group_chat.users, 0)
        return time_user_message

    def get_users_activity_under_week(self):
        """
        Gets the user activity of the chat aggregated into a week since the chats creation.
        The day is split into bins of each day of the week
        :return: dict(datetime, dict(user_name, nr_messages_sent))
        :return:
        """
        time_user_message = dict()
        for message in self.group_chat.messages:
            time = self.ts_to_weekday(message.timestamp)
            if time in time_user_message:
                time_user_message[time][message.sender] += 1
            else:
                time_user_message[time] = dict.fromkeys(self.group_chat.users, 0)
        return time_user_message


    def get_users_activity_under_day(self):
        """
        Gets the user activity of the chat aggregated into a day (24 hours) since the chats creation.
        The day is split into bins to be able to aggregate.
        :return: dict(datetime, dict(user_name, nr_messages_sent))
        :return:
        """
        time_user_message = dict()
        for message in self.group_chat.messages:
            time = self.ts_to_datetime_day_slot_bined_minute(message.timestamp, minute_bin=30)
            if time in time_user_message:
                time_user_message[time][message.sender] += 1
            else:
                time_user_message[time] = dict.fromkeys(self.group_chat.users, 0)
        return time_user_message

    def ts_to_datetime_all(self, ts):
        """
        Converts the timestamp to datetime object
        """
        return datetime.utcfromtimestamp(ts / 1000)

    def ts_to_datetime_day(self, ts):
        """
        Converts the timestamp to datetime object, only keeping year, month and day
        """
        return datetime.utcfromtimestamp(ts / 1000).replace(hour=0, minute=0, second=0, microsecond=0)

    def ts_to_weekday(self, ts):
        """
        Converts the timestamp to datetime object of the weekday
        """
        return datetime.utcfromtimestamp(ts / 1000).weekday()

    def ts_to_datetime_day_slot_bined_minute(self, ts, minute_bin=10):
        """
        Converts the timestamp to datetime object.
        It bins the values so they are all in the same day and in slots of 10 minutes
        """

        if minute_bin > 30:
            raise ValueError("Cannot have bins bigger than 30 minutes")

        dt = datetime.utcfromtimestamp(ts / 1000).replace(year=1900, month=1, day=1)
        discard = timedelta(minutes=dt.minute % minute_bin,
                            seconds=dt.second,
                            microseconds=dt.microsecond)
        dt -= discard
        if discard >= timedelta(minutes=minute_bin / 2):
            dt += timedelta(minutes=minute_bin)
        return dt
