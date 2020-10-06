
import pynput
from pynput.keyboard import Key, Listener
import logging

#log_directory = ""

#logging.basicConfig(filename="log_results.txt", level=logging.DEBUG)

def keypress(key):
    #logging.info(str(key))
    print(key);

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with Listener(on_press=keypress) as listener:
        listener.join()
