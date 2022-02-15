import os


DATA_FILE = 'WinNBQ.db3'
CODE_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
APP_PATH = os.path.dirname(CODE_FILE_PATH)
BACKEND_PATH = os.path.dirname(APP_PATH)
DATA_PATH = os.path.join(BACKEND_PATH, 'data')
DATA_FILE_PATH = os.path.join(DATA_PATH, DATA_FILE)


if __name__ == "__main__":
    print(DATA_FILE_PATH)
