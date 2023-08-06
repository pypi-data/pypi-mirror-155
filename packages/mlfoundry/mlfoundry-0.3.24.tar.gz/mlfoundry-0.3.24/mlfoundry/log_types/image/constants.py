import posixpath
import re

IMAGE_LOG_DIR = posixpath.join("mlf", "run_logs", "images")
MEDIA_DIR = posixpath.join(IMAGE_LOG_DIR, "media")
DEFAULT_IMAGE_FORMAT = "png"
MISSING_PILLOW_PACKAGE_MESSAGE = (
    "We need PIL package to save image.\nTo install, run `pip install pillow`"
)
IMAGE_KEY_REGEX = re.compile(r"^[a-zA-Z0-9-_]+$")
