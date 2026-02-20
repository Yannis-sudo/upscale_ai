from src.images.load_hr import load_images#type:ignore
from src.images.create_lr import create_lr#type:ignore
import sys

# Scripts
# Load HR Images
def start_load_images(path):
    load_images(path)

# Create LR Images
def start_create_lr_images():
    create_lr()

# Get Argument
if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == "load_images":
        path = input("Path to image folder: ")
        start_load_images(path)
    elif arg == "create_lr_images":
        start_create_lr_images()
    else:
        print("No such Argument")