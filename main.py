from data_manager import DataManager
from analyser import Analyser

def main():
    data_manager = DataManager()
    data_manager.save_new_group_chat("di_amici_alvsjo")
    analyser = Analyser()

    analyser.hello_world()


if __name__ == '__main__':
    main()