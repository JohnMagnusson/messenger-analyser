from analyser import Analyser
from data_manager import DataManager
from plotting import *


def main():
    data_manager = DataManager()
    # data_manager.save_new_group_chat("di_amici_alvsjo", "test_alvsjo_1")
    group_chat = data_manager.load_group_chat("test_alvsjo_1")
    analyser = Analyser(group_chat)
    #
    # user_nr_messages = analyser.get_number_messages_per_user()
    # plot_nr_messages_per_user(user_nr_messages)
    # #
    # word_sent = analyser.get_word_sent_dict()
    # plot_most_used_words(word_sent, 30)
    # #
    # message_length_per_user = analyser.get_message_length_per_user()
    # plot_message_length_per_user(message_length_per_user)
    # #
    # chat_activity = analyser.get_users_activity_over_time()
    # plot_chat_activity_over_time(chat_activity)
    # plot_individuals_chat_activity_over_time(chat_activity)
    #
    # chat_activity = analyser.get_users_activity_under_week()
    # plot_chat_activity_over_week(chat_activity)
    # plot_individuals_chat_activity_over_week(chat_activity)
    #
    # chat_activity_during_day = analyser.get_users_activity_under_day()
    # plot_chat_activity_under_day(chat_activity_during_day)
    # plot_individuals_chat_activity_under_day(chat_activity_during_day)

    # Plotting what type of content users use
    content_usage = analyser.get_users_content_usage()
    plot_chat_content_usage_individual(content_usage)
    # plot_chat_content_usage_group(content_usage)

    # ok = 3


if __name__ == '__main__':
    main()
