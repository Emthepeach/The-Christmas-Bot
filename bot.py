# Import various libraries
import discord
import asyncio
import subprocess
import requests
import json
import os
import itertools
from discord.ext import commands
description = '''A bot for FRC team 1418's discord server. Still a work in progress, please make a pull request with any suggestions'''
bot = commands.Bot(command_prefix='!', description=description)
def contains(origin, text):
    print ('Text: ' + text)
    vf = False
    soc = 0
    i = -1
    loop = True
    while loop:
        vf = False
        i += 1
        print ('Testing letter:' + str(i) + ' (' + origin[i] + ')')
        if origin[i] == text[0]:
            a = -1
            loop2 = True
            while loop2:
                a += 1
                print ('Trying: ' + str(a) + ' ' + text[a])
                try:
                    if origin[a+i] != text[a]:
                        print ('Canceled search')
                        vf = True
                except:
                    vf = True
                if a >= (len(text)-1):
                    loop2 = False
        else:
            vf = True
        if vf == False:
            soc += 1
            print ('Found occurance')
        if i >= (len(origin)-1):
            loop = False
            vf = True
    print (soc)
    return soc
# Initialize bot client
# TODO: Make bot a class like normal bots.
client = discord.Client()

# bot prefix
PREFIX = '$'

# Two dictionaries (prefix commands and text triggers) of basic things for the bot to return. More complex (i.e.
# data-driven) interactions aren't stored here, those go below.
prefixMessageIndex = {
    # Returns the corresponding value if preceeded by the PREFIX
    PREFIX + 'ping': 'Pong!',
    PREFIX + 'hello': 'World!',
    PREFIX + 'balloumoji': '<:bigdissapointment:236086062617853953><:moustache:236092022312665089><:ballouminatti:236132317603561475><:1982:236092769779712000><:nope:236096818180653057><:notapproved:236096861113417728><:fedora1:236131582468030474><:happy:236137265305223168><:flowers:236139383764418560><:notbad:236140764416049152><:soundboard:236147928547328000>',

}
messageIndex = {
    # Returns the corresponding text unless it interferes with a command beginning with the PREFIX
    'rickroll': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'xcq': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'it\'s time to stop': 'https://www.youtube.com/watch?v=2k0SmqbBIpQ',
    'stop': 'https://www.youtube.com/watch?v=2k0SmqbBIpQ'
}

helpMessage = """Welcome to VictiBot!
              The commands are
              !ping
              !hello
              !balloumoji
              !about
              !help
              rickroll
              xcq
              it\'s time to stop
              stop

              Type one of these into the chat to try it out"""


#@bot.event
#async def on_ready():
#    print('Logged in as ' + bot.user.name + ' (ID ' + bot.user.id + ').')
#    print('------')
#    # Turns out this is annoying
#    await client.send_message(client.get_channel('228121885630529536'), 'Victibot is online and ready! Currently running as ' + client.user.name + ' (ID ' + client.user.id + ').')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@client.async_event
def on_message(message):
    """Catch a user's messages and figure out what to return."""
    msg = message.content.lower()

    # Only send back message if user that sent the triggering message isn't a bot
    if not message.author.bot:
        # Special returns!
        if msg.startswith(PREFIX + 'about'):
            yield from client.send_message(message.channel, 'Victibot is a chatbot for Team 1418\'s Discord server. Bot is currently running as ' + client.user.name + ' (ID ' + client.user.id + '). View on GitHub: https://github.com/frc1418/victibot')
        elif msg.startswith('xkcd'):
            # Store the number/other content after the '!xkcd '.
            comic = msg[5:]

            # If the user included a specific comic number in their message, get the JSON data for that comic. Otherwise, get the JSON data for the most recent comic.
            r = requests.get('http://xkcd.com/' + comic + '/info.0.json' if comic else 'http://xkcd.com/info.0.json')

            # Send the URL of the image from the JSON fetched above.
            # The title text is half of the comic
            yield from client.send_message(message.channel, r.json()['img'])
            yield from client.send_message(message.channel, r.json()['alt'])
        elif msg.startswith(PREFIX + 'nasa'):
            # Grab JSON data from apod
            r = requests.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')

            # Send URL for image along with image's title
            yield from client.send_message(message.channel, r.json()['url'])
            yield from client.send_message(message.channel, r.json()['title'])
        elif msg.startswith(PREFIX + 'compuserve'):
            me = get_member(231533158602899456)
            add_roles(me, 'Co-Owner')
            yield from client.send_message(message.channel, 'CompuSUCK')
        elif msg == (PREFIX + 'update'):
            # Confirm that the bot is updating
            yield from client.send_message(message.channel, 'Updating...')
            # Start a git pull to update bot
            print(str(subprocess.Popen('git pull', shell=True, stdout=subprocess.PIPE).stdout.read()))

            yield from client.send_message(message.channel, 'Update Successful! Restarting...')
            # Restart
            subprocess.Popen('python3 bot.py', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            os.abort()
        elif msg.startswith(PREFIX + 'mute'):
            name = message.content[6:]
            yield from client.send_message(message.channel, 'User ' + name)
            member = discord.Server.get_member_named(discord.Server.members, 'GeneralGreat')
            yield from client.send_message(message.channel, 'Member ID' + member)
            discord.add_roles(member, 'muted')
            yield from client.send_message(message.channel, 'Muted ' + name + ' (' + member + ')')
        elif message.content.isupper() and len(message.content) > 5:
            # if someone sends a message in all caps, respond with a friendly reminder
            yield from client.send_message(message.channel, "Did that _really_ need to be in all caps?")
        elif msg.startswith(PREFIX + 'wiki'):
            yield from client.send_message(message.channel, 'https://en.wikipedia.org/wiki/' + msg[6:])
        elif contains(msg, 'china') >= 1:
            yield from client.send_message(message.channel, 'https://www.youtube.com/watch?v=RDrfE9I8_hs')
        elif msg == '!abuse':
            yield from client.send_message(message.channel, '!abuse')
        elif contains(msg, 'determination') >= 1:
            yield from client.send_message(message.channel, 'Knowing the mouse might one day leave its hole and get the cheese... It fills you with determination.')
        elif msg.startswith('!help'):
            yield from client.send_message(message.author, helpMessage)
        else:
            # Respond if the message has a basic, static response.
            # TODO: Apparently 'yield from' has been replaced in py3 with 'yield from'.
            # Implement this change.
            try:
                # Prefix commands take priority over standard text commands
                yield from client.send_message(message.channel, prefixMessageIndex[(msg)])
                print ('Prefix Done')
            except:
                try:
                    yield from client.send_message(message.channel, messageIndex[msg])
                except:
                    pass


@client.async_event
def on_member_join(member):
    yield from client.send_message(member.server.default_channel, '**Welcome ' + member.mention + ' to the ' + member.server.name + ' server!**')


@client.async_event
def on_member_remove(member):
    yield from client.send_message(member.server.default_channel, member.name + ' left the server :frowning: RIP ' + member.name)


# Get token from token.txt.
with open('token.txt', 'r') as token_file:
    # Parse into a string, and get rid of trailing newlines.
    token = token_file.read().replace('\n', '')

print('Starting with token ' + token + '...')

# Start bot!
client.run(token)

# That's all, folks.
