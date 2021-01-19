from config import *
import minecraft_launcher_lib
import json

class Launcher:
    def __init__(self, play_name):
        self.play_name = play_name

    def getPath(self):
        with open(PROFILE_PATH, "r") as st_json:
            st_python = json.load(st_json)
        print(type(st_python))

    def run(self):
        minecraft_launcher_lib.utils.get_minecraft_directory()