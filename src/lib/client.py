import os
import pathlib
#from dotenv import load_dotenv
from rcon import Console

ENV_PATH = "/home/steam/.env"
TIMOUT_DURATION = 3

class Client:
    def __init__(self):
        self.GENERIC_ERROR = "Unable to process your request (server did not respond)"
        print("Setting up RCON connection")
        #load_dotenv(ENV_PATH)

    def open(self) -> Console:
        return Console(
            host="127.0.0.1",
            password="Palworld",
            port=25575,
            timeout=TIMOUT_DURATION
        )
    
    def shutdown(self, seconds: str, message: str):
        print(f"Schedule server shutdown in {seconds} seconds")
        console = self.open()
        res = console.command(f"Shutdown {seconds} {message}")
        console.close()
        return res if res else self.GENERIC_ERROR