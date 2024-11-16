import os
import re
from datetime import datetime

def clean_description(description):
    description = re.sub(r'[^\w\s-]', '', description)
    description = re.sub(r'[-\s]+', '_', description)
    return description

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M')
