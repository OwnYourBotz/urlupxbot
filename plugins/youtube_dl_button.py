import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import asyncio
import json
import os
import shutil
import time

if bool(os.environ.get("WEBHOOK", False)):
    from plugins.config import Config
else:
    from plugins.config import Config

from datetime import datetime
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from pyrogram.types import InputMediaPhoto

from plugins.translation import Translation
from functions.help_Nekmo_ffmpeg import generate_screen_shots
from functions.display_progress import progress_for_pyrogram, humanbytes

from PIL import Image


