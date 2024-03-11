import time
import schedule
from src.lib.bot import PalBot
from src.lib.config import *
from lib.backup import zip_and_backup_palworld
from dotenv import load_dotenv

load_dotenv(".env")

schedule.every().hour.do(zip_and_backup_palworld)         # Schedule every hour

bot = PalBot()

bot.run(bot.token)

while True:
    schedule.run_pending()
    time.sleep(500)