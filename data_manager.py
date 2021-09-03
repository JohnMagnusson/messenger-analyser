import glob
import json
import pickle
from pathlib import Path

from json_parser import JsonParser


# The files are read in reverse order. That newer the file is the higher number the file has
# Furthermore, The newest is in the top of the file and oldest at the bottom.


class DataManager:

    def __init__(self):
        self.parser = JsonParser()

    def load_raw_message_files(self, folder_name):
        test = glob.glob("datasets/" + folder_name + "/message_*")
        print(glob.glob("datasets"))

        data = []
        for path in test:
            f = open(path, "r")
            data.append(json.loads(f.read()))
        return data

    def load_group_chat(self, file_name):
        """
        Loads the pickled file and returns a group_chat object
        :param file_name: The name of the file
        :return: GroupChat obj
        """

        file_to_read = open("group_chats/" + file_name + ".pickle", "rb")
        loaded_group_chat = pickle.load(file_to_read)
        file_to_read.close()
        print("Loaded " + file_name + " from disk")
        return loaded_group_chat

    def save_group_chat(self, file_name, group_chat):
        """
        Saves group chat object to disk in pickled format
        :param file_name: The file name
        :param group_chat: The object to be saved
        :return: null
        """

        Path("group_chats").mkdir(parents=True, exist_ok=True)
        file_pi = open("group_chats/" + file_name + ".pickle", 'wb')
        pickle.dump(group_chat, file_pi)
        print("Saved " + file_name + " to file...")

    def save_new_group_chat(self, folder_name, group_chat_name):
        """
        Loads all JSON files in the 'message_x" format, parses it and saves it to disk in a manageable format
        :param folder_name: The name where the JSON files are located
        :param group_chat_name: The given name of the group chat to save
        :return: null
        """

        # todo Find files from location given (files do need to be in project files dataset)
        data = self.load_raw_message_files(folder_name)
        group_chat = self.parser.json_to_group_chat(data)
        self.save_group_chat(group_chat_name, group_chat)
