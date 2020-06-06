from pprint import pprint
import os
from rocketchat_API.rocketchat import RocketChat
from bigbluebutton_api_python import BigBlueButton
from dotenv import load_dotenv
import random

load_dotenv()

dry_run = True
user = os.getenv("RC_USERNAME")
pw = os.getenv("RC_PASSWORD")
group_size = 4
channel = 'zirkuszelt'
server = 'https://chat.klimacamp-leipzigerland.de'
breakout_time = 15
ignore_users = ['bezugsgruppenbot']
bbb_server = [
        { 'server': 'bbb1.klimacamp-leipzigerland.de', 'secret': os.getenv("BBB1_SECRET"), 'capacity': 100, 'phone': '+49 3222 9980 230' },
        { 'server': 'bbb2.klimacamp-leipzigerland.de', 'secret': os.getenv("BBB2_SECRET"), 'capacity': 100 },
        { 'server': 'meet.livingutopia.org', 'secret': os.getenv("BBB3_SECRET"), 'capacity': 50, 'phone': '+49 5563 263 9980' }
        ]

class MyRocket(RocketChat):
    def create_discussion(self, room_id, name, users, **kwargs):
        return rocket._RocketChat__call_api_post('rooms.createDiscussion', prid=room_id, t_name=name, kwargs=kwargs)

bbb = [BigBlueButton(x['server'], x['secret']) for x in bbb_server]

for b in bbb:
    print('next server')

rocket = MyRocket(user, pw, server_url=server)

#room = rocket.channels_info(channel=channel).json()
room = rocket.rooms_info(room_name=channel).json()
pprint(room)
room_id = room['room']['_id']

print('querying channel members')
members = rocket.channels_members(room_id=room_id, count=0).json()
pprint(members)

if not members['success']:
    print('retrying query as group members...')
    members = rocket.groups_members(room_id=room_id, count=0).json()
    pprint(members)

online_members = [x for x in members['members'] if x['status'] == 'online' and x['username'] not in ignore_users]
groups = len(online_members) // group_size
remainder_group_size = len(online_members) % group_size

print('found {} online (out of {}) people. Creating {} groups of {} people (+1 group of {} people)'.format(len(online_members), len(members['members']), groups, group_size, remainder_group_size))

random.shuffle(online_members)
pprint(online_members)

#discussion = rocket.create_discussion(room_id, 'Bezugsgruppe XY', ['matthias', 'hQv5AbM2dkYG3qWbt']).json()
#rocket.channels_invite('2MnTfa6t2Tk4jwpDu', 'hQv5AbM2dkYG3qWbt')
#pprint(discussion)

assigned = 0
use_bbb = 0
meeting = None
meeting_id = None
for m in online_members:
    if meeting is None or meeting_size >= group_size:
        if (assigned + group_size) > bbb_server[use_bbb]['capacity']:
            print('switching to next BBB server after assigning {} people to {}'.format(assigned, bbb_server[use_bbb]['server']))
            use_bbb = use_bbb + 1
            assigned = 0
            if use_bbb >= len(bbb_server):
                print('Failure: No BBB server capacity left!')
                exit()
        meeting_size = 0
        meeting_id = 'bzgs' + str(assigned) + 'meet'
        if not dry_run:
            meeting = bbb[use_bbb].create_meeting(meeting_id, {'attendeePW': 'attendee', 'moderatorPW': 'moderator', 'duration': breakout_time})['xml']
        else:
            meeting = {'voiceBridge': 'test-bridge'}
        pprint(meeting)
    nick = m['name'] if 'name' in m else m['username']
    if not dry_run:
        join = bbb[use_bbb].get_join_meeting_url(nick, meeting_id, 'attendee')
    else:
        join = 'https://test.join.url'
    pprint(join)
    if not dry_run:
        chat = rocket.im_create(m['username']).json()
        pprint(chat)
    else:
        print('would create chat with {}'.format(m['username']))

    english_message = 'You have been assigned to an affinity group with some random people. We invite you to have a conference with them for some minutes.'
    if 'phone' in bbb_server[use_bbb]:
        message = 'Deine zufällig zusammengewürfelte Bezugsgruppe trifft sich jetzt für {} Minuten in der folgenden Videokonferenz: {}\nDu kannst unter Verwendung des Konferenzcodes {} auch per Telefoneinwahl (deutsche Festnetznummer) teilnehmen: {}\n{}'.format(breakout_time, join, meeting['voiceBridge'], bbb_server[use_bbb]['phone'], english_message)
    else:
        message = 'Deine zufällig zusammengewürfelte Bezugsgruppe trifft sich jetzt für {} Minuten in der folgenden Videokonferenz: {}\n{}'.format(breakout_time, join, english_message)
    if not dry_run:
        rocket.chat_post_message(message, room_id=chat['room']['_id'])
    else:
        print('would post message {}'.format(message))
    assigned = assigned + 1
    meeting_size = meeting_size + 1

print('generated {} join links'.format(assigned))
