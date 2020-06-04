from pprint import pprint
import os
from rocketchat_API.rocketchat import RocketChat
from dotenv import load_dotenv
import random

load_dotenv()

user = os.getenv("RC_USERNAME")
pw = os.getenv("RC_PASSWORD")
group_size = 5
channel = 'zirkuszelt'
server = 'https://chat.klimacamp-leipzigerland.de'

class MyRocket(RocketChat):
    def create_discussion(self, room_id, name, users, **kwargs):
        return rocket._RocketChat__call_api_post('rooms.createDiscussion', prid=room_id, t_name=name, kwargs=kwargs)

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

discussion = rocket.create_discussion(room_id, 'Bezugsgruppe XY', ['matthias']).json()
#pprint(discussion)


