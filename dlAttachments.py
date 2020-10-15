import datetime
import json
import os
import re
import sys

from oauth2 import RefreshToken
from imap_tools import MailBox, AND
from tracker import Tracker

# Parameters
LIMIT = -1
sent_date = datetime.date(2020, 10, 3)

# Constants
CONFIG = {}
with open('config.json') as f:
    CONFIG = json.load(f)
EMAIL_LINK = CONFIG['EMAIL_LINK']
EMAIL = CONFIG['EMAIL']
client_id = CONFIG['client_id']
client_secret = CONFIG['client_secret']

now = datetime.datetime.now()
ROOT_DIR = os.path.join('.', 'Attachments_{0}'.format(now.strftime('%c').replace(':', '_')))
REGULARS_DIR = 'Regulars'
REPEATS_DIR = 'Repeats'
UNIDENTIFIED_DIR = 'Unidentified'

# Setup
proffs = {}
with open('proffs.json') as f:
    proffs = json.load(f)
attendance = []
no_attachments = []

# TOKEN WORK

refresh_token = b''
with open('refreshToken', 'r') as refreshTokenFile:
    refresh_token = refreshTokenFile.read()
try:
    print()
    print('Fetching new token for authentication')
    response = RefreshToken(client_id, client_secret, refresh_token)
except Exception as e:
    print(e)
    sys.exit(1)
access_token = response['access_token']
print('Fetched')

# HELPERS

def extract_roll_no(email): # Find roll number
	fields = [msg.subject]
	fields += [att.filename for att in msg.attachments]
	fields += [msg.text]
	for field in fields:
		match = re.search(r'140\d{3}', str(field))
		if match:
			return match.group(0)
		else:
			match = re.search(r'16\d{3}', str(field))
			if match:
				return match.group(0)
	return False

def get_path(roll_no, T):
    if not roll_no:
        T.unidentified += 1
        return os.path.join(ROOT_DIR, UNIDENTIFIED_DIR)
    if roll_no.startswith('14'):
        try:
            roll_no_int = int(roll_no)
        except:
            T.unidentified += 1
            return os.path.join(ROOT_DIR, UNIDENTIFIED_DIR)
        T.reappears += 1
        for proff in proffs:
            if (proffs[proff]["start"] <= roll_no_int and roll_no_int <= proffs[proff]["end"]):
                return os.path.join(ROOT_DIR, proff, REPEATS_DIR)
    elif roll_no.startswith('16'):
        T.regulars += 1
        roll_no_int = int(roll_no)
        for proff in proffs:
            if(roll_no_int in proffs[proff]["regulars"]):
                return os.path.join(ROOT_DIR, proff, REGULARS_DIR)
    T.unidentified += 1
    return os.path.join(ROOT_DIR, UNIDENTIFIED_DIR)

# Doesn't add to STATS
def get_path_safe(roll_no):
    if not roll_no:
        return os.path.join(ROOT_DIR, UNIDENTIFIED_DIR)
    if roll_no.startswith('14'):
        try:
            roll_no_int = int(roll_no)
        except:
            return os.path.join(ROOT_DIR, UNIDENTIFIED_DIR)
        for proff in proffs:
            if (proffs[proff]["start"] <= roll_no_int and roll_no_int <= proffs[proff]["end"]):
                return os.path.join(ROOT_DIR, proff, REPEATS_DIR)
    elif roll_no.startswith('16'):
        roll_no_int = int(roll_no)
        for proff in proffs:
            if(roll_no_int in proffs[proff]["regulars"]):
                return os.path.join(ROOT_DIR, proff, REGULARS_DIR)
    return os.path.join(ROOT_DIR, UNIDENTIFIED_DIR)

def write_file(dir_path, filename, payload):
    try:
        with open(os.path.join(dir_path, filename), 'wb') as file:
            print(filename)
            file.write(payload)
    except:
        if(not os.path.isdir(dir_path)):
            os.makedirs(dir_path)
            with open(os.path.join(dir_path, filename), 'wb') as new_file:
                print(filename)
                new_file.write(payload)
        else:
            print('ERROR INVALID DIRECTORY PATH')
            print(dir_path)
            sys.exit(1)

# LOGIN and DOWNLOAD
print()
print('Signing In')
with MailBox(EMAIL_LINK).xoauth2(EMAIL, access_token) as mailbox:
    print('Signed In. Fetching emails...')
    print('This might take some time so drink some Chai ^^')
    print()
    T = Tracker()
    fetched = mailbox.fetch(AND(sent_date=sent_date))

    for msg in fetched:
        if not LIMIT:
            break
        else:
            LIMIT -= 1
        roll_no = extract_roll_no(msg)
        if roll_no and roll_no in attendance:
            continue

        T.email_count += 1
        dir_path = get_path(roll_no, T)
        # 1 Attachment: Typically pdf or zip
        if(len(msg.attachments) == 1):
            T.att_count += 1
            att = msg.attachments[0]
            ext = att.filename.split('.')[-1]
            name = roll_no if roll_no else f'[{msg.from_}]'
            filename = f'{name}.{ext}'
            write_file(dir_path, filename, att.payload)
            if roll_no:
                attendance.append(roll_no)

        # Multiple attachments: Typically different pages of the exam
        elif (len(msg.attachments) > 1):
            # Create directory
            new_dir = roll_no if roll_no else f'[{msg.from_}]'
            dir_path = os.path.join(dir_path, new_dir)

            for att in msg.attachments:        
                T.att_count += 1
                print(att.filename)
                write_file(dir_path, att.filename, att.payload)
            if roll_no:
                attendance.append(roll_no)

        # No attachments: Probably sent a link or something
        else:
            payload = ''
            if msg.from_:
                payload += 'From: '
                payload += msg.from_
            if roll_no:
                payload += '\nUni Roll No: '
                payload += roll_no
                payload += '\nSave at: '
                payload += get_path_safe(roll_no)
            if msg.subject:
                payload += '\nSubject: '
                payload += msg.subject
            if msg.text:
                payload += '\nContent: '
                payload += msg.text
            if payload:
                no_attachments.append(payload)
            else:
                no_attachments.append('<EMPTY EMAIL>')

# STATS
T.print()
print(f'{len(attendance)} submisssions received [Attendance.txt]')
print(f'{len(no_attachments)} emails did not have attachments [No Attachments.txt]')

print()
print('Sorting attendance')
attendance.sort(key=lambda x: int(x))
print('Sorted')
print('Writing Attendance File [Attendance.txt]')
with open(os.path.join(ROOT_DIR, 'Attendance.txt'), 'w') as attendance_file:
    for rno in attendance:
        attendance_file.write(rno)
        attendance_file.write('\n')
print('Written')

print()
print('Writing No Attachments file [No_Attachments.txt]')
if(len(no_attachments) > 0):
    with open(os.path.join(ROOT_DIR, 'No_Attachments.txt'), 'w') as no_attachments_file:
        for payload in no_attachments: 
            no_attachments_file.write(str(payload))
            no_attachments_file.write('\n')
print('Written')

print()
print('Have a nice day! :)')
