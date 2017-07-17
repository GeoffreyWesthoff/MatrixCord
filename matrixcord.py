import asyncio
import discord
from matrix_client.client import MatrixClient
from matrix_client.api import MatrixHttpApi
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
username = config['settings']['username']
password = config['settings']['password']
room_id = config['settings']['room']
channel = config['settings']['channel']
discord_token = config['settings']['discord_token']

guest_client = MatrixClient('http://matrix.org')

discord_client = discord.Client()

matrix_client = MatrixClient("http://matrix.org")
matrix_client.login_with_password(username=username,password=password)


@discord_client.event
async def on_ready():
    print('MatrixCord is ready')

@discord_client.event
async def on_message(discord_message):
    #token = guest_client.register_as_guest()
    #matrix_api = MatrixHttpApi("http://matrix.org",token=token)
    id = "@_discord_" + str(discord_message.author.id) + ":matrix.org"
    print(id)
    #guest_client.set_user_id(user_id=str(id))
    #matrix_api.set_display_name(user_id=id, display_name=str(discord_message.author))
    room = matrix_client.join_room(room_id)
    room.send_text(str(discord_message.author) + " says in channel #"+str(discord_message.channel) + ": " + discord_message.content)

#def on_matrix_message(room, event):
    #if event['type'] == "m.room.message":
        #if event['content']['msgtype'] == "m.text":
            #matrix_message = ("{0}: {1}".format(event['sender'], event['content']['body']))
            #await discord_client.send_message(discord_client.get_channel(channel), matrix_message)



discord_client.run(discord_token)