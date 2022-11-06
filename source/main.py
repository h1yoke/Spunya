
import os
import discord
from dotenv import load_dotenv
from spunya import *

# NOTE: to run bot setup ".env" file:
# token="<discord api key>""
# prefix="<command prefix string>"

# main program entry
if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("token")
    prefix = os.getenv("prefix")
    if token == None or prefix == None:
        print(".env file is not setuped properly")
        exit()

    # run Spunya callback loop
    spunya = Spunya(prefix, intents=discord.Intents.all())
    spunya.run(token)
