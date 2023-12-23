""" Image text extractor module."""

# Image loader dependencies
from io import BytesIO
import re
from requests import Response, get
from PIL import Image

# Image text parser module
import pytesseract

# Debug loger module
from utils.logger import debug_output

def load_text_image(img_url: str) -> str:
    """ Gets text from image in given url."""
    # load attached image
    response: Response = get(img_url, timeout=60000)
    img = Image.open(BytesIO(response.content))
    img.load()
    if img is None: return ""

    # extract text from image
    text = pytesseract.image_to_string(img, lang="rus")
    text = re.sub("\n\n", "\n", text)
    text = re.sub("[^(\d)(\w)(\n)-,. %]|[_]", " ", text)
    text = re.sub("  ", " ", text)
    debug_output(f"Found text in picture: {text}", 1)
    return text
