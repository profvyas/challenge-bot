import discord
import os

class ChallengeBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.userMessages = []

    def run(self):
        self.loop.run_until_complete(self.start(os.environ['TOKEN']))

    async def on_ready(self):
        print('we have logged in as {0.user}'.format(self))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$command'):
            await message.channel.send("you just called the challenge-bot from " + str(message.channel.mention) +  " channel in '" + str(message.guild.name) + "' server with server id:" + str(message.guild.id) +"!")
        
        # if message.content.startswith('$flush'):
        #     for msg in userMessages:
        #         await message.channel.send(msg)
