import pathlib
from os import listdir, rename, makedirs
from os.path import isfile, join

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

union = list(set(dumbasses) | set(smart))
union.sort()

with open('Attendance2.txt', 'w') as aa:
    for u in union:
        aa.write(str(u))
        aa.write('\n')
