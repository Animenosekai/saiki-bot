import sys

from config import DEBUG_MODE, SAIKI_BOT_VERSION

if "-v" in sys.argv or "--version" in sys.argv:
    print(f"Saiki Discord Bot {SAIKI_BOT_VERSION}")
    quit()

if "-h" in sys.argv or "--help" in sys.argv:
    print()
    print("                SAIKI DISCORD BOT SERVER HELP CENTER")
    print()
    print(f"Saiki Discord {SAIKI_BOT_VERSION}")
    print(f"DEBUG_MODE: {DEBUG_MODE}")
    print("""
The main discord bot server for Saiki.

Args:
    --clear-log                     Clears the 'saiki_discord.log' file
    -h, --help                      Shows the Saiki Discord Bot Server Help Center and exits
    -d, --debug                     Launches Saiki Discord Server in DEBUG_MODE (note: --debug enables a higher debug level)
    -v, --version                   Shows the Server version and exits
""")
    quit()


from __protected import DISCORD_BOT_TOKEN
from saiki import client
from utils.log import log

log("Running the Discord Bot")
client.run(DISCORD_BOT_TOKEN)
