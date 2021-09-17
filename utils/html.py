from imgkit import IMGKit

from utils.log import log

BASE_CSS = """\
* {
    font-family: 'SF Pro Display', 'Inter', 'Helvetica Neue', Helvetica, 'Open Sans', Arial, sans-serif;
    font-size: 22px;
}
h1 {
    font-size: 32px;
    margin-left: -10px;
    margin-top: 5px;
    margin-bottom: 10px;
}
h2 {
    font-size: 28px;
    font-weight: 500;
    margin-top: 20px;
    margin-bottom: 5px;
    margin-left: 15px;
}
img {
    vertical-align: bottom;
}
.content {
    padding-top: 25px;
    padding-left: 30px;
    padding-bottom: 25px;
    padding-right: 25px;
}
"""


def render(html: str, css: str = "", width: int = 1920):
    log("Rendering HTML to Image")
    rendering = f"""
<style>
    {BASE_CSS}
    {css}
</style>
<div class="content">
{html}
</div>
    """
    rtn = IMGKit(
        rendering,
        "string",
        options={'width': int(width)},
        toc=None,
        cover=None,
        css=None,
        config=None,
        cover_first=None,
    )
    return rtn.to_img()
