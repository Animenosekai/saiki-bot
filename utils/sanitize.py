from urllib.parse import quote
from utils.latex import render_discord_latex

from bs4 import BeautifulSoup
from config import BEAUTIFULSOUP_PARSER

from utils.log import log

from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count

pool = ThreadPool(100)
#pool = Pool(cpu_count())

REMOVED_TAGS = ["span"]


def url_encode(text: str):
    log("URL Encoding {text}".format(text=text))
    return quote(str(text), safe='')

def render_math(content, math):
    new_image = content.new_tag("img")
    new_image["src"] = render_discord_latex(str(math.text).strip())
    new_image["alt"] = str(math.text).strip()
    math.replace_with(new_image)
    return 

def sanitize_html(html: str) -> str:
    log("Sanitizing HTML for Discord")
    content = BeautifulSoup(html.replace("\\\\", "\\"), BEAUTIFULSOUP_PARSER)
    for tag in REMOVED_TAGS:
        for element in content.select(tag):
            element.extract()

    pool.starmap(render_math, [(content, math) for math in content.find_all("math")])

    return str(content)
