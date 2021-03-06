import os
import discord

botClient = discord.Client()

userMessages = []

@botClient.event
async def on_ready():
  print('we have logged in as {0.user}'.format(botClient))

@botClient.event
async def on_message(message):
  if message.author == botClient.user:
    return

  if message.content.startswith('$command'):
    await message.channel.send("you just called the challenge-bot from " + str(message.channel.mention) +  " channel in '" + str(message.guild.name) + "' server with server id:" + str(message.guild.id) +"!")
    userMessages.append(message.content[8:])
  
  if message.content.startswith('$flush'):
    for msg in userMessages:
      await message.channel.send(msg)

    
botClient.run(os.environ['TOKEN'])
