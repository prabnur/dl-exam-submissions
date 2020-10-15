import pathlib
from os import listdir, rename, makedirs
from os.path import isfile, join

# ADD NEWLY IDENTIFIED SUBMISSIONS TO ATTENDANCE

def extract_roll_no(field):
    match = re.search(r'140\d{3}', str(field))
    if match:
        return match.group(0)
    else:
        match = re.search(r'16\d{3}', str(field))
        if match:
            return match.group(0)
    return False


dumbasses = [
    1222872, 140661, 16434, 16417, 16644, 140742, 17719, 140587,
    16525, 16528, 16505, 1213791, 16485,
    16784, 16662, 140578, 16746, 16571,
    140734, 16806, 140425, 140433, 16475, 140576,
    140702, 16715, 1213838, 16730, 140732, 140727,
    16753, 16725, 16769, 140644, 16444, 16817,
    140398, 16869, 
    16446, 140724
]

smart = []

with open('Attendance.txt', 'r') as a:
    lines = a.readlines()
    smart = [int(line) for line in lines]

current_path = join(str(pathlib.Path().absolute()), 'numbered')
files = [f for f in listdir(current_path) if isfile(join(current_path, f))]
also_smart = []
for file in files:
    rno = extract_roll_no(filename)
    if rno:
        also_smart.append(int(rno))

print(current_path)
print(also_smarts)