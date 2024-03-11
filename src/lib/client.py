#from dotenv import load_dotenv
from rcon import Client
from .check_uptime import tcp_ping

ENV_PATH = "/home/steam/.env"
TIMOUT_DURATION = 10
HOST="127.0.0.1"
PASSWORD="Palworld"
PORT=25575

class Console:
    # def __init__(self):
    #     self.GENERIC_ERROR = "Unable to process your request (server did not respond)"
    #     print("Setting up RCON connection")
    #     if tcp_ping(HOST,PORT):
    #         print("Connection successful.")
    #     else:
    #         print("Connection failed.")
    #     #load_dotenv(ENV_PATH)

    def open(self) -> Client:
        return Client(
            host=HOST,
            password=PASSWORD,
            port=PORT,
            timeout=TIMOUT_DURATION
        )
    
    def shutdown(self, seconds: str, message: str):
        print(f"Schedule server shutdown in {seconds} seconds")
        console = self.open()
        # res = console.run(f"Shutdown {seconds} {message}")
        res = console.run(command=f"Shutdown {seconds} {message}")
        console.close()
        return res if res else self.GENERIC_ERROR