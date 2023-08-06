import os
import sys

media_path = os.path.abspath(os.path.dirname(__file__))
image_path = os.path.join(media_path, "img")

default_score_surface_pass_bg_path = os.path.join(image_path, "0x0.png")
default_score_surface_not_pass_bg_path = os.path.join(image_path, "0x1.png")
