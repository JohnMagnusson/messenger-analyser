import itertools

import matplotlib.dates as mdates
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
        plt.title('The percentage of messages sent in the chat')
    else:
        plt.ylabel('Number of messages')
        plt.title('Number of messages sent in the chat')
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

    ax.bar(x, y, label=x, align='center', alpha=0.8)

    plt.xticks(rotation=90)
    if is_percent:
        plt.ylabel('Word representation %')
        plt.title('The representation of the top ' + str(nr_word_to_plot) + ' most used words')
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    else:
        plt.ylabel('Number of times word used')
        plt.title('The top ' + str(nr_word_to_plot) + ' most used words in the chat')

    plt.show()


def plot_chat_activity_over_time(chat_activity, window_size=30):
    """
    Displays the chat activity for the chat
    :param chat_activity: Dict containing the activity for individuals over dates
    :param window_size: The windows size to run average on.
    """

    fig = plt.figure(1, (8, 6))
    ax = fig.add_subplot(1, 1, 1)

    date = np.array(list(chat_activity.keys()))
    messages_sent = [sum(name_dict.values()) for name_dict in chat_activity.values()]
    running_mean = np.convolve(messages_sent, np.ones(window_size) / window_size, mode='valid')

    cm = plt.get_cmap('Accent')

    ax.plot(date[window_size:], messages_sent[window_size:], label="Raw", color=cm(0.3), alpha=0.5)
    ax.plot(date[window_size - 1:], running_mean, label="Running mean", color=cm(0.5))
    ax.set_xlabel('Date')
    ax.set_ylabel('Average messages per day')
    plt.title('The chats activity over time. Running mean on  ' + str(window_size) + ' days')

    years = mdates.YearLocator()  # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    plt.grid()
    plt.legend()

    plt.savefig("plots/chat_activity.png")
    plt.show()


def plot_individuals_chat_activity_over_time(chat_activity, window_size=30):
    """
    Displays the chat activity for each individual in the chat
    :param chat_activity: Dict containing the activity for individuals over dates
    :param window_size: The windows size to run average on.
    """

    fig = plt.figure(1, (8, 6))
    ax = fig.add_subplot(1, 1, 1)
    cm = plt.get_cmap('viridis')

    date = np.array(list(chat_activity.keys()))
    names = list(list(chat_activity.values())[0].keys())
    unwrapped_values = [list(name_dict.values()) for name_dict in chat_activity.values()]
    users_messages_sent = list(map(list, itertools.zip_longest(*unwrapped_values, fillvalue=None)))

    ok = zip(names, users_messages_sent)
    sorted_by_second = sorted(ok, key=lambda tup: tup[0])
    names, users_messages_sent = zip(*sorted_by_second)

    running_means = []
    for user_messages in users_messages_sent:
        running_means.append(np.convolve(user_messages, np.ones(window_size) / window_size, mode='valid'))

    for i, running_mean in enumerate(running_means):
        # color = 1/len(names) +  i * 1/len(names)  # Cant decide on colour here :/
        # ax.plot(date[window_size - 1:], running_mean, label=names[i], color=cm(color))
        ax.plot(date[window_size - 1:], running_mean, label=names[i])

    ax.set_xlabel('Date')
    ax.set_ylabel('Average messages per day')
    plt.title('The chats activity over time. Running mean on ' + str(window_size) + ' days')

    years = mdates.YearLocator()  # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    plt.grid()
    plt.legend(title="names", loc="upper right")

    plt.savefig("plots/users_chat_activity.png")
    plt.show()


def plot_chat_activity_over_week(chat_activity, normalize=True):
    """
    Displays the chat activity for the chat aggregated over a week.
    :param chat_activity: Dict containing the activity for individuals over dates
    """

    fig = plt.figure(1, (8, 6))
    ax = fig.add_subplot(1, 1, 1)

    time = np.array(list(chat_activity.keys()))
    messages_sent = [sum(name_dict.values()) for name_dict in chat_activity.values()]

    # Sort so we get the weekday correct
    time, messages_sent = sort_values(time, messages_sent, 0)

    if normalize:
        messages_sent_arr = np.array(messages_sent)
        messages_sent = messages_sent_arr / sum(messages_sent_arr)

    cm = plt.get_cmap('Accent')

    ax.plot(time, messages_sent, color=cm(0.1), marker="o")
    ax.set_xlabel('Time')
    if normalize:
        ax.set_ylabel('Ratio of messages sent %')
    else:
        ax.set_ylabel('Messages sent')
    plt.title('The chats activity over a week')

    ax.set_xticklabels(["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    plt.grid()

    plt.savefig("plots/chat_activity_week.png")
    plt.show()


def plot_individuals_chat_activity_over_week(chat_activity, normalize=True):
    """
    Displays the chat activity for each user in the chat aggregated over a week.
    :param chat_activity: Dict containing the activity for individuals over dates.
    """

    fig = plt.figure(1, (8, 6))
    ax = fig.add_subplot(1, 1, 1)

    names = list(list(chat_activity.values())[0].keys())
    time = np.array(list(chat_activity.keys()))
    unwrapped_values = [list(name_dict.values()) for name_dict in chat_activity.values()]

    # Sort so we get the weekday correct
    time, day_user_sent = sort_values(time, unwrapped_values, 0)

    # Transpose so we get users as key with there entries as values
    users_messages_sent = list(map(list, itertools.zip_longest(*day_user_sent, fillvalue=None)))

    # Sort on name so we get them nicely in the legend
    names_sorted, users_messages_sent_sorted = sort_values(names, users_messages_sent, 0)

    # We normalize to see the relative difference in behaviour between the users
    if normalize:
        for i, user_messages_sent in enumerate(users_messages_sent_sorted):
            users_messages_sent_sorted[i] = np.array(user_messages_sent) / sum(user_messages_sent)

    # Plots
    for i in range(len(names)):
        ax.plot(time, users_messages_sent_sorted[i], label=names_sorted[i])

    ax.set_xlabel('Time')
    if normalize:
        ax.set_ylabel('Ratio of messages sent %')
    else:
        ax.set_ylabel('Messages sent')
    plt.title('The chats activity over a week')

    ax.set_xticklabels(["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    plt.grid()
    plt.legend(title="names", loc="upper right")
    plt.savefig("plots/users_chat_activity_week.png")
    plt.show()


def plot_chat_activity_under_day(chat_activity):
    """
    Displays the chat activity for the chat under 24 hours.
    :param chat_activity: Dict containing the activity for individuals over dates.
    """

    fig = plt.figure(1, (8, 6))
    ax = fig.add_subplot(1, 1, 1)

    time = np.array(list(chat_activity.keys()))
    messages_sent = [sum(name_dict.values()) for name_dict in chat_activity.values()]

    merged = zip(time, messages_sent)
    sorted_by_second = sorted(merged, key=lambda tup: tup[0])
    time, messages_sent = zip(*sorted_by_second)

    cm = plt.get_cmap('Accent')

    ax.plot(time, messages_sent, color=cm(0.1))
    ax.set_xlabel('Time')
    ax.set_ylabel('Messages sent in slot')
    plt.title('The chats activity over 24 hours')

    hours = mdates.HourLocator()  # every hour
    hours_fmt = mdates.DateFormatter('%H')

    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(hours_fmt)
    ax.xaxis.set_minor_locator(hours)

    plt.grid()

    plt.savefig("plots/chat_activity_24_hour.png")
    plt.show()


def plot_individuals_chat_activity_under_day(chat_activity, normalize=True):
    """
    Displays the chat activity for the chat under 24 hours.
    :param chat_activity: Dict containing the activity for individuals over dates.
    """

    fig = plt.figure(1, (8, 6))
    ax = fig.add_subplot(1, 1, 1)

    names = list(list(chat_activity.values())[0].keys())
    time = np.array(list(chat_activity.keys()))
    unwrapped_values = [list(name_dict.values()) for name_dict in chat_activity.values()]

    # sorts so the time is in order
    merged = zip(time, unwrapped_values)
    sorted_by_second = sorted(merged, key=lambda tup: tup[0])
    time, unwrapped_values = zip(*sorted_by_second)

    users_messages_sent = list(map(list, itertools.zip_longest(*unwrapped_values, fillvalue=None)))

    if normalize:
        for i, user_messages_sent in enumerate(users_messages_sent):
            cool = sum(user_messages_sent)
            tmp = np.array(user_messages_sent) / cool
            users_messages_sent[i] = tmp

    # sorts on name so we get them nicely in the legend
    merged = zip(names, users_messages_sent)
    sorted_by_second = sorted(merged, key=lambda tup: tup[0])
    names, users_messages_sent = zip(*sorted_by_second)

    cm = plt.get_cmap('Accent')

    for i in range(len(names)):
        ax.plot(time, users_messages_sent[i], label=names[i])

    ax.set_xlabel('Time')
    plt.title('The users chat activity over 24 hours')
    if normalize:
        ax.set_ylabel('Normalized message frequency in slot')
    else:
        ax.set_ylabel('Messages sent in slot')

    hours = mdates.HourLocator()  # every hour
    hours_fmt = mdates.DateFormatter('%H')

    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(hours_fmt)
    ax.xaxis.set_minor_locator(hours)

    plt.grid()

    plt.legend(title="names", loc="upper right")
    plt.savefig("plots/individuals_chat_activity_24_hour.png")
    plt.show()


def sort_values(v1, v2, index_to_sort_on):
    merged = zip(v1, v2)
    sorted_values = sorted(merged, key=lambda tup: tup[index_to_sort_on])
    v1_sorted, v2_sorted = zip(*sorted_values)
    return list(v1_sorted), list(v2_sorted)


def plot_chat_content_usage_group(content_usage, normalize=True):
    """
    Plots what type of content is sent in the group
    :param content_usage: The content sent
    :param normalize: If to show in normalized format or in numbers
    """

    fig = plt.figure(1, (8, 6))
    ax = fig.add_subplot(1, 1, 1)

    user_content = [list(content_usage[key].values()) for key in content_usage]
    content_user = list(map(list, itertools.zip_longest(*user_content, fillvalue=None)))  # transpose
    content_representation = [sum(content_usage) for content_usage in content_user]
    content_list = list(content_usage[list(content_usage.keys())[0]].keys())  # Gets the name of the content in order
    content_list_names = [content.name for content in content_list]

    x, y = sort_values(content_list_names, content_representation, index_to_sort_on=0)

    # Normalizes number to get a 0-100% interval
    if normalize:
        y_arr = np.array(y)
        y = y_arr / sum(y)

    ax.bar(x, y, align='center', ecolor='black')

    if normalize:
        ax.set_ylabel('Ratio of messages %')
    else:
        ax.set_ylabel('Number of messages')
    ax.set_title('What type of content is sent in the chat')
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    plt.savefig("plots/group_chat_content_usage.png")
    plt.show()


def plot_chat_content_usage_individual(content_usage, normalize=False):
    """
    Plots what type of content is sent in the group on individual basis
    :param content_usage: The content sent
    :param normalize: If to show in normalized format or in numbers
    """

    fig = plt.figure(1, (10, 6))
    ax = fig.add_subplot(1, 1, 1)

    content_list = list(content_usage[list(content_usage.keys())[0]].keys())  # Gets the name of the content in order
    content_list_names = [content.name for content in content_list]

    x, y, names = [], [], []

    x_pos = np.arange(len(content_list))
    w = 0.1
    start = np.floor(len(content_usage) / 2) * - w
    for i, user in enumerate(content_usage):
        step = start + w * i
        x_tmp, y_tmp = sort_values(content_list_names, list(content_usage[user].values()), index_to_sort_on=0)
        x.append(x_pos + step)
        y.append(y_tmp)
        names.append(user)

    # Sort on name
    test = zip(x, y, names)
    sorted_by_name = sorted(test, key=lambda tup: tup[2], reverse=False)
    x_sorted, y_sorted, name_sorted = zip(*sorted_by_name)

    # Plots the bars
    for i in range(len(x_sorted)):
        tmp_y = y_sorted[i]
        if normalize:
            tmp_y = normalize_values(tmp_y)
        ax.bar(x_sorted[i], tmp_y, width=w, align='center', ecolor='black', label=name_sorted[i])


    if normalize:
        ax.set_ylabel('Ratio of messages %')
        ax.set_title('What type of content users sends in the chat (normalized)')
    else:
        ax.set_ylabel('Number of messages')
        ax.set_title('What type of content users sends in the chat')

    ax.yaxis.grid(True)

    ax.set_xticks(x_pos)
    content_list_names.sort()  # To get them in order
    ax.set_xticklabels(content_list_names)
    plt.legend(title="Names")

    # Save the figure and show
    plt.tight_layout()
    plt.savefig("plots/group_chat_content_usage.png")
    plt.show()


def normalize_values(values):
    """
    Normalizes list
    :param values: values to normalize
    :return: normalized nump array
    """
    values_arr = np.array(values)
    return values_arr / sum(values)
