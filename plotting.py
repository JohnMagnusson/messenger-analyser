import matplotlib.pylab as plt
import matplotlib.ticker as mtick
import numpy as np


def plot_nr_messages_per_user(user_nr_messages, is_percent=True):
    x_axis = np.array(list(user_nr_messages.keys()))
    y_axis = np.array(list(user_nr_messages.values()))

    if is_percent:
        total = sum(y_axis)
        y_axis = y_axis / total

    x_y = zip(x_axis, y_axis)
    sorted_by_second = sorted(x_y, key=lambda tup: tup[1], reverse=True)
    labels, y = zip(*sorted_by_second)
    x = get_initials_from_names(labels)

    for i in range(len(x)):
        plt.bar(x[i], y[i], label=labels[i], align='center', alpha=0.8)

    plt.xlabel('Users initials')
    if is_percent:
        plt.ylabel('Percentage of messages sent')
        plt.title('The percentage of messages sent in the chat per user')
    else:
        plt.ylabel('Number of messages')
        plt.title('Number of messages sent in the chat per user')
    plt.legend(title="Name")

    plt.show()


def get_initials_from_names(names):
    initials = []
    for name in names:
        arr = name.split(" ")
        initials.append(arr[0][0] + arr[1][0])
    return initials


def plot_message_length_per_user(message_length_per_user):
    """
    Plots a bar diagram showing the mean, std and median message length per user in the chat.
    :param message_length_per_user: dict(user, messages lengths)
    """

    fig = plt.figure(1, (8, 6))
    ax = fig.add_subplot(1, 1, 1)

    names = get_initials_from_names(np.array(list(message_length_per_user.keys())))
    messages_length = np.array(list(message_length_per_user.values()))

    means, stds, medians = [], [], []
    for user_list in messages_length:
        means.append(np.mean(user_list))
        stds.append(np.std(user_list))
        medians.append(np.median(user_list))

    # Sort on median
    zipped = zip(names, means, stds, medians)
    sorted_by_second = sorted(zipped, key=lambda tup: tup[1], reverse=True)
    names, means, stds, medians = zip(*sorted_by_second)

    x_pos = np.arange(len(names))
    w = 0.4
    ax.bar(x_pos, means, width=w, yerr=stds, align='center', ecolor='black', capsize=5, label="Mean")
    ax.bar(x_pos + w, medians, width=w, align='center', label="Median")

    ax.set_ylabel('Messages length')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(names)
    ax.set_title('The average length of a message sent by an user')
    # ax.yaxis.grid(True)

    # Save the figure and show
    plt.legend()

    plt.tight_layout()
    plt.savefig("plots/average_length_of_message_for_users.png")
    plt.show()


def plot_most_used_words(word_times, nr_word_to_plot=10, is_percent=True):
    """
    Plots the most used words in a bar diagram.
    :param word_times: The dict containing the words with a list when they where used
    :param nr_word_to_plot: Number of words to show in the plot
    :param is_percent: bool flag if want to show number of times sent or the percentage out of all words
    """

    words = np.array(list(word_times.keys()))
    times_word_sent = np.array(list(word_times.values()))
    nr_times_word_sent = [len(nr_times) for nr_times in times_word_sent]

    words_times_word_sent_tuple = zip(words, nr_times_word_sent)
    sorted_by_second = sorted(words_times_word_sent_tuple, key=lambda tup: tup[1], reverse=True)
    cut_list = sorted_by_second[:nr_word_to_plot]
    x, y = zip(*cut_list)

    if is_percent:
        total = sum(nr_times_word_sent)
        y = (np.array(list(y)) / total) * 100

    fig = plt.figure(1, (8, 6))
    ax = fig.add_subplot(1, 1, 1)

    for i in range(len(x)):
        ax.bar(x[i], y[i], label=x[i], align='center', alpha=0.8)

    plt.xticks(rotation=90)
    if is_percent:
        plt.ylabel('Word representation %')
        plt.title('The representation of the top ' + str(nr_word_to_plot) + ' most used words')
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    else:
        plt.ylabel('Number of times word used')
        plt.title('The top ' + str(nr_word_to_plot) + ' most used words in the chat')

    plt.show()
