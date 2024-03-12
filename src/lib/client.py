#from dotenv import load_dotenv
import asyncio
import base64
from gamercon_async import GameRCON, GameRCONBase64
from .config import PALWORLD_RCON_HOST, PALWORLD_RCON_PASSWORD, PALWORLD_RCON_PORT

#ENV_PATH = "/home/steam/.env"

class Rcon_Client:
    def __init__(self):
        self.timeout = 10

    def is_base64_encoded(self, s):
        try:
            return base64.b64encode(base64.b64decode(s)).decode() == s
        except Exception:
            return False

    async def rcon_command(self, command: str):

        async def send_command(ProtocolClass):
            async with ProtocolClass(PALWORLD_RCON_HOST, PALWORLD_RCON_PORT, PALWORLD_RCON_PASSWORD) as pc:
                return await asyncio.wait_for(pc.send(command), timeout=10)

        response = await send_command(GameRCON)
        
        if self.is_base64_encoded(self, response):
            response = await send_command(GameRCONBase64)

        return response
    
    async def shutdown(self, seconds=10, message="No reason specified"):
        print(f"Schedule server shutdown in {seconds} seconds")
        formated_message = message.replace(" ", "\u001f")
        response = await self.rcon_command(f"Shutdown {seconds} {formated_message}")
        return response