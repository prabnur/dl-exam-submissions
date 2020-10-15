import pathlib
from os import listdir, rename, makedirs
from os.path import isfile, join
import re
from shutil import move
import json

"""

SORT ANY NEW FILES INTO THEIR CORRECT FOLDERS

"""


current_path = str(pathlib.Path().absolute())
ROOT_DIR = join('/Users', 'hartejbal', 'Documents', 'Exam Submissions')
REGULARS_DIR = 'Regulars'
REPEATS_DIR = 'Repeats'
UNIDENTIFIED_DIR = 'Unidentified'

proffs = {}
with open('proffs.json') as nf:
    proffs = json.load(nf)

def get_new_path(roll_no):
    if not roll_no:
        return join(ROOT_DIR, UNIDENTIFIED_DIR)
    if roll_no.startswith('14'):
        try:
            roll_no_int = int(roll_no)
        except:
            return join(ROOT_DIR, UNIDENTIFIED_DIR)
        for proff in proffs:
            if (proffs[proff]["start"] <= roll_no_int and roll_no_int <= proffs[proff]["end"]):
                return join(ROOT_DIR, proff, REPEATS_DIR)
    elif roll_no.startswith('16'):
        roll_no_int = int(roll_no)
        for proff in proffs:
            if(roll_no_int in proffs[proff]["regulars"]):
                return join(ROOT_DIR, proff, REGULARS_DIR)
    return join(ROOT_DIR, UNIDENTIFIED_DIR)

def extract_roll_no(field):
    match = re.search(r'140\d{3}', str(field))
    if match:
        return match.group(0)
    else:
        match = re.search(r'16\d{3}', str(field))
        if match:
            return match.group(0)
    return False

files = [f for f in listdir(current_path) if isfile(join(current_path, f))]

for filename in files:
    # Ignore these
    if(filename == 'order.py' or filename == 'proffs.json'):
        continue
    rno = extract_roll_no(filename)
    ext = filename.split('.')[-1]
    new_path = join(get_new_path(rno), f'{rno}.{ext}')
    old_path = join(current_path, filename)
    if (not old_path == new_path):
        try:
            rename(old_path, new_path)
        except:
            makedirs(get_new_path(rno))
            rename(old_path, new_path)

