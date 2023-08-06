import os
import sys
from pathlib import Path

from primaryschool.locale import _
from primaryschool.subjects import *

dir_path = Path(__file__).parent.absolute()
name_t = _("Math")
image_path = os.path.join(dir_path, "media", "img", "0x0.png")
