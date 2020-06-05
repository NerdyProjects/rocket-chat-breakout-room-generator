from pprint import pprint
import os
from rocketchat_API.rocketchat import RocketChat
from bigbluebutton_api_python import BigBlueButton
from dotenv import load_dotenv
import random

load_dotenv()

user = os.getenv("RC_USERNAME")
pw = os.getenv("RC_PASSWORD")
group_size = 5
channel = 'zirkuszelt'
server = 'https://chat.klimacamp-leipzigerland.de'
bbb_server = [
        { 'server': 'bbb1.klimacamp-leipzigerland.de', 'secret': os.getenv("BBB1_SECRET"), 'capacity': 100 },
        { 'server': 'bbb2.klimacamp-leipzigerland.de', 'secret': os.getenv("BBB2_SECRET"), 'capacity': 100 }
        #{ 'server': 'meet.livingutopia.org', 'secret': os.getenv("BBB3_SECRET"), 'capacity': 100 }
        ]

class MyRocket(RocketChat):
    def create_discussion(self, room_id, name, users, **kwargs):
        return rocket._RocketChat__call_api_post('rooms.createDiscussion', prid=room_id, t_name=name, kwargs=kwargs)

bbb = [BigBlueButton(x['server'], x['secret']) for x in bbb_server]

for b in bbb:
    print('next server')
    pprint(b.get_default_config_xml())

rocket = MyRocket(user, pw, server_url=server)

room = rocket.channels_info(channel=channel).json()
room_id = room['channel']['_id']
#pprint(room)

members = rocket.channels_members(room_id=room_id, count=0).json()

online_members = [x for x in members['members'] if x['status'] == 'online']
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
        meeting_size = 0
        meeting_id = 'bzgs' + str(assigned) + 'meet'
        meeting = bbb[use_bbb].create_meeting(meeting_id, {'attendeePW': 'attendee', 'moderatorPW': 'moderator', 'duration': 5})
        pprint(meeting)
    nick = m['name'] if 'name' in m else m['username']
    join = bbb[use_bbb].get_join_meeting_url(nick, meeting_id, 'attendee')
    pprint(join)
    assigned = assigned + 1
    meeting_size = meeting_size + 1

print('generated {} join links'.format(assigned))
