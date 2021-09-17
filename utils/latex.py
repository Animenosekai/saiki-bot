"""
Python LaTeX renderer

Credit to Jiangge Zhang (@tonyseek on GitHub)
> https://gist.github.com/tonyseek/95c90638cf43a87e723b
"""

from base64 import b64encode
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt

from utils.log import log

LOCAL_CACHE = {}

matplotlib.use("agg")
# plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"


def fix_string(string: str):
    string = str(string)
    for flag, replacement in [("\a", "\\a"), ("\b", "\\b"), ("\f", "\\f"), ("\n", "\\n"), ("\r", "\\r"), ("\t", "\\t"), ("\v", "\\v")]:
        string = string.replace(flag, replacement)
    return string


def render_latex(formula, fontsize=12, dpi=300, _format='svg'):
    """Renders LaTeX formula into image."""
    fig = plt.figure()
    try:
        #print("Formula", formula)
        text = fig.text(0, 0, formula, fontsize=fontsize)
    except:
        #print("Failed, trying with encoding")
        # print(formula.encode("utf-8"))
        text = fig.text(0, 0, formula.encode("utf-8"), fontsize=fontsize)

    fig.savefig(BytesIO(), dpi=dpi)  # triggers rendering

    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) + 0.05
    fig.set_size_inches((width, height))

    dy = (bbox.ymin / float(dpi)) / height
    text.set_position((0, -dy))

    buffer = BytesIO()
    transparent = _format != "jpg"

    fig.savefig(buffer, dpi=dpi, transparent=transparent, format=_format)
    plt.close(fig)

    return buffer.getvalue()


def render_discord_latex(formula: str):
    try:
        log("Rendering latex to base64")
        formula = str(formula)
        if not formula.startswith("$"):
            formula = "$" + formula + "$"
        return "data:image/png;base64, " + b64encode(render_latex(formula, fontsize=6, _format="png")).decode("utf-8")
    except Exception:
        return ""
