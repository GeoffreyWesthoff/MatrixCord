import asyncio
import discord
from matrix_client.client import MatrixClient
from matrix_client.api import MatrixHttpApi
import configparser
import json
import requests

config = configparser.ConfigParser()
config.read("config.ini")
username = config['settings']['username']
password = config['settings']['password']
room_id = config['settings']['room']
channel = config['settings']['channel']
discord_token = config['settings']['discord_token']
webhook_url = config['settings']['webhook_url']
webhook_user = config['settings']['webhook_user']

guest_client = MatrixClient('http://matrix.org')

discord_client = discord.Client()

matrix_client = MatrixClient("http://matrix.org")
matrix_client.login_with_password(username=username,password=password)


@discord_client.event
async def on_ready():
    print('MatrixCord is ready')

@discord_client.event
async def on_message(discord_message):
    if str(discord_message.author.id) != str(webhook_user):
        #token = guest_client.register_as_guest()
        #matrix_api = MatrixHttpApi("http://matrix.org",token=token)
        id = "@_discord_" + str(discord_message.author.id) + ":matrix.org"
        print(id)
        #guest_client.set_user_id(user_id=str(id))
        #matrix_api.set_display_name(user_id=id, display_name=str(discord_message.author))
        room = matrix_client.join_room(room_id)
        room.send_text(str(discord_message.author) + " says in channel #"+str(discord_message.channel) + ": " + discord_message.content)

def on_matrix_message(room, event):
    if event['type'] == "m.room.message":
        if event['content']['msgtype'] == "m.text":
            user = matrix_client.get_user(event['sender'])
            payload = {'content': event['content']['body'],'username': user.get_display_name(),'avatar_url': user.get_avatar_url() }
            headers = {'content-type': 'application/json'}
            response = requests.post(webhook_url, data=json.dumps(payload),headers=headers)
        if event['content']['msgtype'] == "m.image":
            user = matrix_client.get_user(event['sender'])
            image_id = event['content']['url'].rsplit('/',1)[1]
            matrix_url = 'https://matrix.org/_matrix/media/v1/download/matrix.org/'+image_id
            payload_image = {'content': matrix_url, 'username': user.get_display_name(),
                       'avatar_url': user.get_avatar_url()}
            headers_image = {'content-type': 'application/json'}
            requests.post(webhook_url, data=json.dumps(payload_image), headers=headers_image)

room = matrix_client.join_room(room_id)

room.add_listener(on_matrix_message)
matrix_client.start_listener_thread()



discord_client.run(discord_token)