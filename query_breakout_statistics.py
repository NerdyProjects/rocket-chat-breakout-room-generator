from pprint import pprint
import os
from bigbluebutton_api_python import BigBlueButton
from dotenv import load_dotenv
import argparse

parser = argparse.ArgumentParser(description='Query BBB meeting stats')
parser.add_argument('--details', action='store_true')

args = parser.parse_args()
load_dotenv()

bbb_server = [
        { 'server': 'bbb1.klimacamp-leipzigerland.de', 'secret': os.getenv("BBB1_SECRET"), 'capacity': 100, 'phone': '+49 3222 9980 230' },
        { 'server': 'bbb2.klimacamp-leipzigerland.de', 'secret': os.getenv("BBB2_SECRET"), 'capacity': 100 },
        { 'server': 'meet.livingutopia.org', 'secret': os.getenv("BBB3_SECRET"), 'capacity': 50, 'phone': '+49 5563 263 9980' }
        ]

bbb = [BigBlueButton(x['server'], x['secret']) for x in bbb_server]

def printMeeting(m):
    if args.details:
        print(m)
    if (len(m['attendees']) > 0 and isinstance(m['attendees']['attendee'], list)):
        attendees = len(m['attendees']['attendee'])
    elif len(m['attendees']) == 0:
        attendees = 0
    else:
        attendees = 1
    print('Meeting {} with {} attendees:'.format(m['meetingName'], attendees))

for b in bbb:
    print('next server:')
    m = b.get_meetings()['xml']['meetings']
    if len(m) > 0:
        if isinstance(m['meeting'], list):
            for meeting in m['meeting']:
                printMeeting(meeting)
        else:
            printMeeting(m)
    else:
        print('No meetings!')

