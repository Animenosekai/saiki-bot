import os
import subprocess
import tempfile
from pathlib import Path
from utils.log import log

WK_PATH = os.environ.get('WKHTMLTOIMAGE', str(
    Path(__file__).parent.resolve() / 'bin' / 'wkhtmltoimage'))
CACHE_DIR = Path(tempfile.gettempdir()) / 'saiki_cache'


def _execute_wk(*args, input=None):
    """
    Generate path for the wkhtmltoimage binary and execute command.

    :param args: args to pass straight to subprocess.Popen
    :return: stdout, stderr
    """
    wk_args = (WK_PATH,) + args
    log("Calling " + " ".join(wk_args))
    return subprocess.run(wk_args, input=input, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _convert_args(**py_args):
    cmd_args = []
    for name, value in py_args.items():
        if value in {None, False}:
            continue
        arg_name = '--' + name.replace('_', '-')
        if value is True:
            cmd_args.append(arg_name)
        else:
            cmd_args.extend([arg_name, str(value)])

    # read from stdin and write to stdout
    cmd_args.extend(['-', '-'])
    return cmd_args


def render_html(
        html, *,
        cache_dir: Path = CACHE_DIR,
        height: int = None,
        width: int = None,
        zoom: int = None,
        disable_javascript: bool = False,
        **extra_kwargs) -> bytes:
    """
    Generate a pdf from either a url or a html string.

    After the html and url arguments all other arguments are
    passed straight to wkhtmltoimage

    For details on extra arguments see the output of get_help()
    and get_extended_help()

    All arguments whether specified or caught with extra_kwargs are converted
    to command line args with "'--' + original_name.replace('_', '-')"

    Arguments which are True are passed with no value eg. just --quiet, False
    and None arguments are missed, everything else is passed with str(value).
    """
    if not cache_dir.exists():
        Path.mkdir(cache_dir)

    py_args = dict(
        cache_dir = cache_dir,
        height = height,
        width = width,
        zoom = zoom,
        disable_javascript = disable_javascript
    )
    py_args.update(extra_kwargs)
    cmd_args = _convert_args(**py_args)

    p = _execute_wk(*cmd_args, input=html.encode())
    pdf_content = p.stdout

    # it seems wkhtmltoimage's error codes can be false, we'll ignore them if we
    # seem to have generated a pdf
    if p.returncode != 0 and pdf_content[:4] != b'%PDF':
        raise RuntimeError('error running wkhtmltoimage, command: {!r}\n'
                           'response: "{}"'.format(cmd_args, p.stderr.decode().strip()))
    return pdf_content
