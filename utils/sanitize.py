from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from urllib.parse import quote

from bs4 import BeautifulSoup
from config import BEAUTIFULSOUP_PARSER
from pylatexenc.latex2text import LatexNodes2Text

from utils.latex import render_discord_latex
from utils.log import log

pool = ThreadPool(100)
#pool = Pool(cpu_count())

LATEX_PARSER = LatexNodes2Text()

REMOVED_TAGS = ["span"]


def url_encode(text: str):
    log("URL Encoding {text}".format(text=text))
    return quote(str(text), safe='')


def render_math(content, math):
    math_string = str(math.text).strip()
    try:
        image_result = render_discord_latex(math_string)
        new_image = content.new_tag("img")
        new_image["src"] = image_result
        new_image["alt"] = math_string
    except Exception:
        new_image = content.new_tag("span")
        new_image["class"] = "saiki-math"
        try:
            new_image.string = LATEX_PARSER.latex_to_text(math_string)
        except Exception:
            new_image.string = math_string
    math.replace_with(new_image)
    return


def sanitize_html(html: str) -> str:
    log("Sanitizing HTML for Discord")
    content = BeautifulSoup(html.replace("\\\\", "\\"), BEAUTIFULSOUP_PARSER)
    for tag in REMOVED_TAGS:
        for element in content.select(tag):
            element.extract()

    pool.starmap(render_math, [(content, math)
                 for math in content.find_all("math")])

    return str(content)
