import sys

# Information
SAIKI_BOT_VERSION = "1.0 (Beta)"
COMMAND_PREFIX = "!"

# Emoji Reaction
ROGER_REACTION = "<:easygif_roger:712005159676411914>"

# Request
REQUEST_CACHE_TTL = 3600
SAIKI_LLS_ENDPOINT = "https://saiki.vercel.app/api/lelivrescolaire?subject={subject}&class={class_name}&pages={pages}"
SAIKI_LATEX_ENDPOINT = "https://openacademy.vercel.app/api/math/latex?format=jpg&formula=${formula}$"

# HTML
BEAUTIFULSOUP_PARSER = "html.parser"

# Parameters
DEBUG_MODE = "-d" in sys.argv or "--debug" in sys.argv