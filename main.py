from data_manager import DataManager
from analyser import Analyser
from plotting import *

def main():
    data_manager = DataManager()
    # data_manager.save_new_group_chat("di_amici_alvsjo", "test_alvsjo_1")
    group_chat = data_manager.load_group_chat("test_alvsjo_1")
    analyser = Analyser(group_chat)
    #
    # user_nr_messages = analyser.get_number_messages_per_user()
    # plot_nr_messages_per_user(user_nr_messages)
    #
    # word_sent = analyser.get_word_sent_dict()
    # plot_most_used_words(word_sent, 20)
    # #
    # message_length_per_user = analyser.get_message_length_per_user()
    # plot_message_length_per_user(message_length_per_user)
    #
    # chat_activity = analyser.get_users_activity_over_time()
    # plot_chat_activity(chat_activity)
    # plot_individuals_chat_activity(chat_activity)
    # ok = 3

if __name__ == '__main__':
    main()